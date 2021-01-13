import sqlite3

'''
For all tables no index is stated, since by default SQLite creates rowid.

Furthermore SQLite uses a more general dynamic type system.
According to SQLite version 3 documentation : "In SQLite, the
datatype of a value is associated with the value itself, not 
with its container.Also SQLite uses data affinities, the type 
affinity of a column is the recommended type for data stored in that column."
That means that the type is recommended, not required. Any column can still store any type of data.
However the SQLite engine will try to convert it to the affinity type.
So the affinity type supported by SQLite v3 are going to be used. :

-TEXT
-NUMERIC
-INTEGER
-REAL
-BLOB

(see: https://www.sqlite.org/datatype3.html).
'''
sql_command_CREATE_CUSTOMERS = '''
CREATE TABLE customers (
    customer_id TEXT NOT NULL,
    gender TEXT,
    status INTEGER,
    verified  INTEGER,
    created_at TEXT,
    PRIMARY KEY (customer_id)
) ;'''

sql_command_CREATE_LOCATIONS = '''
CREATE TABLE locations (
    customer_id TEXT NOT NULL,
    location_number INTEGER NOT NULL,
    latitude REAL,
    longitude REAL,
    PRIMARY KEY (customer_id, location_number)
    FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
);'''

sql_command_CREATE_VENDORS = '''
CREATE TABLE vendors (
    vendor_id INTEGER NOT NULL,
    latitude REAL,
    longitude REAL,
    delivery_charge REAL,
    serving_distance REAL,
    rank REAL,
    vendor_rating REAL,
    opening_time TEXT,
    closing_time TEXT,
    PRIMARY KEY(vendor_id)
);'''

sql_command_CREATE_ORDERS = '''
CREATE TABLE orders (
    order_id REAL NOT NULL,
    customer_id TEXT NOT NULL,
    vendor_id INTEGER NOT NULL,
    location_number INTEGER,
    item_count REAL,
    grand_total REAL,
    payment_mode INTEGER,
    vendor_discount_amount REAL,
    deliverydistance REAL,
    delivered_time TEXT,
    created_at TEXT,
    PRIMARY KEY (order_id)
    FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
    FOREIGN KEY(vendor_id) REFERENCES vendors(vendor_id)
    FOREIGN KEY(location_number) REFERENCES locations(location_number)
);'''

####################################################################################

def create_table(sql_command, DATABASE_NAME = 'delivery.db'):
    """
    This function creates a database table to a database (to delivery.db by default)
    Parameters:
        sql_command (str): The sql command needed to create an SQLite table
        DATABASE_NAME (str): the name of the database the table to be created (default 'delivery.db')
    """
    # connect to the database
    conn = sqlite3.connect(DATABASE_NAME)
    # create the cursor
    cursor = conn.cursor()
    # execute the sql_command
    cursor.execute(sql_command)
    # commit our command
    conn.commit()
    # close our connection
    conn.close()

# UNCOMMENT THE CODE BELOW TO CREATE THE DATABASE'S TABLES
# create_table(sql_command_CREATE_CUSTOMERS)
# create_table(sql_command_CREATE_LOCATIONS)
# create_table(sql_command_CREATE_VENDORS)
# create_table(sql_command_CREATE_ORDERS)

