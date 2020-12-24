import tkinter as tk
from tkinter import ttk
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns


def show_all_customers():
    select_all_from('customers')

def show_all_vendors():
    select_all_from('vendors')

def show_all_orders():
    select_all_from('orders')

def show_all_locations():
    select_all_from('locations')

def select_all_from(table_name):
    for i in my_tree.get_children():
        print('times')
        my_tree.delete(i)
    conn = sqlite3.connect('delivery.db')
    cursor = conn.cursor()
    #command = SQL_command_entry.get()
    cursor.execute(f''' PRAGMA table_info({table_name}) ''')
    conn.commit()
    table_info = cursor.fetchall()
    column_name_ls = []
    for column_name in table_info:
        column_name_ls.append(column_name[1])
    my_tree['columns'] = (column_name_ls)
    my_tree.column('#0', width=0)
    my_tree.heading('#0', text='', anchor='w')
    for column in column_name_ls:
        my_tree.column(column, width=100)
        my_tree.heading(column, text=column, anchor='w')
    my_tree.insert(parent='', index='end', iid=0, text='', values=())
    my_tree.grid(row=4, column=1)

    try:
        cursor.execute(f'''SELECT * FROM {table_name} LIMIT 100''')
        result = cursor.fetchall()

        for row in result:
            my_tree.insert("", tk.END, values=row)
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


# ##### gui code ####

root = tk.Tk()
root.geometry('1000x450')
root.title('SQLite gui')
my_tree = ttk.Treeview(root)

# SETTING THE LABELS AND ENTRIES

SQL_command_entry = tk.Entry(root, width=50)
SQL_command_entry.grid(row=0, column=1, padx=0)

label_screen = tk.Label(root, width=50, bg='green', fg='white')
label_screen.grid(row=1, column=1)

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



quit = tk.Button(text="QUIT", fg="red", command=root.destroy)
quit.grid(row=8, column=0)


# GUI MAIN LOOP
root.mainloop()

