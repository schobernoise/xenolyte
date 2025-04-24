from model import records
from controller import utils
import os
import logging
from datetime import date

today = date.today()

### Folder Management ###

def create_folder_from_record(path,args):
    db_name = utils.get_last_folder(path)
    record = records.read_record(os.path.join(path,f"{db_name}.csv"),args.id)
    if not record["slug"]:
        print("Slug is needed for folder creation.")
        return

    parent_dir = os.path.dirname(os.path.abspath(path))
    folder_name = f"{record['id']} {record['slug']}"
    new_folder_path = os.path.join(path, folder_name)
    os.makedirs(new_folder_path, exist_ok=True)
    create_folder_note(os.path.join(new_folder_path,f"{folder_name}.md"),record)
    logging.info(new_folder_path)
    return new_folder_path


def create_folder_note(path,record):
    frontmatter = f"""---
related:
  - 
created:
  - "[[{today.strftime("%d-%m-%Y-%A")}]]"
aliases: 
 - {record["title"]}
tags: 
 - ist/projekt
Projektnummer: "{record["project_number"]}"
attachments:
---

"""


    with open(path, 'w') as f:
        f.write(frontmatter)
    logging.info(path)
    return path
