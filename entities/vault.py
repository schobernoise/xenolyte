import utils
import table,database

class Vault:

    def __init__(self,path):
        self.path = path
        self.name = utils.get_folder_name(path)
        self.tables = self.get_all_tables()

    
    def reflect_changes(self):
        # TODO: Functions that actually create the folders and files
        # But only for initial creation
        # Needs to be in Vault Class
        for table in self.tables:
            if isinstance(table, table.Table):
                # Create File, exist = ok
                pass
            elif isinstance(table,database.Database):
                pass

        # TODO: Reflect changes returns status and errors
    

    def get_all_tables(self):
        """In this case, Tables refers to Tables and Databases alike. Fetches all entities of the vault."""
        # TODO: Find better terminology for all entities in vault.
        logging.info("Get all Tables")
        objects=[]
        try:
            items = os.listdir(self.path)
        except Exception as e:
            logging.error(f"Error reading directory {self.path}: {e}")
            return objects

        for item in items:
            item_path = os.path.join(self.path, item)
            logging.debug("%s", item_path)
            if os.path.isfile(item_path) and item.lower().endswith('.csv'):
                objects.append(table.Table(item_path))
            elif os.path.isdir(item_path):
                table_path = os.path.join(item_path, f"{item}.csv")
                # print(table_path)
                if os.path.isfile(table_path):
                    objects.append(database.Database(table_path))
        return objects


    def get_table_from_name(self, name):
        """Returns a table or databse object by its name"""
        # TODO: Expand fn to general query functionality.
        logging.info("Get Table from Name")
        for table in self.tables:
            if table["name"] == name:
                return table
        return False


    def create_new_table(self,name):
        """Creates a new table inside the active Vault."""
        logging.debug("Create New Table")
        self.tables.append(table.Table(os.path.join(self.path,name + ".csv")))
        self.reflect_changes()
        logging.info("created new table")
    

    def create_new_database(self, name):
        """Creates a new database inside the active Vault."""    
        logging.info("Create New Database")
        self.tables.append(database.Database(os.path.join(self.path,name)))
        self.reflect_changes()
        logging.info("created new database")
        

    def create_database_from_table(self, name):
        """Creates a database from an existing table inside the active Vault."""
        logging.info("Create Database from Table")
        # Two methods of doing this
            # 1. Copying the CSV over after creating the folder structure
                # Big files get copied faster as is, no validation
            # 2. Use Data Model to handle transfer
                # Might take longer for larger Data but data can be validated/manipulated on the fly  
            # TODO: Sticking with Method no. 2 for now. Might add a flag for manual transfer later.
        temp_table = self.delete_table(name)
        self.tables.append(database.Database(os.path.join(self.path,name),records=temp_table.records))
        logging.info("Created database from table")
    

    def delete_table(self, name):
        """Deletes an Entity from the Vault."""
        for table in self.tables:
            if table.name == name:
                self.tables.remove(table)
                return table
    