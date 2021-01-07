import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg # FigureCanvasTkAgg is needed in order to draw a matplotlib graph on a tkitner application
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

def show_all_customers():
    """
    This functions is assigned to the show_all_customers_button.
    Passes the relevant table name ('customers') to select_all_from function.
    Then calls the create_trees function, passing to it the results of the select_all_from function and the sql_command,
    in order to show the first 100 rows of the customers table
    """
    column_names_ls = show_table_column_names('customers')
    sql_command = '''SELECT * FROM customers LIMIT 100; '''
    create_trees(column_names_ls, sql_command)

def show_all_vendors():
    """
    This functions is assigned to the show_all_vendors_button.
    Passes the relevant table name ('vendors') to select_all_from function.
    Then calls the create_trees function, passing to it the results of the select_all_from function and the sql_command,
    in order to show the first 100 rows of the vendors table
    """
    column_names_ls = show_table_column_names('vendors')
    sql_command = '''SELECT * FROM vendors LIMIT 100; '''
    create_trees(column_names_ls, sql_command)

def show_all_orders():
    """
    This functions is assigned to the show_all_orders_button.
    Passes the relevant table name ('orders') to select_all_from function.
    Then calls the create_trees function, passing to it the results of the select_all_from function and the sql_command,
    in order to show the first 100 rows of the orders table
    """
    column_names_ls = show_table_column_names('orders')
    sql_command = '''SELECT * FROM orders LIMIT 100; '''
    create_trees(column_names_ls, sql_command)

def show_all_locations():
    """
    This functions is assigned to the show_all_locations_button.
    Passes the relevant table name ('locations') to select_all_from function.
    Then calls the create_trees function, passing to it the results of the select_all_from function and the sql_command,
    in order to show the first 100 rows of the locations table
    """
    column_names_ls = show_table_column_names('locations')
    sql_command = '''SELECT * FROM locations LIMIT 100; '''
    create_trees(column_names_ls, sql_command)

def show_table_column_names(table_name):
    '''
    Returns the column names of the given table.

            Parameters:
                    table_name (str): the name of the table. Is given by the relevant button the user pressed.
            Returns:
                    column_name_ls (list): a list of the column names (str) of the given tables. This is used in
                    create_trees function, in order to create the column names of the treeview object on the tkinter application
    '''
    conn = sqlite3.connect('delivery.db')
    cursor = conn.cursor()
    cursor.execute(f''' PRAGMA table_info({table_name}); ''') # PRAGMA table_info returns information about the given table, such as the table column names. https://www.sqlite.org/pragma.html#pragma_table_info
    conn.commit()
    table_info = cursor.fetchall()
    column_name_ls = []
    for row in table_info:
        column_name_ls.append(row[1]) # the item in index 1 is the column's name
    conn.close
    return column_name_ls

