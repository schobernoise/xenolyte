import utils
import os, shutil
import logging
from datetime import datetime
from vault import Vault

XENOLYTE_CONFIG_TEMPLATE = {
    "theme": "default",
    "default_column_width": 20,
    "global_backup_enabled": True,
    "global_backup_path": "",
    "vaults_csv": "data/vaults.csv"
}

class Xenolyte:

    def __init__(self,first_vault_path=False):
        if not os.path.exists("./data/xenolyte.json"):
            logging.error("xenolyte.json was not found.")
            raise FileNotFoundError("Please provide xenolyte.json. Copy the template file from the repo.")  
       
        self.vaults = []
        self.config = self.fetch_config()
        self.fieldnames = ["path"]
        if first_vault_path:
            self.inititalize_xenolyte(first_vault_path)
        if not os.path.exists(self.config["vaults_csv"]):
            logging.error(f"{self.config["vaults_csv"]} was not found.")
            raise FileNotFoundError(f"{self.config["vaults_csv"]} was not found. Most likely Xenolyte was not initialized. Please run 'python cli.py xenolyte init' first. Or provide the correct path in xenolyte.json.")     
        
        for vault in utils.read_csv(self.config["vaults_csv"]):
            self.vaults.append(Vault(vault["path"]))
        
        
    def reflect_changes(self):
        utils.write_json("./data/xenolyte.json",self.config)
        self.write_vaults_csv()
        
    
    def inititalize_xenolyte(self,first_vault_path):
        # utils.write_json("./data/xenolyte.json",XENOLYTE_CONFIG_TEMPLATE)
        self.write_vaults_csv()
        self.create_new_vault(first_vault_path)


    def fetch_config(self):
        return utils.read_json("./data/xenolyte.json")


    def fetch_all_vaults(self):
        return self.vaults
        

    def fetch_recent_vault(self):
        return max(self.vaults, key=lambda obj: obj.config["modified"])


    def fetch_vault(self,name):
        for vault in self.vaults:
            if name == vault.name:
                return vault
        return False


    def create_new_vault(self,path):
        self.vaults.append(Vault(path,init=True))
        self.reflect_changes()
    

    def add_exisiting_vault(self,path):
        self.vaults.append(Vault(path))
        self.reflect_changes()
        

    def write_vaults_csv(self):
        logging.debug("Write Vaults CSV")
        vault_paths = []
        for vault in set(self.vaults): # Creating set to clean up duplicates
            vault_paths.append({"path":vault.path})
        utils.write_csv(self.config["vaults_csv"],vault_paths,self.fieldnames)


    def forget_vault(self,name):
        """This does NOT delete the Vault Folder."""
        for vault in self.vaults:
            if vault.name == name:
                self.vaults.remove(vault)
                self.reflect_changes()
                return vault

