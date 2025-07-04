from cli import CLI


# VAULT_COMMANDS = [
#     {
#         "name": "list",
#         "help": "List all currently selected vaults",
#         "func": CLI.list_vaults,
#         "arguments": []  
#     },
#     {
#         "name": "add",
#         "help": "Add an existing folder as vault",
#         "func": CLI.add_vault_folder,
#         "arguments": [] 
#     },
#     {
#         "name": "select",
#         "help": "Select a vault from list of vaults",
#         "func": CLI.select_vault,
#         "arguments": [] 
#     },
#     {
#         "name": "show",
#         "help": "Display currently selected vault",
#         "func": CLI.show_selected_vault,
#         "arguments": []  
#     }
# ]


# DATABASE_COMMANDS = [
#     {
#         "name": "listtables",
#         "help": "List all records in a table",
#         "func": CLI.list_tables,
#         "arguments": []
#     },
#     {
#         "name": "listrecords",
#         "help": "List all records in a table",
#         "func": CLI.list_records,
#         "arguments": [
#             {
#                 "name": "table",
#                 "type": str,
#                 "help": "The name of the table to list records from"
#             }
#         ]
#     },
#     {
#         "name": "deletetable",
#         "help": "Delete Table.",
#         "func": CLI.delete_table,
#         "arguments": [
#             {
#                 "name": "table",
#                 "type": str,
#                 "help": "The name of the table to delete"
#             }
#         ]
#     },
#     {
#         "name": "showrecord",
#         "help": "Show a specific record by ID in a table",
#         "func": CLI.show_record,
#         "arguments": [
#             {
#                 "name": "table",
#                 "type": str,
#                 "help": "The name of the table to retrieve the record from"
#             },
#             {
#                 "name": "record_id",
#                 "type": str,
#                 "help": "The ID of the record to retrieve"
#             }
#         ]
#     },
#     {
#         "name": "deleterecord",
#         "help": "Delete a specific record by ID in a table",
#         "func": CLI.delete_record,
#         "arguments": [
#             {
#                 "name": "table",
#                 "type": str,
#                 "help": "The name of the table to retrieve the record from"
#             },
#             {
#                 "name": "record_id",
#                 "type": str,
#                 "help": "The ID of the record to retrieve"
#             }
#         ]
#     },
#     {
#         "name": "createrecord",
#         "help": "Create a new Record in a specific table",
#         "func": CLI.create_record,
#         "arguments": [
#             {
#                 "name": "table",
#                 "type": str,
#                 "help": "The name of the table to create the record in."
#             }
#         ]
#     },
#     {
#         "name": "updaterecord",
#         "help": "Update an existing Record in a specific table",
#         "func": CLI.update_record,
#         "arguments": [
#             {
#                 "name": "table",
#                 "type": str,
#                 "help": "The name of the table to create the record in."
#             },
#             {
#                 "name": "record_id",
#                 "type": str,
#                 "help": "The ID of the record to retrieve"
#             }
#         ]
#     }
# ]



def main():

    _CLI = CLI()



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
    

if __name__ == "__main__":
    main()