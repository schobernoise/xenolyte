# Xenolyte

> Python-based GUI for managing local CSV Databases. Using PyQt6.

## Tasks

The plan is to get the CLI fully working before plugging it into the GUI.

- [x] Add Vault to vaults.csv
- [ ] Create .xenolyte.json
- [ ] Read .xenolyte.json

- [ ] Read Database Folder
  - [ ] Read Markdown File
  - [x] Read config.json
  - [x] Read database.csv
  - [ ] Read Functions.py

- [x] Create Database Folder **Fn**
  - [x] Create README.md
  - [x] Create config.json
  - [x] Create Database CSV
  - [ ] Create functions.py
- [x] Create Table (CSV) **Fn**
  - [x] New Table CSV
  - [ ] Extend existing Database Folder with more Tables for types.
- [x] Create Folder from Record **Fn**
  - [x] Create Subfolder
  - [x] Add Markdown Folder Note
  - [x] Add attachments Folder

- [ ] CLI Tools
  - [ ] Vaults functions
  - [ ] Database Functions
  - [ ] Custom Functions

- [ ] PyQt6 GUI
  - [x] Rapid Prototype

![](ressources/gui%20development%202025.png?raw=true)


### Future Features

- Lightweight mini input form window to add new records, triggered by cli.
- Table-Templates
  - Frequently used table layouts like [id,title,slug,status,description] 
- Automatic photo compression and thumbnail caching.
- Calendar/Kanban View
- Version controll with git, syncing vault or single databases.


## Concept and Terminology

Xenolyte, very much like Obsidian, opens a folder as **Vault**. This Folder gets added to `vaults.csv`, a list of all vaults previously opened. The last one that was opened will be opened automatically when the programm starts.

You will have an empty room to fill with your data. When **Obsidian** is all about text based information then **Xenolyte** is aiming at tabular data. Altough it utilzes markdown notes to attach information to rows or folders. The idea is to have information structured in a way that is easily comprehensable for humans in openly accessible file formats, but in a standardized way so Xenolyte can read and manipulate it.

A Vault can have multiple csv-files. Those are called tables. A table by itself has the ability to contain anything a csv file can contain. 

> Vault Structure

- vault/
  - .xenolyte.json
  - database1/
  - database2/
  - table1.csv
  - table2.csv


> **Note for the future:** I have plans to implement prefix-inferred column-typing but this is not a top priority right now. But this would enable to type plain csv files as well, which is imperative to work with those tables like airtable or baserow.

You can create as many tables as you like to store simple tabular data. When you feel the need to organize textual information and files in a tabular manner then the time has come to introduce databases. A database is a folder inside your vault that consists of the following structure:


> Database Structure

- database/
  - database.csv
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


## Usecases

All of the usescases can be located in any cloud service.

- Cataloging a collection of fossils, rocks, plants, etc and adding metdata to it as well as photos and documents.
- Contact list, booking catalogue, CRM