def create_trees(column_name_ls, sql_command):
    """
    Creates treeview widgets, and depicts them on the GUI.
    Every time the user presses a select table button, a new treeview widget is created,
    while the previous is un grided and deleted.
    Then the treeview is populated by the data of the relevant table.
    The results are limited to the first 100 rows.
    Also shows the data of the queries the user has typed in the sql_command_entry Entry
        Parameters:
            column_name_ls (list): a list of the column names (str) of the given tables.
            sql_command (str): the SQL command to be executed
    """
    global my_tree         # the tree was made as a global variable in order to remove the previous generated tkk.Treeview object, otherwise more objects will be created, the newer atop the older ones.
    global tree_scroll_y   # same as above but for the y axis scroll bar
    global tree_scroll_x   # same as above but for the x axis scroll bar
    # try to forget and delete the first instances of my_tree and the scroll bars
    try:
        my_tree.grid_forget()
        tree_scroll_y.grid_forget()
        tree_scroll_x.grid_forget()
        del my_tree # the previous treeview instance is deleted to save memory
        del tree_scroll_y
        del tree_scroll_x
    except:
        pass
    my_tree = ttk.Treeview(treeview_frame) # create a treeview object in the treeview_frame
    my_tree['columns'] = (column_name_ls) # assign to the column names of the treeview the column names of the relevant database table
    my_tree.column('#0', width=0) # The tkinter.TreeView has a first default column (identifier #0). its the first column (like a treeview index), we set it to minimum width in order not to be visible
    # using a for loop to create as many columns in the treeview as the selected database table, and assign the its relevant column names to them
    for column in column_name_ls:
        my_tree.column(column, stretch=False, width=95) # its column have a fixed width to 95, with no resize even if the widget size is changed (see: https://docs.python.org/3/library/tkinter.ttk.html)
        my_tree.heading(column, text=column, anchor='w') # setting column names, and their position (west)
    my_tree.insert(parent='', index='end', iid=0, text='', values=()) # since there is no parent-child relationship we set parent=''. The values will be inserted at row 123
    # Treeview scrollbar y-axis
    tree_scroll_y = ttk.Scrollbar(treeview_frame, orient='vertical', command=my_tree.yview)
    tree_scroll_y.grid(row=0, column=1, sticky='nse')
    my_tree.configure(yscrollcommand=tree_scroll_y.set)
    # Treeview scrollbar x-axis
    tree_scroll_x = ttk.Scrollbar(treeview_frame, orient='horizontal', command=my_tree.xview)
    tree_scroll_x.grid(row=1, column=0, sticky='swe')
    my_tree.configure(xscrollcommand=tree_scroll_x.set)
    try:
        conn = sqlite3.connect('delivery.db')
        cursor = conn.cursor()
        cursor.execute(sql_command)
        conn.commit
        result = cursor.fetchall()
        for row in result:
            # insert data to the treeview
            my_tree.insert("", tk.END, values=row) # inserting the results of the query to the treeview
        my_tree.grid(row=0, column=0, rowspan=8, columnspan=10)
        conn.close()
    except Exception as e:
        print(e)
        label_screen.config(text=e, font='Helvetica 9 bold', fg='red')

def show_all_table_names():
    """
    This function is assigned to the show_table_names button.
    Shows on the label_screen all the tables of the database.
    """
    conn = sqlite3.connect('delivery.db')
    cursor = conn.cursor()
    try:
        cursor.execute(''' SELECT name FROM sqlite_master WHERE type='table';''')
        conn.commit()
        result = cursor.fetchall()
        print(result)
        label_screen.config(text= result, font='Helvetica 9 bold', fg='white')
    except Exception as e:
        label_screen.config(text=e, font='Helvetica 9 bold', fg='red')
    conn.close()

def entry_customers():
    """
    Inserts a new customer into the customers table.
    The new customer's details are given through the respective entry labels.
    If no customer_id is given, error message pops to the label_screen.
    If no proper values for gender, status or verified is given, error appears on the label_screen. (can receive null values)
    """
    conn = sqlite3.connect('delivery.db')
    cursor = conn.cursor()
    # getting the entries the user typed
    customer_id = customer_id_entry.get()
    gender = customer_gender_entry.get()
    gender = gender.upper() # format to uppercase
    if gender == '':    # Blank values are converted to None type since, our database stores and depicts blank values as None.
        gender = None
    status = customer_status_entry.get()
    if status == '':
        status = None
    verified = customer_verified_entry.get()
    if verified == '':
        verified = None
    try:
        status = int(status) # try to convert them to integers, since they are stored as int in our database
        verified = int(verified)
    except Exception as e:
        print(e)
    dateTimeObj = datetime.now() # creating a datetime object to use it as the created_at variable of the customers table
    created_at = dateTimeObj.strftime("%Y-%m-%d %H:%M:%S") # format it to '2020-12-01 16:02:05'
    data_tuple = (customer_id, gender, status, verified, created_at)
    # handling wrong entry values
    if not customer_id: # no customer_id is given
        label_screen.config(text='Give Customer ID', font='Helvetica 9 bold', fg='red')
    else:
        if not (status in [1,0,None] and verified in [1,0,None]):
            label_screen.config(text='status and verified can receive only 1, 0 values or left empty', font='Helvetica 9 bold',  fg='red')
        else:
            if gender not in ['M', 'F',None]:
                label_screen.config(text='gender can receive only M or F values or left empty', font='Helvetica 9 bold', fg='red')
            else:
                try:
                    cursor.execute(f'''INSERT INTO customers (customer_id, gender, status, verified, created_at) VALUES(?, ?, ?, ?, ?);''', data_tuple)
                    label_screen.config(text=f'New customer with: {data_tuple}, inserted.', font='Helvetica 9 bold', fg='green')
                except Exception as e:
                    print(e)
                    label_screen.config(text=e, font='Helvetica 9 bold', fg='red')
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
    conn = sqlite3.connect('delivery.db')
    df = pd.read_sql_query(''' SELECT deliverydistance FROM orders ''', conn ) # Returns a DataFrame corresponding to the result set of the query string
    f, ax = plt.subplots(figsize=(4, 4)) # initialise the plot and setting its size
    df['deliverydistance'].hist(bins=40) # create a histogram with 40 bins
    for label in (ax.get_xticklabels() + ax.get_yticklabels()): # seting y and x label values size
	    label.set_fontsize(8)
    ax.set_xlim(right=16)   # seting the right limit of our plot to 16, since there was a bit of extra white space
    plt.gcf().subplots_adjust(left=0.18) # adjusting the plot so the y title label fit within the frame
    plt.title('Delivery distance distribution', fontsize=10)
    plt.ylabel('Counts', fontsize=9)
    plt.xlabel('Delivery distance', fontsize=9)
    canvas = FigureCanvasTkAgg(f, master=plot_frame)  # setting the tk.DrawingArea
    canvas.draw()
    canvas.get_tk_widget().grid() # row = 2, column = 10, columnspan=3

