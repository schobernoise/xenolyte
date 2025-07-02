import argparse
import logging
from controller import xenolyte,database,utils
from _version import __version__
from datetime import datetime

# TODO Create CLI Class with parent cli-method
# All cli methods derive from it
# Logging,


# def backup_vault(args):
    # Get backup location from config
    # Overwrite 
    # ? Comes with Version 2.0
#     logging.debug(f"cli: {args}")
#     pass

# def backup_table(args):
    # Get backup location from config
    # Overwrite 
    # ? Comes with Version 2.0
#     logging.debug(f"cli: {args}")
#     pass


def list_vaults(args=False):
    """
    Retrieves and displays a list of vaults with their paths and modification times.
    """
    logging.debug(f"cli: {args}")
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


def add_folder(args):
    logging.debug(f"cli: {args}")
    path = input("Enter existing folder path: ")
    xenolyte.append_vault(path)
    list_vaults()


def select_vault(args):
    logging.debug(f"cli: {args}")
    print("Type in the number of the vault you want to select.")
    list_vaults()
    select_vault = input("Select Vault: ")
    select_vault_path = xenolyte.return_all_vaults()[int(select_vault)]["path"]
    # TODO: Error handling for user input
    if xenolyte.set_vault_modified_now(select_vault_path):
        print(f"Selected Vault {select_vault_path}")
    else:
        print("Error selecting Vault")


def show_selected_vault(args):
    logging.debug(f"cli: {args}")
    active_vault = xenolyte.return_recent_vault()
    print(f"{active_vault["path"]}")


def show_vault_config(args):
    logging.debug(f"cli: {args}")
    print(xenolyte.read_xenolyte_json(xenolyte.return_recent_vault()["path"]))


def list_tables(args):
    logging.debug(f"cli: {args}")
    active_vault = xenolyte.return_recent_vault()
    for table in database.get_all_tables(active_vault["path"]):
        print(table["name"]) 


def show_table_config(args):
    logging.debug(f"cli: {args}")
    print(utils.get_config_json(database.get_table_from_name(args.table)))


def show_table_readme(args):
    logging.debug(f"cli: {args}")
    pass


def show_vault_readme(args):
    logging.debug(f"cli: {args}")
    pass


def delete_table(args):
    logging.debug(f"cli: {args}")
    # TODO args.table - delete table
    # TODO Confirm before delete - show data sample
    pass


def create_record(args):
    logging.debug(f"cli: {args}")
    # TODO args.table - read headers - iterate through them
    # TODO Get Types form config.json, show near input
    table_name = args.table
    active_vault = xenolyte.return_recent_vault()
    table = database.get_table_from_name(path=active_vault["path"],name=table_name)
    new_record = utils.create_wizard(table.records[0].keys())
    database.create_record_in_table(table_name,new_record,id=int(table.records[:1]["id"])+1)

    


def update_record(args):
    logging.debug(f"cli: {args}")
    table_name = args.table
    record_id = args.record_id
    table = database.get_table_from_name(path=active_vault["path"],name=table_name)
    record = database.get_record_from_table(table, record_id)
    # TODO args.table, args.id - get record - iterate through it
    # TODO Make modified copy - overwrite old record


def delete_record(args):
    logging.debug(f"cli: {args}")
    table_name = args.table
    record_id = args.record_id
    table = database.get_table_from_name(path=active_vault["path"],name=table_name)
    database.delete_record
    pass


def show_record(args):
    """
    Show a specific record by id in a specific table.
    """
    logging.debug(f"cli: {args}")
    table_name = args.table
    active_vault = xenolyte.return_recent_vault()
    table = database.get_table_from_name(path=active_vault["path"],name=table_name)
    record_id = args.record_id
    record = database.get_record_from_table(table, record_id)
    print(utils.object_to_table(record))


def list_records(args):
    """
    List all records in a specific table.
    """
    logging.debug(f"cli: {args}")
    active_vault = xenolyte.return_recent_vault()
    table_name = args.table
    table = database.get_table_from_name(path=active_vault["path"],name=table_name)
    print(utils.dicts_to_table(table["records"]))


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


DATABASE_COMMANDS = [
    {
        "name": "listtables",
        "help": "List all records in a table",
        "func": list_tables,
        "arguments": []
    },
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
        "name": "deletetable",
        "help": "Delete Table.",
        "func": delete_table,
        "arguments": [
            {
                "name": "table",
                "type": str,
                "help": "The name of the table to delete"
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
    },
    {
        "name": "deleterecord",
        "help": "Delete a specific record by ID in a table",
        "func": delete_record,
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
    },
    {
        "name": "createrecord",
        "help": "Create a new Record in a specific table",
        "func": create_record,
        "arguments": [
            {
                "name": "table",
                "type": str,
                "help": "The name of the table to create the record in."
            }
        ]
    },
    {
        "name": "updaterecord",
        "help": "Update an existing Record in a specific table",
        "func": update_record,
        "arguments": [
            {
                "name": "table",
                "type": str,
                "help": "The name of the table to create the record in."
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
parser.add_argument('-v', '--verbose', action='count', default=0, help='Increase verbosity (use -vvv for debug)')

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

if args.verbose >= 3:
    loglevel = logging.DEBUG
elif args.verbose == 2:
    loglevel = logging.INFO
elif args.verbose == 1:
    loglevel = logging.WARNING
else:
    loglevel = logging.ERROR

logging.basicConfig(level=loglevel, format='%(levelname)s: %(message)s')

args.func(args=args)