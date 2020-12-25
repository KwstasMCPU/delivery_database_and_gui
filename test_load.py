from make_the_dataframes import make_the_dataframes
from database_script import show_table_rows, show_table_info, show_all_tables
import numpy as np
import pandas as pd
import sqlite3

DATABASE_NAME = 'delivery.db'
customer_clean_df, locations_clean_df, orders_clean_df, vendors_clean_df = make_the_dataframes()

def load_dataframe_to_db(df, table, DATABASE_NAME, chunk=100):
    conn = sqlite3.connect(DATABASE_NAME)
    df.to_sql(table, conn, if_exists='replace', index = False, chunksize = 100)
    conn.commit()
    conn.close()

# load_dataframe_to_db(customer_clean_df, 'customers', DATABASE_NAME)
# load_dataframe_to_db(locations_clean_df, 'locations', DATABASE_NAME)
# load_dataframe_to_db(vendors_clean_df, 'vendors', DATABASE_NAME)
# load_dataframe_to_db(orders_clean_df, 'orders', DATABASE_NAME)


# print(vendors_clean_df.head)
# print('')
# show_table_info('vendors')
# show_table_rows('vendors', 100)