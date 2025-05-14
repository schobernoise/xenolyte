import argparse
import logging
from controller import xenolyte,database
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




def show_record(args):
    """
    Show a specific record by id in a specific table.
    """
    table_name = args.table
    record_id = args.record_id

    # try:
    #     record = xenolyte.get_record(table_name, record_id)
    #     if record:
    #         print(f"Record {record_id} in table {table_name}: {record}")
    #     else:
    #         print(f"Record {record_id} not found in table {table_name}.")
    # except Exception as e:
    #     print(f"Error retrieving record: {e}")


def list_records(args):
    """
    List all records in a specific table.
    """
    table_name = args.table
    # try:
    #     records = xenolyte.list_records(table_name)
    #     if records:
    #         print(f"Records in table {table_name}:")
    #         for record in records:
    #             print(record)
    #     else:
    #         print(f"No records found in table {table_name}.")
    # except Exception as e:
    #     print(f"Error listing records: {e}")


VAULT_COMMANDS = [
    {
        "name": "list",
        "help": "List all currently selected vaults",
        "func": list_vaults,
        "arguments": []  
    },
    {
        "name": "add",
        "help": "Add an existing folder as vault",
        "func": add_folder,
        "arguments": [] 
    },
    {
        "name": "select",
        "help": "Select a vault from list of vaults",
        "func": select_vault,
        "arguments": [] 
    },
    {
        "name": "show",
        "help": "Display currently selected vault",
        "func": show_selected_vault,
        "arguments": []  
    }
]

# Define database functions
# listtables
# deletetable
# createtable
# showreadme for table
# showreadme for record (combine?)

DATABASE_COMMANDS = [
    {
        "name": "listrecords",
        "help": "List all records in a table",
        "func": list_records,
        "arguments": [
            {
                "name": "table",
                "type": str,
                "help": "The name of the table to list records from"
            }
        ]
    },
    {
        "name": "showrecord",
        "help": "Show a specific record by ID in a table",
        "func": show_record,
        "arguments": [
            {
                "name": "table",
                "type": str,
                "help": "The name of the table to retrieve the record from"
            },
            {
                "name": "record_id",
                "type": str,
                "help": "The ID of the record to retrieve"
            }
        ]
    }
]

parser = argparse.ArgumentParser(prog='cli', description='Xenolyte Vault Management CLI')
subparsers = parser.add_subparsers(title='Commands', dest='command', required=True)

vault_parser = subparsers.add_parser('vault', help='Vault management commands')
vault_subparsers = vault_parser.add_subparsers(title='Vault Subcommands', dest='vault_command', required=True)

for cmd in VAULT_COMMANDS:
    subparser = vault_subparsers.add_parser(cmd["name"], help=cmd["help"])
    for arg in cmd["arguments"]:
        subparser.add_argument(arg["name"], type=arg["type"], help=arg["help"])
    subparser.set_defaults(func=cmd["func"])

database_parser = subparsers.add_parser('database', help='Database management commands')
database_subparsers = database_parser.add_subparsers(title='Database Subcommands', dest='db_command', required=True)

for cmd in DATABASE_COMMANDS:
    subparser = database_subparsers.add_parser(cmd["name"], help=cmd["help"])
    for arg in cmd["arguments"]:
        subparser.add_argument(arg["name"], type=arg["type"], help=arg["help"])
    subparser.set_defaults(func=cmd["func"])

args = parser.parse_args()
args.func(args=args)