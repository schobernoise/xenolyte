import model
import logging
import utils
from datetime import datetime

VAULTS = "data/vaults.csv"

XENOLYTE_CONFIG_TEMPLATE = {
    theme: "default",
    default_column_width: 20
}

def return_recent_vault():
    """Checks vaults.csv and returns most recent (active) vault. If empty, return False."""
    vaults = model.records.read_records(VAULTS)
    if vaults:
        return max(vaults, key=lambda obj: obj.modified)


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
    #  TODO: Check if already is vault
    append_vault()
    create_xenolyte_json(path)

    # if it is: update vaults.csv and select it as active



def set_vault_modified_now(path):
    vaults = model.records.read_records(VAULTS)
    updated_vaults = vaults.copy()
    for vault in updated_vaults:
            if vault["path"] == path:
                vault["modified"] = datetime.now()
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


def delete_vault_from_vaults(index):
    vaults = model.records.read_records(VAULTS)
    updated_vaults = vaults.copy()
    del updated_vaults[index]
    model.records.overwrite_records(VAULTS,updated_vaults)
    return updated_vaults


def create_xenolyte_json(path):
    pass


def read_xenolyte_json():
    pass


def update_xenolyte_json():
    pass