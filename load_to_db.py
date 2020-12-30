import os
import numpy as np
import pandas as pd
import sqlite3

DATABASE_NAME = 'delivery.db'

#load the csv to pandas DataFrames
path = 'cleaned_data/'
csv_list = os.listdir('cleaned_data/') # we make a list of the file names (.csv files), in order to use them in the make_the_dataframes() 

def make_the_dataframes():
    """
    this function reads the csv files with the clean data, and turns them to a dataframe
    """
    customer_clean_df = pd.read_csv(''.join([path,csv_list[0]])) #  i used .join() instead of string concatenation '+' since is more efficient and i have been used to it https://waymoot.org/home/python_string/ https://stackoverflow.com/questions/3055477/how-slow-is-pythons-string-concatenation-vs-str-join
    locations_clean_df = pd.read_csv(''.join([path,csv_list[1]]))
    orders_clean_df = pd.read_csv(''.join([path,csv_list[2]]))
    vendors_clean_df = pd.read_csv(''.join([path,csv_list[3]]))
    return customer_clean_df, locations_clean_df, orders_clean_df, vendors_clean_df

def load_dataframe_to_db(df, table, DATABASE_NAME='delivery.db', chunk=100):
    """
    this function turns a pandas dataframe to an SQLite table

    Parameters:
        df (pandas dataframe): The first parameter.
        table (str): The table name the pandas dataframe is going to be converted into the SQLite database
        DATABASE_NAME (str): The name of the database to load the table. (default 'delivery.db)
        chunk (int): Specify the number of rows in each batch to be written at a time. 
                    Is assign to the chunksize parameter of the to_sql(), which by default tries to write all rows at once. (default 100)
    """
    conn = sqlite3.connect(DATABASE_NAME)
    df.to_sql(table, conn,
                if_exists='append', # we used append since the tables, although empty, they already exist. If replaced was used, the tables and theier variable types would had been replaced.
                index = False, # do not load the dataframe index as an sqlite db column
                chunksize = chunk)
    conn.commit()
    conn.close()

def show_all_tables(DATABASE_NAME = 'delivery.db'):
    """
    This function prints the table names of a database
    Parameters:
        DATABASE_NAME (str): the name of the database the table to be created (default 'delivery.db')
    """
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute(''' SELECT name FROM sqlite_master WHERE type='table';''')
    conn.commit()
    result = cursor.fetchall()
    for item in result:
        print(item)
    # close our connection
    conn.close()

def show_table_info(table_name, DATABASE_NAME = 'delivery.db'):
    """
    This function prints the information of a database table (look: https://www.sqlite.org/pragma.html#pragma_table_info, https://www.sqlite.org/pragma.html#pragma_table_info )
    Parameters:
        table_name (str): the table we request to receive information
        DATABASE_NAME (str): the name of the database where the table is (default 'delivery.db')
    """
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute(f''' PRAGMA table_info({table_name}) ''')
    conn.commit()
    result = cursor.fetchall()
    for item in result:
        print(item)
    # close our connection
    conn.close()

def show_table_rows(table_name, DATABASE_NAME='delivery.db', rows = 100):
    """
    This function makes a database query and returns the results.
    Parameters:
        table_name (str): the table we want to perform the query
        DATABASE_NAME (str): the name of the database where the table is (default 'delivery.db')
        rows (int): the number of rows to limited our results (default 100)
    """
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute(f''' SELECT * FROM {table_name} LIMIT {rows};''')
    conn.commit()
    for row in cursor.fetchall():
        print (row)
    conn.close()

def delete_table(table_name, DATABASE_NAME = 'delivery.db'):
    """
    This functions deleted a table from the database
    Parameters:
        table_name (str): the table we want to delete
        DATABASE_NAME (str): the name of the database the table to be deleted (default 'delivery.db')
    """
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute(f''' DROP TABLE {table_name}; ''')
    conn.commit()
    conn.close()

customer_clean_df, locations_clean_df, orders_clean_df, vendors_clean_df = make_the_dataframes()

# load_dataframe_to_db(customer_clean_df, 'customers', DATABASE_NAME)
# load_dataframe_to_db(locations_clean_df, 'locations', DATABASE_NAME)
# load_dataframe_to_db(vendors_clean_df, 'vendors', DATABASE_NAME)
# load_dataframe_to_db(orders_clean_df, 'orders', DATABASE_NAME)

show_all_tables()
print('cid # name # type # notnull # dflt_value # pk')
print('=========')
show_table_info('customers')
print('=========')
show_table_info('orders')
print('=========')
show_table_info('locations')
print('=========')
show_table_info('vendors')
