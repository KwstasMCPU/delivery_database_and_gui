import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime


def show_all_customers():
    """
    This functions is assigned to the show_all_customers_button.
    Passes the relevant table name ('customers') to select_all_from function.
    Then calls the create_trees function, passing to it the results of the select_all_from function
    """
    column_names_ls = show_table_column_names('customers')
    sql_command = '''SELECT * FROM customers LIMIT 100; '''
    create_trees(column_names_ls, sql_command)

def show_all_vendors():
    """
    This functions is assigned to the show_all_vendors_button.
    Passes the relevant table name ('vendors') to select_all_from function.
    Then calls the create_trees function, passing to it the results of the select_all_from function
    """
    column_names_ls = show_table_column_names('vendors')
    sql_command = '''SELECT * FROM vendors LIMIT 100; '''
    create_trees(column_names_ls, sql_command)

def show_all_orders():
    """
    This functions is assigned to the show_all_orders_button.
    Passes the relevant table name ('orders') to select_all_from function.
    Then calls the create_trees function, passing to it the results of the select_all_from function
    """
    column_names_ls = show_table_column_names('orders')
    sql_command = '''SELECT * FROM orders LIMIT 100; '''
    create_trees(column_names_ls, sql_command)

def show_all_locations():
    """
    This functions is assigned to the show_all_locations_button.
    Passes the relevant table name ('locations') to select_all_from function.
    Then calls the create_trees function, passing to it the results of the select_all_from function
    """
    column_names_ls = show_table_column_names('locations')
    sql_command = '''SELECT * FROM orders LIMIT 100; '''
    create_trees(column_names_ls, sql_command)

def show_table_column_names(table_name):
    '''
    Returns the column names of the given table.

            Parameters:
                    table_name (str): the name of the table. Is given by the relevant button the user pressed.
            Returns:
                    column_name_ls (list): a list of the column names (str) of the given tables.
    '''
    conn = sqlite3.connect('delivery.db')
    cursor = conn.cursor()
    cursor.execute(f''' PRAGMA table_info({table_name}); ''') # PRAGMA table_info returns information about the given table, such as the table column names. https://www.sqlite.org/pragma.html#pragma_table_info
    conn.commit()
    table_info = cursor.fetchall()
    column_name_ls = []
    for row in table_info:
        column_name_ls.append(row[1]) # the row format is (column number, column name, data type, is a column can be null, default value of the column, if column is a primary key ), thus the item in index 1 is the column name
    conn.close
    return column_name_ls

def create_trees(column_name_ls, sql_command):
    """
    Creates treeview widgets, and depicts them on the GUI.
    Its time user presses a select {table_name} button, a new treeview widget is created,
    while the previous is un grided and deleted.
    Then the treeview is populated by the data of the relevant table.
    The results are limited to the first 100 rows.
            Parameters:
                        column_name_ls (list): a list of the column names (str) of the given tables.
    """
    global my_tree # the tree was made as a global variable in order to remove the previous generated tkk.Treeview object, otherwise more objects will be created, the newer atop the older ones.
    try:
        my_tree.grid_forget()
        del my_tree # the previous treeview instance is deleted to save memory
    except:
        pass
    my_tree = ttk.Treeview(treeview_frame)
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
        cursor.execute(sql_command)
        conn.commit
        result = cursor.fetchall()
        for row in result:
            my_tree.insert("", tk.END, values=row)
        my_tree.grid(row=0, column=0, rowspan=8, columnspan=10)
        conn.close()
    except Exception as e:
        print(e)
        label_screen.config(text=e)

def show_all_table_names():
    """
    This function is assigned to the show_table_names button.
    Shows in the label_screen all the tables of the database.
    """
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

def entry_customers():
    """
    Inserts a new customer into the customers table.
    The new customer's details are given through the respective entry labels.
    If no customer_id is given, error message pops to the label_screen.
    """
    conn = sqlite3.connect('delivery.db')
    cursor = conn.cursor()
    # getting the entries from the user input
    customer_id = customer_id_entry.get()
    gender = customer_gender_entry.get()
    status = customer_status_entry.get()
    verified = customer_verified_entry.get()
    dateTimeObj = datetime.now() # creating a datetime object to use it as the created_at variable of the customers table
    created_at = dateTimeObj.strftime("%Y-%m-%d %H:%M:%S") # format it to '2020-12-01 16:02:05'
    data_tuple = (customer_id, gender, status, verified, created_at)
    if not customer_id:
        label_screen.config(text='Give Customer ID', fg='red')
    else:
        cursor.execute(f'''INSERT INTO customers (customer_id, gender, status, verified, created_at) VALUES(?, ?, ?, ?, ?);''', data_tuple)
        label_screen.config(text=f'New customer with: {data_tuple}, inserted.')
    conn.commit()
    conn.close()

