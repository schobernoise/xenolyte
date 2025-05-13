from model import records
import os
import json


CONFIG_TEMPLATE = {
    columns: [
        {
            name: "id",
            _type: "int",
            width: 20
        }
    ]
}


def get_folder_name(path):
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
    return json.load(os.path.join(path,"config.json"))


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


def read_markdown(path):
    pass


def fetch_table(path):
    return records.read_records(table_path)


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