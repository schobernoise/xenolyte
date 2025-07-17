import argparse
import os
import logging
from xenolyte import Xenolyte
from _version import __version__
from datetime import datetime
import utils


def initialize_xenolyte(args):
    print("Welcome to XENOLYTE.")
    if not os.path.exists("./data/vaults.csv"):
        first_vault_path = input("Please provide your first Vault path: ")
        _xeno = Xenolyte(first_vault_path=first_vault_path)


def list_vaults(args):
    _xeno = Xenolyte()
    vaults = _xeno.fetch_all_vaults()
    for vault in vaults:
        print(vault.name)


def add_existing_folder(args):
    _xeno = Xenolyte()
    logging.debug(f"{args}")
    path = input("Enter existing vault path: ")
    _xeno.add_exisiting_vault(path)
    list_vaults(args)


def create_vault(args):
    _xeno = Xenolyte()
    logging.debug(f"{args}")
    path = input("Enter new vault path: ")
    _xeno.create_new_vault(path)
    list_vaults(args)


def select_vault(args):
    logging.debug(f"{args}")
    _xeno = Xenolyte()
    print("Type in the number of the vault you want to select.")
    list_vaults()
    vaults = _xeno.fetch_all_vaults()
    select_vault = input("Select Vault: ")
    vaults[select_vault].set_vault_modified_now()


def show_selected_vault(args):
    logging.debug(f"{args}")
    _xeno = Xenolyte()
    active_vault = _xeno.fetch_recent_vault()
    print(active_vault.name)


def show_vault_config(args):
    logging.debug(f"{args}")
    _xeno = Xenolyte()
    active_vault = _xeno.fetch_recent_vault()
    print(active_vault.fetch_vault_config())


def list_tables(args):
    _xeno = Xenolyte()
    logging.debug(f"{args}")
    active_vault = _xeno.fetch_recent_vault()
    for container in active_vault.containers:
        print(container.name) 


def delete_table(args):
    logging.debug(f"{args}")
    _xeno = Xenolyte()
    active_vault = _xeno.fetch_recent_vault()
    table = active_vault.get_container_from_name(args.table)
    if table:
        print(f"Deleting Container {args.table}!")
        print("Data Sample:")
        print(utils.object_to_table(table.records[0:5]))
        choice = input("Are you sure? (y/n)" )
        if choice == "y":
            active_vault.delete_container(args.table)
            return 1
        elif choice == "n":
            print("Cancelled Delete.")
            return 0
        else:
            print("Please provide a valid input (y/n).")
            return 0



def create_table(args):
    logging.debug(f"{args}")
    _xeno = Xenolyte()
    active_vault = _xeno.fetch_recent_vault()
    if not args.table:
        table_name = input("Provide name of new Table: ")
    else:
        table_name = args.table
    active_vault.create_new_table(table_name)


def create_database(args):
    logging.debug(f"{args}")
    _xeno = Xenolyte()
    active_vault = _xeno.fetch_recent_vault()
    if not args.table:
        table_name = input("Provide name of new Database: ")
    else:
        table_name = args.table
    active_vault.create_new_database(table_name)


def convert_table_to_database(args):
    logging.debug(f"{args}")
    _xeno = Xenolyte()
    active_vault = _xeno.fetch_recent_vault()
    active_vault.create_database_from_table(args.table)


def create_record(args):
    _xeno = Xenolyte()
    logging.debug(f"{args}")
    active_vault = _xeno.fetch_recent_vault()
    container = active_vault.get_container_from_name(args.table)
    columns = []
    if container._type == "database":
        columns = container.config["columns"]
    new_record = utils.create_wizard(container.fieldnames, columns=columns)
    container.create_record(new_record)


def create_column(args):
    _xeno = Xenolyte()
    logging.debug(f"{args}")
    if not args.name:
        print("Please provide a Column name.")
        return 0
    active_vault = _xeno.fetch_recent_vault()
    container = active_vault.get_container_from_name(args.table)
    if container._type == "table":
        container.create_column(args.name)
    elif container._type == "database":
        _type = args._type
        width = args.width
        if not args._type:
            _type = "str"
        if not args.width:
            width = 20
        container.create_column(args.name, _type=_type, width=width)


def update_record(args):
    _xeno = Xenolyte()
    active_vault = _xeno.fetch_recent_vault()
    table = active_vault.get_container_from_name(args.table)
    record = table.fetch_record(args.record_id)
    logging.debug(f"{args}")
    logging.debug(f"{record}")
    if not record:
        logging.error(f"Record Id {args.record_id} not found.")
        return
    updated_record = utils.update_wizard(record)
    table.update_record(updated_record)


def delete_record(args):
    logging.debug(f"{args}")
    _xeno = Xenolyte()
    active_vault = _xeno.fetch_recent_vault()
    container = active_vault.get_container_from_name(args.table)
    container.delete_record(args.record_id)


def show_record(args):
    _xeno = Xenolyte()
    logging.debug(f"{args}")
    active_vault = _xeno.fetch_recent_vault()
    table = active_vault.get_container_from_name(args.table)
    record = table.fetch_record(args.record_id)
    print(utils.object_to_table(record))


