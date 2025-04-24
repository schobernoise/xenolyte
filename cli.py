from argparse import ArgumentParser
from controller import utils, folders
from _version import __version__

FUNCTIONS = {
    "createfolder": folders.create_folder_from_record
}

parser = ArgumentParser(prog='cli')
parser.add_argument('database', help="Postional Argument, which database should it be?")
parser.add_argument('command', help="Postional Argument, command to do with database.", nargs='?')
parser.add_argument('-id',action='store',dest="id", help="Id of record.") 
parser.add_argument('-v', '--version',action='version',version=__version__) 

args = parser.parse_args()

for database in utils.get_databases():
    db_name = utils.get_last_folder(database["path"])
    # print(database)
    if args.database == db_name:
        # print(db_name)
        func = FUNCTIONS.get(args.command)
        if func:
            func(database["path"],args)
        else:
            print(f"No such function: {args.command}")

        
