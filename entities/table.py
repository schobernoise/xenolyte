import table
import utils
import os
import model
import logging
from datetime import date
import shutil

today = date.today()

class Table:
    
    def __init__(self, path):
        self.path = path
        self.name = utils.get_folder_name(path)
        self.status = "cold"
        self.records = model.records.read_records(self.path)
        self._type = "table"

    
    def reflect_changes(self):
        pass
    

    def write_table():
        model.records.overwrite_records(self.path,self.records)

    
    def append_record(new_record):
        self.records.append(new_record)


    def delete_record(id):
        self.records.pop()
    

    




    


    def load_table(self, path):
        """Returns a table object."""
        logging.info("database: Load Table")
        return {
            "_type": "table",
            "name": utils.get_folder_name(path.replace(".csv",""))[1],
            "records": utils.fetch_table(path),
            "path": path
        }


    def get_record_from_table(self, table, id):
        """Returns the record of a table object."""
        logging.info("database: Get Record from Table")
        logging.debug("database: %s", table)
        logging.debug("database: %s", id)
        for record in table["records"]:
            if record["id"] == id:
                return record
        return False


    def create_record_in_table(self, table, record,id=False):
        """Creates a record."""
        logging.info("database: Create Record")
        logging.debug("database: %s", table)
        logging.debug("database: %s", record)
        logging.debug("database: %s", id)
        table_path = os.path.join(path, f"{table}.csv")
        model.records.create_record(table_path,record)
        logging.info(f"database: Create Record with Id {record['id']}")
        return record


    def delete_record_from_table(self, table,id):
        """Deletes the record."""
        logging.info("database: Delete Record")
        logging.debug("database: %s", path)
        logging.debug("database: %s", id)
        database_name = utils.get_folder_name(path)
        table_path = os.path.join(path, f"{database_name}.csv")
        table = utils.fetch_table(table_path)
        updated_table = utils.remove_record_by_id(table,id)
        model.records.overwrite_records(table_path,updated_table)
        logging.info(f"database: Delete Record with Id {id}")
        return id


    def update_record(self, path,updated_record):
        """Updates the record."""
        logging.info("database: Update Record")
        logging.debug("database: %s", path)
        logging.debug("database: %s", updated_record)
        database_name = utils.get_folder_name(path)
        table_path = os.path.join(path, f"{database_name}.csv")
        table = utils.fetch_table(table_path)
        updated_table = utils.replace_record_in_table(table,updated_record)
        model.records.overwrite_records(table_path,updated_table)
        logging.info(f"database: Create Record with Id {updated_record['id']}")
        logging.debug(f"database: {updated_record}")
        return updated_record


    def create_functions_py(self):
        pass


