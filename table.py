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
            self.intialize_table()
        self.records = utils.read_csv(self.table_path)
        self._type = "table"
        self.fieldnames = utils.get_fieldnames_from_file(self.table_path)
        self.__str__ = self.name

    
    def reflect_changes(self):
        logging.info("Reflect changes...")
        self.write_table_csv()
        utils.write_csv(self.table_path,self.records,self.fieldnames)


    def intialize_table(self):
        pass


    def fetch_records(self):
        return self.records


    def fetch_record(self,id):
        for record in self.records:
            if record["id"] == id:
                return record
    

    def create_record(self,new_record):
        # TODO: Create Function for ID-Handling
        # TODO: Index Argument for inserting inbetween
        self.records.append(new_record)
        self.reflect_changes()


    def delete_record(self,id):
        """Deletes Record from Table."""
        for record in self.records:
            if record.id == id:
                self.records.remove(record)
                self.reflect_changes()
                logging.info("Deleted Record", id)
                return record
        
    
    def update_record(self, updated_record):
        """Updates a record."""
        for i, record in enumerate(self.records):
            if record.id == updated_record.id:
                self.records[i] = updated_record
                self.reflect_changes()
                logging.info("Updated Record", record.id)
                return record
    



