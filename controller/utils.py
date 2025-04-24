from model import records
import os

def load_dotenv(filename='.env'):
    base_dir = os.path.dirname(os.path.abspath(__file__))  # directory of the script
    env_path = os.path.join(base_dir, '..', filename)       # go up one level
    env = {}

    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' in line:
                key, value = line.split('=', 1)
                env[key.strip()] = value.strip().strip('"').strip("'")
    return env

env_vars = load_dotenv()

def get_last_folder(path):
    return os.path.basename(os.path.normpath(path))

def get_databases():
    return records.read_records(env_vars['DATABASES'])