def create_histogram():
    """
    Creates a histogram for the deliverydistance column.
    Firstly loads the deliverydistance as a pd.Dataframe with the pandas.read_sql_query()
    and then the  FigureCanvasTkAgg to embed the figure into the tkinter GUI
    """
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
    '''
    Calculates the mean of the item_count column in the orders table,
    and returns it in the label_screen, formated as a float with 4 decimals
    '''
    conn = sqlite3.connect('delivery.db')
    df = pd.read_sql_query(''' SELECT item_count FROM orders ''', conn )
    label_screen.config(text="{:.4f}".format(df['item_count'].mean()))

def mean_grand_total():
    '''
    Calculates the mean of the grand_total column in the orders table,
    and returns it in the label_screen, formated as a float with 4 decimals
    '''
    conn = sqlite3.connect('delivery.db')
    df = pd.read_sql_query(''' SELECT grand_total FROM orders ''', conn )
    label_screen.config(text="{:.4f}".format(df['grand_total'].mean())) # formats the float to 4 decimals

def run_sql_command():
    """
    This function runs an SQL command, the user has typed into the sql_command_entry entry label.
    If its a 'SELECT' query, the result is shown in the treeview widget.
    Else it returns success message in the label_screen.
    Cannot handle SELECT * command
    """
    conn = sqlite3.connect('delivery.db')
    cursor = conn.cursor()
    sql_command = sql_command_entry.get()
    try:
        if sql_command.split()[0].upper() == 'SELECT': # check if the first word is SELECT, show we need to return the results to the treeview
            table_name = sql_command.split()[3]
            try:
                column_names_ls = show_table_column_names(table_name)
                create_trees(column_names_ls, sql_command)
            except Exception as e:
                label_screen.config(text=e)
        else:
            try:
                cursor.execute(sql_command)
                conn.commit()
                conn.close()
                confirmation_message = (", ".join([f'{sql_command}','runned successfully.']))
                label_screen.config(text=confirmation_message)
                print(confirmation_message)
            except Exception as e:
                label_screen.config(text=e)
    except Exception as e:
        label_screen.config(text=e)

# ##### gui code ####

root = tk.Tk()
root.geometry('1300x600')
root.title('SQLite gui')

buttons_frame = tk.Frame(root, highlightbackground='grey'  ,highlightthickness=1, padx=5, pady=5)
buttons_frame.grid(row=0, column=0, rowspan=10)

sql_entry_and_screen_frame = tk.LabelFrame(root, text='SQL Command', padx=5, pady=5)
sql_entry_and_screen_frame.grid(row=0, column=1, rowspan=2)

treeview_frame = tk.LabelFrame(root, text='Output window', padx=5, pady=5)
treeview_frame.grid(row = 2, column = 1)

down_frame = tk.LabelFrame(root, text="Insert new customer's details", padx=5, pady=5)
down_frame.grid(row = 9, column=1)

plot_frame = tk.LabelFrame(root, text='Delivery distance histogram', highlightbackground='black', highlightthickness=1, padx=5, pady=5)
plot_frame.grid(row=11, column = 1, columnspan=3)

dummy_columns = [x for x in range(0,7)]
my_tree = ttk.Treeview(treeview_frame, columns=dummy_columns)
my_tree['columns'] = (dummy_columns)
my_tree.column('#0', width=0)
my_tree.heading('#0', text='', anchor='w')
for column in dummy_columns:
    my_tree.column(column, stretch=False, width=95)
    my_tree.heading(column, text=column, anchor='w')
my_tree.grid(row=0, column=0, rowspan=8, columnspan=10)


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

show_all_table_names_button = tk.Button(buttons_frame, text='Table names', command=show_all_table_names, width= 20)
show_all_table_names_button.grid(row=1, column=0)

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



