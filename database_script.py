import sqlite3

# for all tables no index is stated, since by default SQLite creates rowid

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
    vendor_tag_name TEXT,
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
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute(sql_command)
    # commit our command
    conn.commit()
    # close our connection
    conn.close()

def show_all_tables(DATABASE_NAME = 'delivery.db'):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute(''' SELECT name FROM sqlite_master WHERE type='table';''')
    conn.commit()
    result = cursor.fetchall()
    for item in result:
        print(item)
    # close our connection
    conn.close()

def show_table_info(table_name, DATABASE_NAME = 'delivery.db'):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute(f''' PRAGMA table_info({table_name}) ''')
    conn.commit()
    result = cursor.fetchall()
    for item in result:
        print(item)
    # close our connection
    conn.close()

def show_table_rows(table_name, rows = 100):
    conn = sqlite3.connect('delivery.db')
    cursor = conn.cursor()
    cursor.execute(f''' SELECT * FROM {table_name} LIMIT {rows};''')
    conn.commit()
    for row in cursor.fetchall():
        print (row)
    conn.close()

def delete_table(table_name, DATABASE_NAME = 'delivery.db'):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute(f''' DROP TABLE {table_name}; ''')
    conn.commit()
    conn.close()

# create_table(sql_command_CREATE_CUSTOMERS)
# create_table(sql_command_CREATE_LOCATIONS)
# create_table(sql_command_CREATE_VENDORS)
# create_table(sql_command_CREATE_ORDERS)

# delete_table('customers')
# delete_table('vendors')
# delete_table('locations')
# delete_table('orders')


show_all_tables()
print('cid # name # type # notnull # dflt_value # pk')
print('=========')
show_table_info('customers')
print('=========')
show_table_info('orders')
print('=========')
show_table_info('locations')
print('=========')
show_table_info('vendors')





