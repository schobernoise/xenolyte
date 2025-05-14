import model, utils
import os
import logging
from datetime import date
import shutil

today = date.today()

def create_new_table(path,name):
    new_table_path = os.path.join(path,f"{name}.csv")
    utils.create_empty_table(new_table_path)
    logging.info("database: created new table")


def create_new_database(path,name,args=False):
    new_database_path = os.path.join(path,f"{name}")
    utils.create_empty_folder(new_database_path)
    utils.create_config_json(path)

    new_foldernote_path = os.path.join(new_database_path,f"README.md")
    utils.create_note(new_foldernote_path)

    logging.info("database: created new database")
    return new_database_path
    

def create_database_from_table(path, create_record_folders=False):
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
    record = get_record(path,id)
    return utils.create_record_folder(path,record)


def load_table(path):
    return {
        "_type": "table",
        "table": utils.fetch_table(path)
    }


def load_database(path):
    database_name = utils.get_folder_name(path)
    table_path = os.path.join(path, f"{database_name}.csv")
    table = utils.fetch_table(table_path)
    config = utils.get_config_json(path)
    return {
        "_type": "database",
        "table": table,
        "config": config
    }


def get_record(path, id):
    database_name = utils.get_folder_name(path)
    table_path = os.path.join(path, f"{database_name}.csv")
    table = utils.fetch_table(table_path)
    logging.info(f"database: Returning Record with Id {id}")
    return utils.fetch_record(table,id)


def create_record(path, record,id=False):
    database_name = utils.get_folder_name(path)
    table_path = os.path.join(path, f"{database_name}.csv")
    model.records.create_record(table_path,record)
    logging.info(f"database: Create Record with Id {record['id']}")
    return record


def delete_record(path,id):
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
    return updated_record


def create_functions_py():
    pass



