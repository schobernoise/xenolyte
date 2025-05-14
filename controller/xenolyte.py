import model
import logging
from controller import utils
from datetime import datetime

VAULTS = "data/vaults.csv"

XENOLYTE_CONFIG_TEMPLATE = {
    "theme": "default",
    "default_column_width": 20
}

def return_recent_vault():
    """Checks vaults.csv and returns most recent (active) vault. If empty, return False."""
    vaults = model.records.read_records(VAULTS)
    if vaults:
        return max(vaults, key=lambda obj: obj["modified"])


def return_all_vaults():
    """Reads vaults.csv and returns a list of all vaults."""
    return model.records.read_records(VAULTS)


def append_vault(path):
    model.records.create_record(VAULTS,
        {path: path,
        modified: datetime.now()
        })
    return path


def create_vault(path):
    vaults = model.records.read_records(VAULTS)
    for vault in vaults:
        if vault["path"] == path:
            set_vault_modified_now(path)
            logging.info("Vault already in path, selecting it now.")
            return
    append_vault(path)
    create_xenolyte_json(path) # Also checks, if file aready exists.


def set_vault_modified_now(path):
    vaults = model.records.read_records(VAULTS)
    updated_vaults = vaults.copy()
    for vault in updated_vaults:
            if vault["path"] == path:
                vault["modified"] = datetime.now()
            else: 
                return False
    model.records.overwrite_records(VAULTS,updated_vaults)
    return updated_vaults



def create_vaults_csv():
    """
    Checks if the VAULTS file exists.
    If it exists, returns True.
    If not, creates the CSV file with headers 'path' and 'created' and returns False.
    
    Returns:
        bool: True if the file exists, False otherwise.
    """
    if VAULTS.exists():
        return model.records.read_records(VAULTS)
    else:
        # Create parent directories if they don't exist
        try:
            VAULTS.parent.mkdir(parents=True, exist_ok=True)
            logging.debug(f"Ensured directory exists: {VAULTS.parent}")
        except Exception as e:
            logging.debug(f"Error creating directories: {e}")
            return False
        
        # Create the CSV file with headers
        try:
            with VAULTS.open(mode='w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['path', 'created'])
            logging.debug(f"Created file with headers at: {VAULTS}")
            return False
        except IOError as e:
            logging.debug(f"Error creating file {VAULTS}: {e}")
            return False


def delete_vault_from_vaults(index: int):
    vaults = model.records.read_records(VAULTS)
    updated_vaults = vaults.copy()
    del updated_vaults[index]
    model.records.overwrite_records(VAULTS,updated_vaults)
    return updated_vaults


def create_xenolyte_json(path: str, overwrite: bool = False, backup: bool = False):
    """
    Creates a xenolyte.json configuration file in the specified directory.

    Args:
        path (str): The directory path where xenolyte.json will be created.
        overwrite (bool, optional): If True, overwrite the file if it exists. Defaults to False.
        backup (bool, optional): If True and overwrite is enabled, create a backup of the existing file. Defaults to False.
    """
    try:
        directory = Path(path)
        xenolyte_config = directory / "xenolyte.json"

        logging.debug(f"Attempting to create xenolyte.json at: {xenolyte_config}")

        if not directory.exists():
            logging.info(f"Directory {directory} does not exist. Creating it.")
            directory.mkdir(parents=True, exist_ok=True)

        if xenolyte_config.exists():
            if overwrite:
                if backup:
                    backup_path = xenolyte_config.with_suffix('.bak')
                    xenolyte_config.rename(backup_path)
                    logging.info(f"Existing file backed up to {backup_path}")
                logging.warning(f"File {xenolyte_config} already exists and will be overwritten.")
            else:
                logging.info(f"File {xenolyte_config} already exists. Skipping creation.")
                return None

        with xenolyte_config.open(mode="w", encoding="utf-8") as f:
            json.dump(XENOLYTE_CONFIG_TEMPLATE, f, indent=4)
        
        logging.info(f"Created {xenolyte_config}")
        return xenolyte_config

    except Exception as e:
        logging.error(f"Failed to create xenolyte.json in {path}: {e}")
        return None



def read_xenolyte_json(path):
    return json.load(os.path.join(path,"xenolyte.json"))


def update_xenolyte_json(path, updated_config):
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