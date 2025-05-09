import model

VAULTS = "data/vaults.csv"

def return_recent_vault():
    """Checks vaults.csv and returns most recent vault. If empty, return False."""
    vaults = model.records.read_records(VAULTS)
    if vaults:
        return max(vaults, key=lambda obj: obj.modified)


def return_all_vaults():
    """Reads vaults.csv and returns a list of all vaults."""
    return model.records.read_records(VAULTS)


def create_vaults_csv():
    pass


def delete_vault_from_vaults():
    pass