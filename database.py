import table
import utils
import os
import logging
from datetime import date
import shutil
import importlib.util
import sys

today = date.today()

CONFIG_TEMPLATE = {
    "id_type": "increment",
    "columns": [
        {
            "name": "id",
            "_type": "int",
            "width": 20
        }
    ]
}

FUNCTIONS_TEMPLATE = """
# Xenolyte - functions.py
# All functions in here receive the database instance.

def fill_cells_w_xenolyte(self):
    \"\"\"Example function to demonstrate functions.py
        Fills all cells with the word 'xenolyte'.
    \"\"\"
    for record in self.records:
        for key in record.keys():
            if not record[key]:
                record[key] = "xenolyte"
    self.reflect_changes()"""


class Database(table.Table):

        def __init__(self, path, records=False, init=False):
            logging.debug(f"Loading Database: {path}")
            self.path = path
            self.name = utils.get_folder_name(self.path)
            logging.debug(f"Database Name: {self.name}")
            self.table_path = os.path.join(self.path, self.name + ".csv")
            logging.debug(f"Table Path: {self.table_path}")
            if not os.path.exists(os.path.join(self.path,"config.json")) or init:
                logging.error("config.json was not found.")
                # raise FileNotFoundError("Please provide xenolyte.json. Copy the template file from the repo.")  
                self.initialize_database(records)
            if records:
                self.records = records
            else:
                if not os.path.isfile(self.table_path):
                    logging.debug(f"{self.table_path} not existing, starting Initialization.")
                    self.initialize_database(records)
                self.records = utils.read_csv(self.table_path)
            self.fieldnames = utils.get_fieldnames_from_file(self.table_path)
            self._type = "database"
            self.config = self.fetch_config_json()
            if not os.path.exists(os.path.join(self.path,self.name + ".md")):
                self.create_database_note()
            self.note = self.fetch_database_note()
            if not os.path.exists(os.path.join(self.path,"functions.py")):
                self.create_functions_py()
            self.functions = self.load_functions(os.path.join(self.path,"functions.py"))
            # logging.debug(f"{self.functions}")
            # self.functions.fill_cells_w_random_data(self)
        

        def load_functions(self,source):
            # Credit: https://medium.com/@david.bonn.2010/dynamic-loading-of-python-code-2617c04e5f3f
            """
            reads file source and loads it as a module

            :param source: file to load
            :param module_name: name of module to register in sys.modules
            :return: loaded module
            """

            module_name = "functions"

            spec = importlib.util.spec_from_file_location(module_name, source)
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)

            return module
        

        def reflect_changes(self):
            self.write_config_json(self.config)
            utils.write_csv(self.table_path,self.records,self.fieldnames)


        def initialize_database(self, records, create_folders=False):
            if not os.path.isdir(self.path):
                logging.debug(f"Create Path {self.path}")
                utils.create_empty_folder(self.path)
            if not records:
                records = [{"id": 0}]
            if not os.path.exists(self.table_path):
                logging.debug(f"Path not existing.")
                utils.write_csv(self.table_path,records,records[0].keys())
            if not os.path.exists(os.path.join(self.path,"config.json")):
                self.write_config_json(CONFIG_TEMPLATE)
            if not os.path.exists(os.path.join(self.path,"functions.py")):
                self.create_functions_py()
            if not os.path.exists(os.path.join(self.path,f"{self.name}.md")):
                self.create_database_note()
            if create_folders:
                self.create_all_record_folders()
            # self.reflect_changes()

        
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
            self.create_record_note(id)

        
        def create_column(self,name,_type="str",width=20):
            for fieldname in self.fieldnames:
                if name == fieldname:
                    logging.error("Columns must have unique names.")
                    return 0
            self.fieldnames.append(name)
            self.config["columns"].append({
            "name": name,
            "_type": _type,
            "width": int(width)
        })
            self.reflect_changes()


        def create_all_record_folders(self):
            for record in self.records:
                self.create_record_folder(record.id)
        

        def create_functions_py(self):
            functions_path = os.path.join(self.path,"functions.py")
            utils.write_code(functions_path,FUNCTIONS_TEMPLATE)
        

        def call_function(self,name):
            try:
                fn = getattr(self.functions, name)
            except:
                logging.error(f"Please provide a valid function in functions.py.")
                return 0
            fn(self)


        def write_config_json(self,config):
            logging.debug(f"{config}")
            config_path = os.path.join(self.path,"config.json")
            utils.write_json(config_path,config)
        

        def fetch_config_json(self):
            if not os.path.isfile(os.path.join(self.path,"config.json")):
                self.write_config_json(CONFIG_TEMPLATE)
                return
            return utils.read_json(os.path.join(self.path,"config.json"))
        

        def create_database_note(self): 
            DATABASE_NOTE_TEMPLATE = f"""# Database - {self.name} 
"""
            utils.write_markdown(os.path.join(self.path,self.name + ".md"),DATABASE_NOTE_TEMPLATE)


        def create_record_note(self,id):
            record = self.fetch_record(id)
            RECORD_NOTE_TEMPLATE = f"""# {record.id} {record.name} 
"""
            utils.write_markdown(os.path.join(self.path,f"{record.id} {record.slug}",f"{record.id} {record.slug}.md"),RECORD_NOTE_TEMPLATE)  
        

        def fetch_database_note(self):
            return utils.read_markdown(os.path.join(self.path,self.name + ".md"))
        

        def fetch_record_note(self,id):
            record = self.fetch_record(id)
            return utils.read_markdown(os.path.join(self.path,f"{record.id} {record.slug}",f"{record.id} {record.slug}.md"))
