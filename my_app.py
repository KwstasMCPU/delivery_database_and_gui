import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime


root = tk.Tk()
root.geometry('1300x600')
root.title('SQLite gui')

buttons_frame = tk.Frame(root, highlightbackground='grey'  ,highlightthickness=1, padx=5, pady=5)
buttons_frame.grid(row=0, column=0, rowspan=10)

sql_entry_and_screen_frame = tk.Frame(root, highlightbackground='grey'  ,highlightthickness=1, padx=5, pady=5)
sql_entry_and_screen_frame.grid(row=0, column=1, rowspan=2)

treeview_frame = tk.Frame(root, highlightbackground='black', highlightthickness=1)
treeview_frame.grid(row = 2, column = 1)

down_frame = tk.Frame(root, highlightbackground='black', highlightthickness=1, padx=5, pady=5)
down_frame.grid(row = 9, column=1)

plot_frame = tk.Frame(root,  highlightbackground='black', highlightthickness=1)
plot_frame.grid(row=16, column = 0)

my_1st_tree = ttk.Treeview(treeview_frame, columns=[x for x in range(0,4)])
my_1st_tree.grid(row=2, column=1, rowspan=8, columnspan=10)


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
    my_tree = ttk.Treeview(treeview_frame)
    column_name_ls = []
    for column_name in table_info:
        column_name_ls.append(column_name[1])
    my_tree['columns'] = (column_name_ls)
    my_tree.column('#0', width=0)
    my_tree.heading('#0', text='', anchor='w')
    for column in column_name_ls:
        my_tree.column(column, stretch=False, width=95)
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
        my_tree.grid(row=0, column=0, rowspan=8, columnspan=8)
        conn.close()
    except Exception as e:
        print(e)
        label_screen.config(text=e)

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
    global canvas
    try:
        canvas.grid_forget()
        del canvas
    except:
        pass
    # the data will be collected by the database not by the csv file.
    conn = sqlite3.connect('delivery.db')
    df = pd.read_sql_query(''' SELECT deliverydistance FROM orders ''', conn )
    f, ax = plt.subplots(figsize=(4, 4))
    df['deliverydistance'].hist(bins=40)
    canvas = FigureCanvasTkAgg(f, master=plot_frame)  # A tk.DrawingArea.
    canvas.draw()
    canvas.get_tk_widget().grid(row = 16, column = 0, columnspan=3)

def mean_item_count():
    conn = sqlite3.connect('delivery.db')
    df = pd.read_sql_query(''' SELECT item_count FROM orders ''', conn )
    label_screen.config(text="{:.4f}".format(df['item_count'].mean()))

def mean_grand_total():
    conn = sqlite3.connect('delivery.db')
    df = pd.read_sql_query(''' SELECT grand_total FROM orders ''', conn )
    label_screen.config(text="{:.4f}".format(df['grand_total'].mean())) # formats the float to 4 decimals

def run_sql_command():
    conn = sqlite3.connect('delivery.db')
    cursor = conn.cursor()
    command = sql_command_entry.get()
    try:
        if command.split()[0].upper() == 'SELECT':
            print('SELECT')
            try:
                cursor.execute(command)
                result = cursor.fetchall()
                for r in result:
                    #
                    print(r)
            except Exception as e:
                print(e)
                label_screen.config(text=e)
        else:
            try:
                cursor.execute(command)
                print(", ".join([f'{command}','runned successfully.']))
            except Exception as e:
                print(e)
                label_screen.config(text=e)
    except:
        pass


# ##### gui code ####


# SETTING THE LABELS AND ENTRIES

sql_command_entry = tk.Entry(sql_entry_and_screen_frame, width=60)
sql_command_entry.grid(row=0, column=1)

label_screen = tk.Label(sql_entry_and_screen_frame, width=60, bg='green', fg='white', text='screen')
label_screen.grid(row=1, column=1)

customer_id_label = tk.Label(down_frame, width=20, text='Customer ID')
customer_id_label.grid(row=9, column=1, padx=0)
customer_id_entry = tk.Entry(down_frame, width=20)
customer_id_entry.grid(row=10, column=1, padx=0)

customer_gender_label = tk.Label(down_frame, width=20, text='Gender')
customer_gender_label.grid(row=9, column=2, padx=0)
customer_gender_entry = tk.Entry(down_frame, width=20)
customer_gender_entry.grid(row=10, column=2, padx=0)

customer_status_label = tk.Label(down_frame, width=20, text='Status')
customer_status_label.grid(row=9, column=3, padx=0)
customer_status_entry = tk.Entry(down_frame, width=20)
customer_status_entry.grid(row=10, column=3, padx=0)

customer_verified_label = tk.Label(down_frame, width=20, text='Verified')
customer_verified_label.grid(row=9, column=4, padx=0)
customer_verified_entry = tk.Entry(down_frame, width=20)
customer_verified_entry.grid(row=10, column=4, padx=0)



# SETTING BUTTONs

sql_command_run_button = tk.Button(buttons_frame, text='Run command', command=run_sql_command, width=20)
sql_command_run_button.grid(row=0, column=0)

show_table_names = tk.Button(buttons_frame, text='Table names', command=show_all_tables, width= 20)
show_table_names.grid(row=1, column=0)

show_all_customers_button = tk.Button(buttons_frame, text="Show all customers", command=show_all_customers, width = 20)
show_all_customers_button.grid(row=2, column=0)

show_all_vendors_button = tk.Button(buttons_frame, text="Show all vendors", command=show_all_vendors, width = 20)
show_all_vendors_button.grid(row=3, column=0)

show_all_orders_button = tk.Button(buttons_frame, text="Show all orders", command=show_all_orders, width = 20)
show_all_orders_button.grid(row=4, column=0)

show_all_locations_button = tk.Button(buttons_frame, text="Show all locations", command=show_all_locations, width = 20)
show_all_locations_button.grid(row=5, column=0)

mean_item_count_button = tk.Button(buttons_frame, text='Mean Item Count', command=mean_item_count, width=20)
mean_item_count_button.grid(row=6, column=0)

mean_grand_total_button = tk.Button(buttons_frame, text='Mean Grand Total', command=mean_grand_total, width=20)
mean_grand_total_button.grid(row=7, column=0)

entry_customers_button = tk.Button(buttons_frame, text="Entry customers", command=entry_customers, width = 20)
entry_customers_button.grid(row=8, column=0)

create_histogram_buttom = tk.Button(buttons_frame, text='Create histogram', command=create_histogram, width = 20)
create_histogram_buttom.grid(row=9, column=0)

quit = tk.Button(buttons_frame, text="QUIT", fg="red", command=root.destroy, width=20)
quit.grid(row=10, column=0)


# GUI MAIN LOOP
root.mainloop()

