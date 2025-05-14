import argparse
import logging
from controller import xenolyte
from _version import __version__
from datetime import datetime



def list_vaults(args=False):
    """
    Retrieves and displays a list of vaults with their paths and modification times.
    """
    try:
        vaults: List[Dict[str, str]] = xenolyte.return_all_vaults()
    except Exception as e:
        print(f"Error retrieving vaults: {e}")
        return

    if not vaults:
        print("No vaults available.")
        return

    table_data = []
    for index, vault in enumerate(vaults, start=0):
        path = vault.get('path', 'N/A')
        modified_raw = vault.get('modified', '')
        try:
            modified_dt = datetime.fromisoformat(modified_raw)
            modified = modified_dt.strftime('%Y-%m-%d %H:%M:%S')
        except ValueError:
            modified = modified_raw  

        table_data.append([index, path, modified])

    headers = ["#", "Path", "Modified"]

    col_widths = [max(len(str(row[i])) for row in table_data + [headers]) for i in range(3)]

    row_format = ("| {:<" + str(col_widths[0]) + "} "
                    "| {:<" + str(col_widths[1]) + "} "
                    "| {:<" + str(col_widths[2]) + "} |")

    print(row_format.format(*headers))
    print("-" * (sum(col_widths) + 10))  

    for row in table_data:
        print(row_format.format(*row))


def add_folder(args=False):
    path = input("Enter existing folder path: ")
    xenolyte.append_vault(path)
    list_vaults()

def select_vault(args=False):
    print("Type in the number of the vault you want to select.")
    list_vaults()
    select_vault = input("Select Vault: ")
    select_vault_path = xenolyte.return_all_vaults()[int(select_vault)]["path"]
    # TODO: Error handling for user input
    if xenolyte.set_vault_modified_now(select_vault_path):
        print(f"Selected Vault {select_vault_path}")
    else:
        print("Error selecting Vault")

def show_selected_vault(args=False):
    active_vault = xenolyte.return_recent_vault()
    print(f"{active_vault["path"]}")


FUNCTIONS = [
    # Vault Functions
    ["listvaults", "List all currently selected vaults", list_vaults],
    ["addfolder", "Add an existing folder as vault, [path]", add_folder],
    ["selectvault", "Select a vault from List of Vaults, [id]", select_vault],
    ["showselectedvault", "Display currently selected vault",show_selected_vault],

    # Database functions
    # ["createtable", ""],
    # ["createdatabase", ""],
    # ["createrecordfolder", ""],
    # ["createrecord", ""],

]

parser = argparse.ArgumentParser(prog='cli', description='Xenolyte Vault Management CLI')
subparsers = parser.add_subparsers(title='Commands', dest='command', required=True)

for func in FUNCTIONS:
    cmd_name, help_text, func_ref = func
    subparser = subparsers.add_parser(cmd_name, help=help_text)
    
    # if cmd_name == "addfolder":
    #     subparser.add_argument('path', type=str, help='Path to the folder to add as vault')
    # elif cmd_name == "selectvault":
    #     subparser.add_argument('id', type=int, help='ID of the vault to select')

    # db: database to perform action on

    # Associate the function with the subparser
    subparser.set_defaults(func=func_ref)

args = parser.parse_args()

# Call the associated function with parsed arguments
args.func(args=args)

