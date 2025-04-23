# py-fabi-2
Python-based GUI for managing local CSV Databases.

## Code Structure

### /cli

Controller for pulling data, manipulate it, hand it over to the frontend and give it back again. You can manage your databases with this cli alone, no gui needed.

### /gui

PyQt6 frontend with as little logic as possible. 

### /model

Contains all methods to manage CSV files, treat them like a database. CRUD Operations, type definitions. The types are read from the json file in every database.

### /data

All additional files like: 

- **user_settings.json:** Default view, etc
- **database_list.json:** A List containg locations to all databases.

## Database Structure


A Database is a Folder containing the following structure:

stones/
├── stones.csv
├── stones.json
├── stone_types.csv
├── 1 salzach0425/
│   ├── 1 salzach0425.md
│   ├── attachments/
│   │   ├── 1 salzach0425 000.jpg
│   │   └── 1 salzach0425 001.jpg
├── 1 goisern0625/
│   ├── 1 goisern0625.md
│   ├── attachments/
│   │   ├── 1 goisern0625 000.jpg
│   │   └── 1 goisern0625 001.jpg


Where the leading number represents the index number in the csv file, that is named after the parent dir. The json file contains metadata for the single columns and the database itself.
