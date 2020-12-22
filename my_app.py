import tkinter as tk
from tkinter import ttk
import sqlite3

def run_sql_command():
    conn = sqlite3.connect('delivery.db')
    cursor = conn.cursor()
    command = SQL_command_entry.get()
    try:
        cursor.execute(command)
        result = cursor.fetchall()
        #query_return.config(text=result)
        for row in result:
            print(row) # it print all records in the database
            my_tree.insert("", tk.END, values=row)
    except:
        print('Error')
    conn.close()

def show_all_tables(DATABASE_NAME = 'delivery.db'):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute(''' SELECT name FROM sqlite_master WHERE type='table';''')
        conn.commit()
        result = cursor.fetchall()
        for row in result:
            print(row) # it print all records in the database
            my_tree.insert("", tk.END, values=row)
    except:
            print('Error')
    conn.close()


# ##### gui code ####

root = tk.Tk()
root.geometry('700x450')
root.title('SQLite gui')

# SETTING THE LABELS AND ENTRIES
SQL_command_label = tk.Label(root, text='SQL command')
SQL_command_label.grid(row=0, column=0, padx=0)

SQL_command_entry = tk.Entry(root, width=50)
SQL_command_entry.grid(row=0, column=1, padx=0)

# query_return = tk.Label(root, text='', bg='red', width=50, height=5)

# setting return treeview:
my_tree = ttk.Treeview(root)
my_tree['columns'] = ('index','customer_id','genre','status','verified','created_at')

# format columns
my_tree.column('#0', width=0)
my_tree.column('index', anchor='w', width=50)
my_tree.column('customer_id', anchor='center', width=100)
my_tree.column('genre', anchor='center', width=80)
my_tree.column('status', anchor='center', width=50)
my_tree.column('verified', anchor='center', width=50)
my_tree.column('created_at', anchor='center', width=150)

# create headings
my_tree.heading('#0', text='', anchor='w')
my_tree.heading('index', text='index', anchor='w')
my_tree.heading('customer_id', text='customer_id', anchor='center')
my_tree.heading('genre', text='genre', anchor='center')
my_tree.heading('status', text='status', anchor='center')
my_tree.heading('verified', text='verified', anchor='center')
my_tree.heading('created_at', text='created_at', anchor='center')

# add data
my_tree.insert(parent='', index='end', iid=0, text='', values=())

my_tree.grid(row=3, column=1)

# SETTING BUTTONs
run = tk.Button(text="Run", command=run_sql_command, width = 10)
run.grid(row=2, column=0, padx=5)

show_info = tk.Button(text='schema_info', command=show_all_tables)
show_info.grid(row=1, column=0)

quit = tk.Button(text="QUIT", fg="red", command=root.destroy)
quit.grid(row=5, column=0)


# GUI MAIN LOOP
root.mainloop()

