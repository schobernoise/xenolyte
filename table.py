import table
import utils
import os
import logging
from datetime import date
import shutil

today = date.today()

class Table:
    
    def __init__(self, path, init=False):
        logging.debug(f"Creating Table: {path}")
        self.table_path = path
        self.name = utils.get_folder_name(path)
        if init:
            self.records = [{"id": "0"}]
            self.intialize_table()
        self.records = utils.read_csv(self.table_path)
        self._type = "table"
        self.fieldnames = utils.get_fieldnames_from_file(self.table_path)
        self.__str__ = self.name
        

    def reflect_changes(self):
        logging.info("Reflect changes...")
        utils.write_csv(self.table_path,self.records,self.fieldnames)


    def intialize_table(self):
            if not os.path.exists(self.table_path):
                utils.write_csv(self.table_path,self.records,self.records[0].keys())
            # self.reflect_changes()


    def fetch_records(self):
        return self.records


    def fetch_record(self,id):
        for record in self.records:
            if record["id"] == id:
                return record


    def create_column(self,name):
        for fieldname in fieldnames:
            if name == fieldname:
                logging.error("Columns must have unique names.")
                return 0
        self.fieldnames.append(name)
        self.reflect_changes()
            
            
    def create_record(self,new_record):
        # TODO: Index Argument for inserting inbetween
        new_record["id"] = self.create_id()
        self.records.append(new_record)
        self.reflect_changes()
    

    def create_id(self,_type="increment"):
        return str(int(self.records[-1]["id"]) + 1)


    def delete_record(self,id):
        """Deletes Record from Table."""
        for record in self.records:
            if record["id"] == id:
                self.records.remove(record)
                self.reflect_changes()
                logging.info(f"Deleted Record {id}")
                return record
            return False
        
    
    def update_record(self, updated_record):
        """Updates a record."""
        for i, record in enumerate(self.records):
            if record["id"]== updated_record["id"]:
                self.records[i] = updated_record
                self.reflect_changes()
                logging.info(f"Updated Record {record["id"]}")
                return record
    



