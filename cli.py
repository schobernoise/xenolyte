from argparse import ArgumentParser
from controller import utils, folders
from _version import __version__


FUNCTIONS = [
    # Vault Functions
    ["listvaults", "List all currently selected vaults"],
    ["addexistingfolder", "Add an existing folder as vault, [path]"],
    ["createnewvault", "Create a new Vault in Location [path]"],
    ["selectvault", "Select a vault from List of Vaults, [id]"],
    ["showselectedvault", "Display currently selected vault"],

    # Database functions
    ["createtable", ""],
    ["createdatabase", ""],
    ["createrecordfolder", ""],
    ["createrecord", ""],

]

parser = ArgumentParser(prog='cli')
parser.add_argument('database', help="Postional Argument, which database should it be?", default=False)
parser.add_argument('command', help="Postional Argument, command to do with database.", nargs='?')
parser.add_argument('-id',action='store',dest="id", help="Id of record.") 
parser.add_argument('-v', '--version',action='version',version=__version__) 

args = parser.parse_args()

# for database in utils.get_databases():
#     db_name = utils.get_last_folder(database["path"])
#     # print(database)
#     if args.database == db_name:
#         # print(db_name)
#         func = FUNCTIONS.get(args.command)
#         if func:
#             func(database["path"],args)
#         else:
#             print(f"No such function: {args.command}")

        
