from controller import utils
import model
import os
import logging
from datetime import date
import shutil

today = date.today()


def get_all_tables(path):
    logging.debug("database: Get all Tables")
    objects=[]
    try:
        items = os.listdir(path)
    except Exception as e:
        logging.error(f"Error reading directory {path}: {e}")
        return objects

    for item in items:
        item_path = os.path.join(path, item)
        logging.debug("database: %s", item_path)
        if os.path.isfile(item_path) and item.lower().endswith('.csv'):
            obj = {
                "_type": "table",
                "name": utils.get_folder_name(item_path.replace(".csv",""))[1],
                "records": utils.fetch_table(item_path)
            }
            objects.append(obj)
        elif os.path.isdir(item_path):
            table_path = os.path.join(item_path, f"{item}.csv")
            # print(table_path)
            if os.path.isfile(table_path):
                obj = {
                    "_type": "database",
                    "name": utils.get_folder_name(table_path.replace(".csv",""))[1],
                    "records": utils.fetch_table(table_path),
                    "config": utils.get_config_json(item_path)
                }
                objects.append(obj)
    return objects



def get_table_from_name(path, name):
    logging.debug("database: Get Table from Name")
    tables = get_all_tables(path)
    for table in tables:
        if table["name"] == name:
            return table
    return False


def create_new_table(path,name):
    logging.debug("database: Create New Table")
    new_table_path = os.path.join(path,f"{name}.csv")
    utils.create_empty_table(new_table_path)
    logging.info("database: created new table")


def create_new_database(path,name,args=False):
    logging.debug("database: Create New Database")
    new_database_path = os.path.join(path,f"{name}")
    utils.create_empty_folder(new_database_path)
    utils.create_config_json(path)

    new_foldernote_path = os.path.join(new_database_path,f"README.md")
    utils.create_note(new_foldernote_path)

    logging.info("database: created new database")
    return new_database_path
    

def create_database_from_table(path, create_record_folders=False):
    logging.debug("database: Create Database from Table")
    database_path = utils.create_empty_folder(path.replace(".csv",""))
    shutil.move(path, database_path)
    utils.create_config_json(database_path)

    new_foldernote_path = os.path.join(database_path,f"README.md")
    utils.create_note(new_foldernote_path)

    if create_record_folders:
        records = model.records.read_records(path)
        for record in records:
            utils.create_record_folder(database_path,record)

    logging.info("database: created database from table")
    return database_path


def create_record_folder(path, id):
    logging.debug("database: create Record Folder")
    record = get_record(path,id)
    return utils.create_record_folder(path,record)


def load_table(path):
    logging.debug("database: Load Table")
    return {
        "_type": "table",
        "name": utils.get_folder_name(path.replace(".csv",""))[1],
        "records": utils.fetch_table(path)
    }


def load_database(path):
    logging.debug("database: Load Database")
    database_name = utils.get_folder_name(path)[1]
    table_path = os.path.join(path, f"{database_name}.csv")
    table = utils.fetch_table(table_path)
    config = utils.get_config_json(path)
    return {
        "_type": "database",
        "name": database_name,
        "records": table,
        "config": config
    }


def get_record(path, id):
    # ! DEPRECATED: will be removed
    logging.debug("database: Get Record - Deprecated")
    database_name = utils.get_folder_name(path)
    table_path = os.path.join(path, f"{database_name}.csv")
    table = utils.fetch_table(table_path)
    logging.info(f"database: Returning Record with Id {id}")
    return utils.fetch_record(table,id)



def get_record_from_table(table, id):
    logging.debug("database: Get Record from Table")
    logging.debug("database: %s", table)
    logging.debug("database: %s", id)
    for record in table["records"]:
        if record["id"] == id:
            return record
    return False


def create_record(path, record,id=False):
    logging.debug("database: Create Record")
    logging.debug("database",path,record,id)
    database_name = utils.get_folder_name(path)
    table_path = os.path.join(path, f"{database_name}.csv")
    model.records.create_record(table_path,record)
    logging.info(f"database: Create Record with Id {record['id']}")
    return record


def delete_record(path,id):
    logging.debug("database: Delete Record")
    logging.debug("database: path,id")
    database_name = utils.get_folder_name(path)
    table_path = os.path.join(path, f"{database_name}.csv")
    table = utils.fetch_table(table_path)
    updated_table = utils.remove_record_by_id(table,id)
    model.records.overwrite_records(table_path,updated_table)
    logging.info(f"database: Delete Record with Id {id}")
    return id


def update_record(path,updated_record):
    database_name = utils.get_folder_name(path)
    table_path = os.path.join(path, f"{database_name}.csv")
    table = utils.fetch_table(table_path)
    updated_table = utils.replace_record_in_table(table,updated_record)
    model.records.overwrite_records(table_path,updated_table)
    logging.info(f"database: Create Record with Id {updated_record['id']}")
    logging.debug(f"database: {updated_record}")
    return updated_record


def create_functions_py():
    pass


def delete_table(path):
    pass