#!/usr/bin/env python
import signal
import sys
import mariadb
import sys

# signal handler for easy cut off
def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    sys.exit(1)
signal.signal(signal.SIGINT, signal_handler)

#connection to database
conn = mariadb.connect(
    user="db_user",
    password="db_user_passwd",
    host="localhost",
    database="employees")
cur = conn.cursor() 

#retrieving information 
some_name = "Georgi" 
cur.execute("SELECT first_name,last_name FROM employees WHERE first_name=?", (some_name,)) 

for first_name, last_name in cur: 
    print(f"First name: {first_name}, Last name: {last_name}")
    
#insert information 
try: 
    cur.execute("INSERT INTO employees (first_name,last_name) VALUES (?, ?)", ("Maria","DB")) 
except mariadb.Error as e: 
    print(f"Error: {e}")

#commit changes
conn.commit() 
print(f"Last Inserted ID: {cur.lastrowid}")

#By default, MariaDB Connector/Python enables auto-commit
# Disable Auto-Commit
#conn.autocommit = False

#close connection after we are done
conn.close()
