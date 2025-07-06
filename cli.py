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
    path = input("Enter existing folder path: ")
    _xeno.add_exisiting_vault(path)
    list_vaults()


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
    active_vault.delete_container(args.table)
    # TODO Confirm before delete - show data sample


def create_record(args):
    # TODO Get Types form config.json, show near input
    _xeno = Xenolyte()
    logging.debug(f"{args}")
    active_vault = _xeno.fetch_recent_vault()
    table = active_vault.get_container_from_name(args.table)
    new_record = utils.create_wizard(table.fieldnames)
    table.create_record(new_record)
    

def update_record(args):
    logging.debug(f"{args}")
    _xeno = Xenolyte()
    active_vault = _xeno.fetch_recent_vault()
    table = active_vault.get_container_from_name(args.table)
    record = table.fetch_record(args.record_id)
    updated_record = utils.update_wizard(record)
    table.update_record(updated_record)


def delete_record(args):
    logging.debug(f"{args}")
    _xeno = Xenolyte()
    table = active_vault.get_container_from_name(args.table)
    database.delete_record()


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
    print(active_vault.fetch_vault_config())


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

    logging.basicConfig(level=loglevel, format='%(levelname)s | %(funcName)s | %(message)s')

    args.func(args=args)


if __name__ == "__main__":
    main()