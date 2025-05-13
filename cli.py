from argparse import ArgumentParser
import controller
from _version import __version__


def list_vaults():
    """
    Retrieves and displays a list of vaults with their paths and modification times.
    """
    try:
        vaults: List[Dict[str, str]] = controller.xenolyte.return_all_vaults()
    except Exception as e:
        print(f"Error retrieving vaults: {e}")
        return

    if not vaults:
        print("No vaults available.")
        return

    table_data = []
    for index, vault in enumerate(vaults, start=1):
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


def add_folder():
    path = input("Enter existing folder path: ")
    controller.xenolyte.append_vault(path)
    list_vaults()


FUNCTIONS = [
    # Vault Functions
    ["listvaults", "List all currently selected vaults", list_vaults],
    ["addfolder", "Add an existing folder as vault, [path]", add_folder],
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


