# Xenolyte

> Python CLI and PyQt6 GUI for managing local, CSV-based folder databases.

## Concept and Terminology

Xenolyte, very much like Obsidian, opens a folder as **Vault**. This Folder gets added to `vaults.csv`, a list of all vaults previously opened. The last one that was opened will be opened automatically when the programm starts.

You will have an empty room to fill with your data. When **Obsidian** is all about text based information then **Xenolyte** is aiming at tabular data. Altough it utilzes markdown notes to attach information to rows or folders. The idea is to have information structured in a way that is easily comprehensable for humans in openly accessible file formats, but in a standardized way so Xenolyte can read and manipulate it.

A Vault can have multiple **containers**, alongside an equally named json-file for metadata. A container in its most basic form is a csv-file in the vault, which is called a **table**. You can, however, expand this table to become a **database**. A database is a subfolder of the vault that contains an equally named csv file (the table), a `config.json` containing metadata about columns and the database, an equally named markdown-file as folder note and a **functions.py**. The python file is containing a class extending the Xenolyte-class. It has access to all Vault-Objects, so you are able to create custom functions and cli-commands.

A **record** is one row of a table. If the table becomes a Database the record is able to have a **record-folder**. This record-folder itself contains a Markdown-File and every other file you like.

## Structure

### Vault Structure with tables

- vault/
  - .xenolyte.json
  - database1/
  - database2/
  - table1.csv
  - table2.csv


You can create as many tables as you like to store simple tabular data. When you feel the need to organize textual information and files in a tabular manner then the time has come to introduce databases. A database is a folder inside your vault that consists of the following structure:


### Database Structure

- database/
  - database.csv
  - database.md
  - functions.py
  - config.json
  - 001 record1/
    - 001 record1.md
    - attachments/
      - image01.jpg
      - document.pdf
  - 002 record2/
    - 002 record2.md
    - attachments/
      - image01.jpg
      - document.pdf
        ...

Where the leading number represents the index id in the csv file that is named after the parent dir. The config.json contains metadata for the single columns and the database itself like typing, column-width, etc. You do not see any of this structure. Instead you only see one entry in the sidebar which fills the table by clicking on it. You now also see an attached markdown note per record, and a mosaic of all attachments in its corresponding record-folder.

The functions.py contains a pre-generated **class Vault**. Every method of this class gets added as a button to the toolbox area in the application and gets its own cli-command. They receive an object with an array of all vaults and all variables of config.json which enables users to create their own settings for their own functions.

## How to use

### First Time Use

> To be expanded.

#### CLI

Copy the `xenolyte.template.json` from the `ressources` dir into the data dir and rename it to `xenolyte.json`. This enables you to run the first time initialize command:

```python cli.py xenolyte init```

Which will prompt you for a path to your first vault location. It then sets up a `vaults.csv` in a predefined location, found at the `xenolyte.json` file.

#### GUI

> Not yet in development.

## Using it

### Logging

Using the CLI makes it possible to enable various loglevels for detailed debugging.  

`python cli.py -vvv xenolyte`

### Vault Commands

### Database Commands

> Will be renamed to Container Commands in the future.


`python cli.py -vvv database showrecord <database_name> <record_id>`

### Filesystem

Any Vault can be located in any cloud-location, e.g. Nextcloud.

**Some usecases include but are not limted to:**

- Cataloging a collection of fossils, rocks, plants, etc and adding metdata to it as well as photos and documents.
- Contact list, booking catalogue, CRM


## Future Features

- Lightweight mini input form window to add new records, triggered by cli.
- Table-Templates
  - Frequently used table layouts like [id,title,slug,status,description] 
- Automatic photo compression and thumbnail caching.
- Calendar/Kanban View
- Version control with git, syncing vault or single databases.


> **Note for the future:** I have plans to implement prefix-inferred column-typing but this is not a top priority right now. This would enable to type plain csv files as well, which is imperative to work with those tables like airtable or baserow.