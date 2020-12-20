import os
import numpy as np
import pandas as pd

#load the csv to pandas DataFrames
path = 'cleaned_data/'
csv_list = os.listdir('cleaned_data/')

def make_the_dataframes():
    customer_clean_df = pd.read_csv(''.join([path,csv_list[0]]))
    locations_clean_df = pd.read_csv(''.join([path,csv_list[1]]))
    orders_clean_df = pd.read_csv(''.join([path,csv_list[2]]))
    vendors_clean_df = pd.read_csv(''.join([path,csv_list[3]]))
    return customer_clean_df, locations_clean_df, orders_clean_df, vendors_clean_df