def mean_item_count():
    '''
    Calculates the mean of the item_count column in the orders table,
    and returns it in the label_screen, formated as a float with 4 decimals
    '''
    conn = sqlite3.connect('delivery.db')
    df = pd.read_sql_query(''' SELECT item_count FROM orders ''', conn ) # Returns a DataFrame corresponding to the result set of the query string
    label_screen.config(text="Mean item_count = "+"{:.4f}".format(df['item_count'].mean()),  # calculates the mean and format it to float with 4 decimals. By default mean() skip nan values in the calculation
                        font='Helvetica 9 bold', fg='white')

def mean_grand_total():
    '''
    Calculates the mean of the grand_total column in the orders table,
    and returns it in the label_screen, formated as a float with 4 decimals
    '''
    conn = sqlite3.connect('delivery.db')
    df = pd.read_sql_query(''' SELECT grand_total FROM orders ''', conn ) # Returns a DataFrame corresponding to the result set of the query string
    label_screen.config(text="Mean grand_total = "+"{:.4f}".format(df['grand_total'].mean()), # calculates the grand_total and format it to float with 4 decimals. By default mean() skip nan values in the calculation
                        font='Helvetica 9 bold', fg='white')

def run_sql_command():
    """
    This function runs an SQL command, the user has typed into the sql_command_entry entry label.
    If its a 'SELECT' query, the result is shown in the treeview widget.
    Else it returns success message in the label_screen.
    Note that cannot handle 'SELECT *' command, or depict correctly column names only if few of them are selected
    """
    conn = sqlite3.connect('delivery.db')
    cursor = conn.cursor()
    sql_command = sql_command_entry.get()
    try:
        if sql_command.split()[0].upper() == 'SELECT': # check if the first word is SELECT
            table_name = sql_command.split()[3] # e.g. if there is an SELECT query the element in the index number 3 will be the table name
            try:
                column_names_ls = show_table_column_names(table_name)
                create_trees(column_names_ls, sql_command) # calling create trees function to show the results of the query
            except Exception as e:
                label_screen.config(text=e, font='Helvetica 9 bold', fg='red')
        # in case the query does not start with SELECT statement
        else:
            try:
                cursor.execute(sql_command)
                conn.commit()
                confirmation_message = (", ".join([f'{sql_command}','ran successfully.']))
                label_screen.config(text=confirmation_message, font='Helvetica 9 bold', fg='green')
                print(confirmation_message)
                result = cursor.fetchall()
                print(result)
            except Exception as e:
                label_screen.config(text=e, font='Helvetica 9 bold', fg='red')
    except Exception as e:
        label_screen.config(text=e, font='Helvetica 9 bold', fg='red')
    conn.close()

############################## GUI CODE #############################################

