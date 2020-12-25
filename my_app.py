import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import pandas as pd

root = tk.Tk()
root.geometry('1000x800')
root.title('SQLite gui')
my_tree = ttk.Treeview(root)
my_tree.grid(row=2, column=1, rowspan=8, columnspan=8)



def show_all_customers():
    table_info, table_name = select_all_from('customers')
    create_trees(table_info, table_name)

def show_all_vendors():
    table_info, table_name = select_all_from('vendors')
    create_trees(table_info, table_name)

def show_all_orders():
    table_info, table_name = select_all_from('orders')
    create_trees(table_info, table_name)

def show_all_locations():
    table_info, table_name = select_all_from('locations')
    create_trees(table_info, table_name)

def entry_customers():
    conn = sqlite3.connect('delivery.db')
    cursor = conn.cursor()
    customer_id = customer_id_entry.get()
    gender = customer_gender_entry.get()
    status = customer_status_entry.get()
    verified = customer_verified_entry.get()
    dateTimeObj = datetime.now()
    created_at = dateTimeObj.strftime("%Y-%m-%d %H:%M:%S")
    data_tuple = (customer_id, gender, status, verified, created_at)
    if not customer_id:
        label_screen.config(text='Give Customer ID')
    else:
        cursor.execute(f'''INSERT INTO customers (customer_id, gender, status, verified, created_at) VALUES(?, ?, ?, ?, ?);''', data_tuple)
        label_screen.config(text=f'New customer with: {data_tuple}, inserted.')
    conn.commit()
    conn.close()


def select_all_from(table_name):
    for i in my_tree.get_children():
        print('times')
        my_tree.delete(i)
    conn = sqlite3.connect('delivery.db')
    cursor = conn.cursor()
    cursor.execute(f''' PRAGMA table_info({table_name}); ''')
    conn.commit()
    table_info = cursor.fetchall()
    conn.close
    return table_info, table_name

def create_trees(table_info, table_name):
    # the tree was made as a global variable in order to remove the previous generated tkk.Treeview object, otherwise more objects where created and 
    global my_tree
    try:
        my_tree.grid_forget()
        del my_tree # the previous treeview instance is deleted to save memory
    except:
        pass
    my_tree = ttk.Treeview(root)
    column_name_ls = []
    for column_name in table_info:
        column_name_ls.append(column_name[1])
    my_tree['columns'] = (column_name_ls)
    my_tree.column('#0', width=0)
    my_tree.heading('#0', text='', anchor='w')
    for column in column_name_ls:
        my_tree.column(column, stretch=False, width=90)
        my_tree.heading(column, text=column, anchor='w')
    my_tree.insert(parent='', index='end', iid=0, text='', values=())
    
    try:
        conn = sqlite3.connect('delivery.db')
        cursor = conn.cursor()
        cursor.execute(f'''SELECT * FROM {table_name} LIMIT 100; ''')
        conn.commit
        result = cursor.fetchall()
        for row in result:
            my_tree.insert("", tk.END, values=row)
        
        my_tree.grid(row=2, column=1, rowspan=8, columnspan=8)
    except:
        print('Error')
    conn.close()

def show_all_tables():
    conn = sqlite3.connect('delivery.db')
    cursor = conn.cursor()
    try:
        cursor.execute(''' SELECT name FROM sqlite_master WHERE type='table';''')
        conn.commit()
        result = cursor.fetchall()
        label_screen.config(text=result)
    except:
        label_screen.config(text='Error')
    conn.close()

def create_histogram():
    # the data will be collected by the database not by the csv file.
    conn = sqlite3.connect('delivery.db')
    df = pd.read_sql_query(''' SELECT deliverydistance FROM orders ''', conn )
    f, ax = plt.subplots(figsize=(5, 5))
    df['deliverydistance'].hist(bins=40)
    canvas = FigureCanvasTkAgg(f, master=root)  # A tk.DrawingArea.
    canvas.draw()
    canvas.get_tk_widget().grid(row = 12, column = 1)

 


# ##### gui code ####


# SETTING THE LABELS AND ENTRIES

customer_id_label = tk.Label(root, width=20, text='Customer ID')
customer_id_label.grid(row=10, column=1, padx=0)
customer_id_entry = tk.Entry(root, width=20)
customer_id_entry.grid(row=11, column=1, padx=0)

customer_gender_label = tk.Label(root, width=20, text='Gender')
customer_gender_label.grid(row=10, column=2, padx=0)
customer_gender_entry = tk.Entry(root, width=20)
customer_gender_entry.grid(row=11, column=2, padx=0)

customer_status_label = tk.Label(root, width=20, text='Status')
customer_status_label.grid(row=10, column=3, padx=0)
customer_status_entry = tk.Entry(root, width=20)
customer_status_entry.grid(row=11, column=3, padx=0)

customer_verified_label = tk.Label(root, width=20, text='Verified')
customer_verified_label.grid(row=10, column=4, padx=0)
customer_verified_entry = tk.Entry(root, width=20)
customer_verified_entry.grid(row=11, column=4, padx=0)

label_screen = tk.Label(root, width=60, bg='green', fg='white', text='screen')
label_screen.grid(row=1, column=1, columnspan=3)

# SETTING BUTTONs

show_table_names = tk.Button(text='Table names', command=show_all_tables, width= 20)
show_table_names.grid(row=1, column=0)

show_all_customers_button = tk.Button(text="Show all customers", command=show_all_customers, width = 20)
show_all_customers_button.grid(row=2, column=0, padx=5)

show_all_vendors_button = tk.Button(text="Show all vendors", command=show_all_vendors, width = 20)
show_all_vendors_button.grid(row=3, column=0, padx=5)

show_all_orders_button = tk.Button(text="Show all orders", command=show_all_orders, width = 20)
show_all_orders_button.grid(row=4, column=0, padx=5)

show_all_locations_button = tk.Button(text="Show all locations", command=show_all_locations, width = 20)
show_all_locations_button.grid(row=5, column=0, padx=5)

entry_customers_button = tk.Button(text="Entry customers", command=entry_customers, width = 20)
entry_customers_button.grid(row=11, column=0, padx=5)

create_histogram_buttom = tk.Button(text='Create histogram', command=create_histogram, width = 20)
create_histogram_buttom.grid(row=12, column=0, padx=5)

quit = tk.Button(text="QUIT", fg="red", command=root.destroy)
quit.grid(row=9, column=0)


# GUI MAIN LOOP
root.mainloop()

