import csv
import logging


def read_records(file):
    """Return all projects."""
    with open(file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=";")
        logging.info("Reading Records.")
        return list(reader)


def create_record(file, new_record):
    with open(file, 'a', encoding="utf-8",newline="") as f:
        writer = csv.DictWriter(f, fieldnames=new_record.keys(), delimiter=";")
        writer.writerow(new_record) 
        logging.info("Create Record.")


def read_record(file,id):
    """Return the row that matches the id."""
    with open(file, 'r', encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")
        for record in reader:
            if record["id"] == id:
                return record
        logging.info("Reading Record.")


def overwrite_records(file,records):
    """Overwrites all records with an updated list"""
    with open(file, 'w+', encoding="utf-8",newline="") as f:
        writer = csv.DictWriter(f, fieldnames=records[-1].keys(), delimiter=";",extrasaction='ignore')
        writer.writerows(records)
        logging.info("Overwriting Records.")