def list_records(args):
    _xeno = Xenolyte()
    logging.debug(f"{args}")
    active_vault = _xeno.fetch_recent_vault()
    table = active_vault.get_container_from_name(args.table)
    if table:
        print(utils.dicts_to_table(table.records))
    else:
        print("No Records found")


def show_vault_readme(args):
    logging.debug(f"{args}")
    _xeno = Xenolyte()
    active_vault = _xeno.fetch_recent_vault()
    print(active_vault.fetch_vault_note())


def forget_vault(args):
    logging.debug(f"{args}")
    _xeno = Xenolyte()
    _xeno.forget_vault(args.vault)
    print(f"Forgetting Vault {args.vault}")


def call_function(args):
    logging.debug(f"{args}")
    _xeno = Xenolyte()
    active_vault = _xeno.fetch_recent_vault()
    table = active_vault.get_container_from_name(args.table)
    if table._type == "database":
        table.call_function(args.function)
    else:
        print(f"{table.name} is not a database, functions are only available in databases.")
        return 0



# def show_database_config(args):
#     _xeno = Xenolyte()
#     active_vault = _xeno.fetch_recent_vault()
#     active_vault.get_container_from_name(args.table)
#     logging.debug(f"{args}")
#     print(_xeno)


# def show_database_readme(args):
#     _xeno = Xenolyte()
#     logging.debug(f"{args}")
#     pass


# def backup_vault(args):
    # Get backup location from config
    # Overwrite 
    # ? Comes with Version 2.0
#     logging.debug(f"{args}")
#     pass


# def backup_table(args):
    # Get backup location from config
    # Overwrite 
    # ? Comes with Version 2.0
#     logging.debug(f"{args}")
#     pass


VAULT_COMMANDS = [
    {
        "name": "list",
        "help": "List all currently selected vaults",
        "func": list_vaults,
        "arguments": []  
    },
    {
        "name": "create",
        "help": "Create a new Vault Folder.",
        "func": create_vault,
        "arguments": [] 
    },
    {
        "name": "add",
        "help": "Add an existing folder as vault",
        "func": add_existing_folder,
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
    },
    {
        "name": "show_readme",
        "help": "Display Readme of the currently selected vault.",
        "func": show_vault_readme,
        "arguments": []  
    },
    {
        "name": "forget",
        "help": "Forget vault by name.",
        "func": forget_vault,
        "arguments": [
            {
                "name": "vault",
                "type": str,
                "help": "The name of the vault to forget."
            }
        ]  
    }
]


DATABASE_COMMANDS = [
    {
        "name": "fn",
        "help": "Calls a function form functions.py.",
        "func": call_function,
        "arguments": [
            {
                "name": "table",
                "type": str,
                "help": "The name of the table to list records from"
            },
            {
                "name": "function",
                "type": str,
                "help": "The name of the function to call form functions.py."
            }
        ]
    },
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
        "name": "createcolumn",
        "help": "Create a new Column in a specific table",
        "func": create_column,
        "arguments": [
            {
                "name": "table",
                "type": str,
                "help": "The name of the table to create the record in."
            },
            {
                "name": "name",
                "type": str,
                "help": "The name of the column to be created."
            },
            {
                "name": "_type",
                "type": str,
                "help": "The type of the column to be created."
            },
            {
                "name": "width",
                "type": str,
                "help": "The default width of the column in PyQt."
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
    },
    {
        "name": "createtable",
        "help": "Create a new Table in the active Vault.",
        "func": create_table,
        "arguments": [
            {
                "name": "table",
                "type": str,
                "help": "The name of the table that is going to be created."
            }
        ]
    },
     {
        "name": "createdatabase",
        "help": "Create a new Database in the active Vault.",
        "func": create_database,
        "arguments": [
            {
                "name": "table",
                "type": str,
                "help": "The name of the database that is going to be created."
            }
        ]
    },
     {
        "name": "converttabletodb",
        "help": "Convert an existing Table to a Database.",
        "func": convert_table_to_database,
        "arguments": [
            {
                "name": "table",
                "type": str,
                "help": "The name of the Table that is going to be used."
            }
        ]
    }
]

XENOLYTE_COMMANDS = [
    {
        "name": "init",
        "help": "Initialize Xenolyte for first time use.",
        "func": initialize_xenolyte,
        "arguments": []
    }
]


def main():

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
    
    xenolyte_parser = subparsers.add_parser('xenolyte', help='Xenolyte management commands')
    xenolyte_subparsers = xenolyte_parser.add_subparsers(title='Xenolyte Subcommands', dest='db_command', required=True)

    for cmd in XENOLYTE_COMMANDS:
        subparser = xenolyte_subparsers.add_parser(cmd["name"], help=cmd["help"])
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

    logging.basicConfig(level=loglevel, format='%(levelname)s | %(filename)s | %(funcName)s | %(message)s')

    args.func(args=args)


if __name__ == "__main__":
    main()