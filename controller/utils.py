from model import records
import os
import json
import logging


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


def get_folder_name(path):
    logging.debug("utils: Get Folder Name")
    return os.path.split(os.path.normpath(path))


def create_empty_table(path, header=["id"]):
    if os.path.exists(path):
        logging.error("File already exists")
        raise FileExistsError(f"{path} already exists.")
    else:
        with open(path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            if header:
                writer.writerow(header)
        logging.info(f"Created {path}")
        return path


def create_empty_folder(path):
    pass


def create_note(path):
    with open(path, 'w') as f:
        f.write()
    logging.info(f"Created {path}")
    return path


def create_config_json(path):
    new_config_path = os.path.join(path,"config.json")
    with open(new_config_path , "w") as f:
        json.dump(CONFIG_TEMPLATE, f, indent=4)
    logging.info(f"Created {new_config_path }")
    return new_config_path 


def get_config_json(path):
    logging.debug("utils: Get Config Json")
    logging.debug("utils: %s", path)
    config_path = os.path.join(path,"config.json")
    logging.debug("utils: Config Path %s", config_path)

    if os.path.isfile(config_path) and config_path.lower().endswith('.json'):
        with open(config_path, 'r') as f:
            config = json.load(f)
            logging.debug("utils: Config existing %s", config)
            return config
    else:
        logging.debug("utils: Config missing, creating")
        new_config_path = create_config_json(path)
        with open(new_config_path, 'r') as f:
            return json.load(f)



def update_config_json(path, updated_config):
    config_path = os.path.join(path,"config.json")
    try:
        config_json = json.dumps(updated_config, indent=4)

        with tempfile.NamedTemporaryFile('w', delete=False, dir=config_path.parent, encoding='utf-8') as tmp_file:
            tmp_file.write(config_json)
            temp_path = Path(tmp_file.name)

        config_path.replace(temp_path)

        print(f"{config_path} has been atomically updated.")
        return True

    except Exception as e:
        print(f"An error occurred during atomic update: {e}")
        return False


def create_record_folder(path, record):
    """path: Path to the database"""
    folder_name = f"{record['id']} {record['slug']}".strip().replace("/", "-")
    record_folder_path = os.path.join(path, folder_name)

    attachments_path = os.path.join(record_folder_path, "attachments")
    markdown_file_path = os.path.join(record_folder_path, f"{folder_name}.md")

    os.makedirs(attachments_path, exist_ok=True)

    if not os.path.exists(markdown_file_path):
        with open(markdown_file_path, "w") as f:
            f.write(f"# {record['title']}\n")

    return record_folder_path


def get_record_folder(path,record):
    return f"{record['id']} {record['slug']}".strip().replace("/", "-")



def read_markdown(file_path):
    """
    Reads a Markdown file and returns its content as a string.
    """
    try:
        logging.debug("Attempting to read the Markdown file: %s", file_path)
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        logging.info("Successfully read the file: %s", file_path)
        return content
    except FileNotFoundError:
        logging.error("The file '%s' does not exist.", file_path)
        raise
    except IOError as e:
        logging.error("An I/O error occurred while reading '%s': %s", file_path, e)
        raise
    except UnicodeDecodeError as e:
        logging.error("Encoding error while reading '%s': %s", file_path, e)
        raise


def fetch_table(path):
    return records.read_records(path)


def fetch_record(table,id):
    for record in table:
            if record["id"] == id:
                return record


def replace_record_in_table(table,updated_record):
    updated_table = table.copy()
    for index, record in enumerate(updated_table):
        if getattr(record, "id", None) == getattr(updated_record, "id", None):
            updated_table[index] = updated_record
            break
    else:
        updated_table.append(updated_record)
    return updated_table



def remove_record_by_id(table, id_to_remove):
    return [record for record in table if getattr(record, "id", None) != id_to_remove]