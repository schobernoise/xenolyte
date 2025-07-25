import os
import csv
import json
import logging
import pathlib
import uuid


# SIMPLE_TYPES = ["int","float","bool","str"]


def get_folder_name(path):
    logging.info(f"Get Folder Name: {path}")
    if os.path.isfile(path):
        path = os.path.dirname(path)
    return os.path.basename(os.path.normpath(path))


def create_empty_folder(path):
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)


def simple_type_check(value,_type):
    if _type == "int":
        try:
            value = int(value)
        except:
            print("Please provide int.")
            return False
    elif _type == "float":
        try:
            value = float(value)
        except:
            print("Please provide float.")
            return False
    elif _type == "bool":
        try:
            value = bool(value)
        except:
            print("Please provide bool.")
            return False
    else:
        try:
            value = str(value)
        except:
            print("Can't create string.")
            return False
    return value


def create_wizard(keys, columns=False):
    logging.debug(f"{keys}")
    logging.debug(f"{columns}")
    print("##### CREATE WIZARD #####")
    new_record = {}
    logging.debug(f"while start")
    for key in keys:
        if 'id' == key.lower():
            continue
        done = False
        while not done:
            _type = "str" # Fallback
            if columns:
                for column in columns:
                    if column["name"] == key:
                        _type = column["_type"]
            value = input(f"Enter value for '{key}' ({_type}): ")
            value = simple_type_check(value,_type)
            if not value:
                break
            done = True
            new_record[key] = value                
    return new_record


def update_wizard(record):
    print("##### UPDATE WIZARD #####")
    new_record = {}
    for key in record.keys():
        if 'id' == key.lower():
            new_record["id"] = record["id"]
            continue
        print(record[key])
        new_record[key] = input(f"Enter value for '{key}': ") or record[key]
    return new_record


def get_fieldnames_from_file(path):
    logging.debug("Get Fieldnames from File")
    logging.debug(path)
    with open(path, 'r', encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")
        fieldnames = reader.fieldnames
    return fieldnames


def read_csv(file):
    """Return all rows of a csv file."""
    with open(file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=";")
        logging.info("Reading CSV.")
        return list(reader)


def read_json(file):
    with open(file, 'r') as f:
            content = json.load(f)
            return content


def write_json(file,content):
    logging.debug(f"{content}")
    with open(file , "w") as f:
        json.dump(content, f, indent=4)
    logging.info(f"Written {file }")


def write_csv(file,records,fieldnames):
    logging.debug(f"{file}")
    logging.debug(f"{records}")
    logging.debug(f"{fieldnames}")
    with open(file, 'w', encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";", extrasaction='ignore')
        writer.writeheader()
        logging.debug("CSV header written.")
        writer.writerows(records)


# TODO: Those two Table printing functions
# are still from the AI.
# Need to refactor them.

def dict_to_table(obj, indent=0):
    if isinstance(obj, dict):
        properties = obj.keys()
        values = obj.values()
    else:
        properties = [prop for prop in dir(obj) if not prop.startswith('__')]
        values = [getattr(obj, prop) for prop in properties]
    
    max_prop_length = max(len(prop) for prop in properties)
    
    table = ''
    for prop, val in zip(properties, values):
        if callable(val):
            val_str = f'<function {val.__name__}>'
        elif isinstance(val, dict) or hasattr(val, '__dict__'):
            val_str = '\n' + dict_to_table(val, indent + 2)
        else:
            val_str = str(val)
        
        table += f'{" " * indent}{prop:<{max_prop_length}} | {val_str}\n'
    
    return table


def dicts_to_table(dicts):
    if not dicts:
        return ''

    headers = list(dicts[0].keys())
    max_lengths = [max(len(str(d[key])) for d in dicts) for key in headers]

    table = ''

    for header, max_length in zip(headers, max_lengths):
        table += f'{header:<{max_length}} | '
    table = table.rstrip(' | ') + '\n'

    for max_length in max_lengths:
        table += f'{"-" * max_length} | '
    table = table.rstrip(' | ') + '\n'

    for d in dicts:
        for header, max_length in zip(headers, max_lengths):
            table += f'{str(d[header]):<{max_length}} | '
        table = table.rstrip(' | ') + '\n'

    return table


def generate_uuid():
    return uuid.uuid4().hex


def write_markdown(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)


def read_markdown(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def write_code(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)