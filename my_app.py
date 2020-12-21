from database_script import *
from tkinter import ttk
import tkinter as tk
import sqlite3

def run_sql_command():
    connection = sqlite3.connect('delivery.db')
    cursor = connection.cursor()
    command = SQL_command_entry.get()
    try:
        cursor.execute(command)
        result = cursor.fetchall()
        query_return.config(text=result)
        for r in result:
            #
            print(r)

    except:
        print('Error')
        query_return.config(text='ERROR')

# def mean():
#     cursor.execute('SELECT this FROM this // ')
#     mean(....)

##### gui code ####

root = tk.Tk()
root.minsize(300, 350)
root.title('SQLite gui')

# SETTING THE LABELS AND ENTRIES
SQL_command_label = tk.Label(root, text='SQL command')
SQL_command_entry = tk.Entry(root, width=50)

query_return = tk.Label(root, text='', bg='green', fg='white', width=50, height=5)

# SETTING BUTTON
run = tk.Button(text="Run", command=run_sql_command)
quit = tk.Button(text="QUIT", fg="red", command=root.destroy)

SQL_command_label.pack()
SQL_command_entry.pack()
query_return.pack(pady=20)
run.pack()
quit.pack(pady=20)
# GUI MAIN LOOP
root.mainloop()

# class MyFirstGUI(tk.Frame):
#     def __init__(self, master):
#         self.root = root
#         root.title("SQLite GUI")
#         root.minsize(400, 350)

#         self.sql_command_label = tk.Label(root, text="SQL command")
#         self.sql_command_label.pack()

#         self.SQL_command_entry = tk.Entry(root, width=50)
#         self.SQL_command_entry.pack()

#         self.query_return = tk.Label(root, text='', bg='green', fg='white', width=50, height=5)
#         self.query_return.pack()

#         self.run = tk.Button(text="Run", command=run_sql_command())
#         self.run.pack()

#         self.close_button = tk.Button(root, text="Close",  fg="red", command=root.quit)
#         self.close_button.pack()