# initializing the tkinter application
root = tk.Tk()
# setting window length and height
root.geometry('1600x600')
# giving a title to the window
root.title('SQLite gui')

# setting the frames

buttons_frame = tk.LabelFrame(root, text='Tools', padx=8, pady=8)
buttons_frame.grid(row=0, column=0, rowspan=10, columnspan=1, sticky="WN")
buttons_frame.grid_columnconfigure(0, weight=1)
buttons_frame.grid_rowconfigure(0, weight=1)

sql_entry_and_screen_frame = tk.LabelFrame(root, text='SQL Command', padx=5, pady=5)
sql_entry_and_screen_frame.grid(row=0, column=1, rowspan=2, columnspan=2, sticky="N")
sql_entry_and_screen_frame.grid_columnconfigure(0, weight=1)
sql_entry_and_screen_frame.grid_rowconfigure(0, weight=1)


treeview_frame = tk.LabelFrame(root, text='Output window', padx=5, pady=5)
treeview_frame.grid(row=3, column=1, rowspan=8, columnspan=9, sticky='W')
treeview_frame.grid_columnconfigure(0, weight=1)
treeview_frame.grid_rowconfigure(0, weight=1)

down_frame = tk.LabelFrame(root, text="Insert new customer's details", padx=5, pady=5)
down_frame.grid(row = 11, column=1)
down_frame.grid_columnconfigure(0, weight=1)
down_frame.grid_rowconfigure(0, weight=1)

plot_frame = tk.LabelFrame(root, text='Delivery distance histogram', padx=2, pady=5)
plot_frame.grid(row=3, column = 11, rowspan=6, columnspan=4, sticky='WN')
plot_frame.grid_columnconfigure(0, weight=1)
plot_frame.grid_rowconfigure(0, weight=1)

# creating a dummy treeview object
# the purpose of creating a dummy treeview and canvas is to fill the empty space when the application is initialized
# Treeview (return table data)
dummy_columns = [x for x in range(0,7)]
my_tree = ttk.Treeview(treeview_frame, columns=dummy_columns)
my_tree['columns'] = (dummy_columns)
my_tree.column('#0', width=0)
my_tree.heading('#0', text='', anchor='w')
for column in dummy_columns:
    my_tree.column(column, stretch=False, width=95)
    my_tree.heading(column, text=column, anchor='w')
my_tree.grid(row=0, column=0, rowspan=8, columnspan=10)

# Treeview scrollbar y-axis
tree_scroll_y = ttk.Scrollbar(treeview_frame, orient='vertical', command=my_tree.yview)
tree_scroll_y.grid(row=0, column=1, sticky='nse')
my_tree.configure(yscrollcommand=tree_scroll_y.set)

# Treeview scrollbar x-axis
tree_scroll_x = ttk.Scrollbar(treeview_frame, orient='horizontal', command=my_tree.xview)
tree_scroll_x.grid(row=1, column=0, sticky='swe')
my_tree.configure(xscrollcommand=tree_scroll_x.set)

# empty canvas for the plot
canvas = tk.Canvas(master=plot_frame, bg='white', height=400, width=400)
canvas.grid()


# setting the labels and entries

sql_command_entry = tk.Entry(sql_entry_and_screen_frame, width=70, selectborderwidth=5)
sql_command_entry.grid(row=0, column=3)

label_screen = tk.Label(sql_entry_and_screen_frame, bg='black', fg='white', width=70)
label_screen.grid(row=1, column=3)

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

# setting the buttons

sql_command_run_button = tk.Button(sql_entry_and_screen_frame, text='Run command', command=run_sql_command, width=20)
sql_command_run_button.grid(row=0, column=2)

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

entry_customers_button = tk.Button(down_frame, text="Entry customers", command=entry_customers, width = 20)
entry_customers_button.grid(row=10)

create_histogram_buttom = tk.Button(buttons_frame, text='Create histogram', command=create_histogram, width = 20)
create_histogram_buttom.grid(row=9, column=0)

quit = tk.Button(buttons_frame, text="QUIT", fg="red", command=root.quit, width=20)
quit.grid(row=10, column=0)


# gui main loop
root.mainloop()
root.destroy()



