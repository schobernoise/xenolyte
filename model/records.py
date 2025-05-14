import csv
import logging


def read_records(file):
    """Return all records."""
    with open(file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=";")
        logging.info("Reading Records.")
        return list(reader)


def create_record(file, new_record):
    """Create record"""
    with open(file, 'a', encoding="utf-8",newline="") as f:
        writer = csv.DictWriter(f, fieldnames=new_record.keys(), delimiter=";")
        writer.writerow(new_record) 
        logging.info("Create Record.")


def read_record(file,id):
    """Return the record that matches the id."""
    with open(file, 'r', encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")
        for record in reader:
            if record["id"] == id:
                return record
        logging.info("Reading Record.")


def overwrite_records(file, records):
    """
    Overwrites all records in the given CSV file with an updated list of records.
    
    Args:
        file (str): The path to the CSV file to overwrite.
        records (List[Dict[str, any]]): A list of dictionaries representing the CSV records.
    """
    if not records:
        logging.warning("No records provided to overwrite. Operation skipped.")
        return None
    
    try:
        fieldnames = list(records[0].keys())
        logging.debug(f"Determined fieldnames: {fieldnames}")
        
        with open(file, 'w', encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";", extrasaction='ignore')
            
            writer.writeheader()
            logging.debug("CSV header written.")
            
            writer.writerows(records)
            logging.info(f"Successfully overwrote records in {file}.")
        
        return file
    
    except Exception as e:
        logging.error(f"Failed to overwrite records in {file}: {e}")
        return None
