The project was coded in python 3.8.6

All dependencies (libraries used) that have to be installed for project to run properly are stored in requirements.txt file.
To install all required dependencies run command: $ pip install -r requirements.txt

====================================

Brief explanation of the files (its advisable to run the files with this order):

1. data_preparation.ipynb : Used to explore and clean the data. Also stores the final cleaned pandas DataFrames into .csv files, for easier future use.
2. create_sqlite_tables.py : Consists the SQLite commands and a function to create the 'delivery.db' database and its respective tables
3. load_to_db.py: Loads the .csv cleaned files into the SQLite 'delivery.db'. Consists with functions, to delete, show schema info, show table info, and table data.
4. gui_db.py: Consists the GUI code.

