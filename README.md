# py-fabi-2
Python-based GUI for managing local CSV Databases.  

## Code Structure

### /controller

Controller for pulling data, manipulate it, hand it over to the frontend and give it back again. You can manage your databases with this cli alone, no gui needed.

### /gui

PyQt6 frontend with as little logic as possible. 

### /model

Contains all methods to manage CSV files, treat them like a database. CRUD Operations, type definitions. The types are read from the json file in every database.

### /data

All additional files like: 

- **user_settings.json:** Default view, etc
- **databases.csv:** A List containing locations to all databases.

## Database Structure

- database/
    - database.csv
    - database.json
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

Where the leading number represents the index id in the csv file, that is named after the parent dir. The json file contains metadata for the single columns and the database itself.
