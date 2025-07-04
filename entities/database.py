import table
import utils
import os
import model
import logging
from datetime import date
import shutil

today = date.today()


class Database(table.Table):
    
        def __init__(self, path, records=False):
            self.path = path
            self.name = utils.get_folder_name(self.path)
            self.status = "cold"
            if records:
                self.records = records
            else:
                self.records = model.records.read_records(os.path.join(self.path, f"{self.name}.csv"))
            self._type = "database"
            self.config = utils.get_config_json(self.path)
        
        def reflect_changes(self):
            pass

        
        def load_database(self, path):
            """Returns a database object."""
            logging.info("database: Load Database")
            database_name = utils.get_folder_name(path)[1]
            table_path = os.path.join(path, f"{database_name}.csv")
            table = utils.fetch_table(table_path)
            config = utils.get_config_json(path)
            return {
                "_type": "database",
                "name": database_name,
                "records": table,
                "config": config,
                "path": path
            }
        
        def create_record_folder(self, path, id):
            """Creates a folder form a record."""
            logging.info("create Record Folder")
            record = get_record(path,id)
            return utils.create_record_folder(path,record)