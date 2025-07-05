import table
import utils
import os
import logging
from datetime import date
import shutil

today = date.today()

CONFIG_TEMPLATE = {
    "id": "generate_id",
    "columns": [
        {
            "name": "id",
            "_type": "int",
            "width": 20
        }
    ]
}


class Database(table.Table):

        def __init__(self, path, records=False, init=False):
            logging.debug(f"Creating Database: {path}")
            self.path = os.path.split(os.path.normpath(path))[0]
            self.name = utils.get_folder_name(self.path.replace(".csv",""))
            logging.debug(f"Database Name: {self.name}")
            self.table_path = os.path.join(self.path, self.name + ".csv")
            if init:
                self.initialize_database(records)
            self.fieldnames = utils.get_fieldnames_from_file(self.table_path)
            if records:
                self.records = records
            else:
                self.records = utils.read_csv(os.path.join(self.path, f"{self.name}.csv"))
            self._type = "database"
            self.config = self.fetch_config_json
            if not os.path.exists(os.path.join(self.path,self.name + ".md")):
                self.create_database_note()
            self.note = self.fetch_database_note()
        

        def reflect_changes(self):
            self.write_config_json(self.config)
            utils.write_csv(self.table_path,self.records,self.fieldnames)


        def initialize_database(self, records, create_folders=False):
            if not records:
                records = [{"id": 0}]
            utils.create_empty_folder(self.path)
            self.write_config_json(CONFIG_TEMPLATE)
            utils.write_csv(self.table_path,records,records[0].keys())
            self.create_functions_py()
            self.create_database_note()
            if create_folders:
                self.create_all_record_folders()
            self.reflect_changes()

        
        # TODO: Extend every record with properties 
        # to reflect changes for every record.
        # E.g. Property "Folder = True"
        # Reflect changes automatically creates/deletes
        # Record Folder


        def create_record_folder(self, id):
            """Creates a folder for a record."""
            logging.info("create Record Folder")
            record = self.fetch_record(id)
            utils.create_empty_folder(os.path.join(self.path,f"{record.id} {record.slug}"))

            
        def create_all_record_folders(self):
            for record in self.records:
                self.create_record_folder(record.id)
        

        def create_functions_py(self):
            pass


        def write_config_json(self,config):
            config_path = os.path.join(self.path,"config.json")
            utils.write_json(config_path,config)
        

        def fetch_config_json(self):
            return utils.read_json(self.path,"config.json")
        

        def create_database_note(self):
            DATABASE_NOTE_TEMPLATE = f"""# Database - {self.name} 
"""
            with open(os.path.join(self.path,self.name + ".md"), 'w') as f:
                f.write(DATABASE_NOTE_TEMPLATE)


        def create_record_note(self,id):
            record = self.fetch_record(id)
            RECORD_NOTE_TEMPLATE = f"""# {record.id} {record.name} 
"""
            with open(os.path.join(self.path,f"{record.id} {record.slug}",f"{record.id} {record.slug}.md"), 'w') as f:
                f.write(RECORD_NOTE_TEMPLATE)   
        

        def fetch_database_note(self):
            with open(os.path.join(self.path,self.name + ".md"), 'r', encoding='utf-8') as file:
                content = file.read()
            return content
        

        def fetch_record_note(self,id):
            record = self.fetch_record(id)
            with open(os.path.join(self.path,f"{record.id} {record.slug}",f"{record.id} {record.slug}.md"), 'r', encoding='utf-8') as file:
                content = file.read()
            return content
