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

# Let's say:
# For standard tables there are only integer-indexes and incremention 
# If you have a database you get e.g. uuid-indexes
# You can implement your own ID-creatio scheme anyways           
            
    def create_record(self,new_record,index=False,_id=False):
        """If you insert inbetween, you are getting uuid automatically,
        except when you provide a manual ID."""
        if index:
            if index < len(self.records):
                new_record["id"] = _id if _id else self.create_id(_type="uuid")
                self.records.insert(index,new_record)
            else:
                logging.error(f"Index Argument is too big.")
        else:
            new_record["id"] = _id if _id else self.create_id()
            self.records.append(new_record)
        self.reflect_changes()
    

    def create_id(self,_type="increment"):
        if _type == "increment":
            _id = str(int(self.records[-1]["id"]) + 1)
        elif _type == "uuid":
            _id = utils.generate_uuid()
        return _id


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
    



