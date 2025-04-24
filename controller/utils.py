from model import records
import os

def get_last_folder(path):
    return os.path.basename(os.path.normpath(path))


def get_databases():
    return records.read_records("./data/databases.csv")

