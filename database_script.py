import sqlite3
import os
import numpy as np
import pandas as pd
from make_the_dataframes import make_the_dataframes

# customer_clean_df, locations_clean_df, orders_clean_df, vendors_clean_df = make_the_dataframes() 
DATABASE_NAME = 'delivery.db'


sql_command_CREATE_CUSTOMERS = '''
CREATE TABLE customers ( 
    customer_id TEXT, 
    gender TEXT, 
    status INTEGER, 
    verified  INTEGER, 
    created_at TEXT,
    PRIMARY KEY (customer_id)
) ;'''

sql_command_CREATE_LOCATIONS = '''
CREATE TABLE locations (
    customer_id TEXT,
    location_number INTEGER,
    latitude REAL,
    longitude REAL,
    PRIMARY KEY (customer_id, location_number)
    FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
);'''

def create_table(sql_command):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute(sql_command)
    # commit our command
    conn.commit()
    # close our connection
    conn.close()

def show_all_tables():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute(''' SELECT name FROM sqlite_master WHERE type='table';''')
    conn.commit()
    result = cursor.fetchall()
    for item in result:
        print(item)
    # close our connection
    conn.close()

def show_table(table_name):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute(f''' PRAGMA table_info({table_name}) ''')
    conn.commit()
    result = cursor.fetchall()
    for item in result:
        print(item)
    # close our connection
    conn.close()

#create_table(sql_command_CREATE_CUSTOMERS)
#create_table(sql_command_CREATE_LOCATIONS)
#show_all_tables()
show_table('customers')
