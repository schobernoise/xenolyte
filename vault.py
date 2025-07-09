import utils, shutil,os
from table import Table
from database import Database
from datetime import datetime
import logging

VAULT_CONFIG_TEMPLATE = {
    "id": "generate_id",
    "theme": "default",
    "default_column_width": 20,
    "backup_path": "",
    "modified": "",
}

class Vault:

    def __init__(self,path,init=False):
        self.containers = []
        self.path = path
        self.name = utils.get_folder_name(path)
        if init:
            self.initialize_vault()
        self.config = self.fetch_vault_config()
        self.set_vault_modified_now()
        self.containers = self.read_all_containers_from_dir()
        self.note = "" # TODO: Fetch Vault Note
        self.__str__ = self.name


    def initialize_vault(self):
        if not os.path.isdir(self.path):
            utils.create_empty_folder(self.path)
        utils.write_json(os.path.join(self.path,f"{self.name}.json"),VAULT_CONFIG_TEMPLATE)
        # self.reflect_changes()

    
    def reflect_changes(self):
        logging.info("Reflect changes...")
        dir_containers= self.read_all_containers_from_dir()

        # Check if Memory is consistent with Filetree (Create)
        for container in self.containers:
            if isinstance(container, Table):
                if not os.path.isfile(container.table_path):
                    with open(container.table_path, 'a', encoding="utf-8",newline="") as f:
                        writer = csv.DictWriter(f, fieldnames=container.fieldnames, delimiter=";")
                    logging.info("Created Table CSV", container.name)
            elif isinstance(container,Database):
                if not os.path.exists(container.path):
                    container.initialize_database()

        # Check if Filetree is consistent with Memory (Delete)
        for container in dir_containers:
            if not self.get_container_from_name(container.name):
                if isinstance(container, Table):
                    os.remove(container.table_path)
                    logging.info(f"Deleted Table CSV {container.name}" )
                elif isinstance(container,Database):
                    shutil.rmtree(container.table_path, ignore_errors=True)
                    logging.info(f"Deleted Database Dir {container.name}")
        
        self.set_vault_modified_now() # Writes entire config
        # TODO: Reflect changes returns status and errors
    

    def fetch_vault_config(self):
        return utils.read_json(os.path.join(self.path,f"{self.name}.json"))


    def read_all_containers_from_dir(self):
        logging.info("Initialize all Containers in all Vaults.")
        containers=[]
        try:
            items = os.listdir(self.path)
        except Exception as e:
            logging.error(f"Error reading directory {self.path}: {e}")
            return containers

        for item in items:
            item_path = os.path.join(self.path, item)
            logging.debug("%s", item_path)
            if os.path.isfile(item_path) and item.lower().endswith('.csv'):
                containers.append(Table(item_path))
            elif os.path.isdir(item_path):
                # print(table_path)
                containers.append(Database(item_path))
        return containers


    def get_container_from_name(self, name):
        """Returns a table or databse object by its name"""
        # TODO: Expand fn to general query functionality.
        logging.info("Get Table from Name")
        for container in self.containers:
            if container.name == name:
                logging.debug(f"Found Container {name}")
                return container
        return False


    def create_new_table(self,name):
        """Creates a new table inside the active Vault."""
        logging.debug("Create New Table")
        self.containers.append(Table(os.path.join(self.path,name + ".csv"),init=True))
        self.reflect_changes()
        logging.info("Created new Table")
    

    def create_new_database(self, name):
        """Creates a new database inside the active Vault."""    
        logging.info(f"Create New Database {os.path.join(self.path,name)}")
        self.containers.append(Database(os.path.join(self.path,name),init=True))
        self.reflect_changes()
        logging.info("Created new Database")
        

    def create_database_from_table(self, name):
        """Creates a database from an existing table inside the active Vault."""
        logging.info("Create Database from Table")
        # Two methods of doing this
            # 1. Copying the CSV over after creating the folder structure
                # Big files get copied faster as is, no validation
            # 2. Use Data Model to handle transfer
                # Might take longer for larger Data but data can be validated/manipulated on the fly  
            # TODO: Sticking with Method no. 2 for now. Might add a flag for manual transfer later.
        temp_table = self.delete_container(name)
        self.containers.append(Database(os.path.join(self.path,name),records=temp_table.records))
        self.reflect_changes()
        logging.info("Created Database from Table")
    

    def delete_container(self, name):
        """Deletes an Entity from the Vault."""
        for table in self.containers:
            if table.name == name:
                self.containers.remove(table)
                self.reflect_changes()
                return table
        logging.info("Deleted Table")
    

    def set_vault_modified_now(self):
        self.config["modified"] = str(datetime.now())
        utils.write_json(os.path.join(self.path,f"{self.name}.json"),self.config)
    

    def write_vault_note(self, note): 
        VAULT_NOTE_TEMPLATE = f"""# Database - {self.name} 
"""     
        if not note and not self.note:
            note = VAULT_NOTE_TEMPLATE
        utils.write_markdown(os.path.join(self.path,self.name + ".md"),note)

    
    def fetch_vault_note(self):
        if os.path.isfile(os.path.join(self.path,self.name + ".md")):
            return utils.read_markdown(os.path.join(self.path,self.name + ".md"))
        else:
            self.write_vault_note()
            return utils.read_markdown(os.path.join(self.path,self.name + ".md"))