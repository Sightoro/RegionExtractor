

# Import required modules
import csv
import sqlite3

# Connecting to the geeks database
connection = sqlite3.connect('addresses_database.db')

# Creating a cursor object to execute
# SQL queries on a database table
cursor = connection.cursor()

# Table Definition
create_table = '''CREATE TABLE addresses(
                Ind INTEGER,
                OPSName TEXT NOT NULL,
                OPSType TEXT NOT NULL, OPSSubm TEXT NOT NULL,
            Region TEXT NOT NULL, Autonom TEXT NOT NULL, Area TEXT
             NOT NULL, City TEXT NOT NULL, City1 TEXT NOT NULL, ActDate TEXT NOT NULL, IndexOld TEXT NOT NULL);
                '''

# Creating the table into our
# database
cursor.execute(create_table)

# Opening the person-records.csv file
file = open('addresses.csv', encoding = "ISO-8859-1")

# Reading the contents of the
# person-records.csv file
contents = csv.reader(file)

# SQL query to insert data into the
# person table
insert_records = "INSERT INTO addresses (Ind, OPSName, OPSType, OPSSubm,\
            Region, Autonom, Area, City, City1, ActDate, IndexOld) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

# Importing the contents of the file
# into our person table
cursor.executemany(insert_records, contents)

# SQL query to retrieve all data from
# the person table To verify that the
# data of the csv file has been successfully
# inserted into the table
select_all = "SELECT * FROM addresses"
rows = cursor.execute(select_all).fetchall()

# Output to the console screen
for r in rows:
    print(r)

# Committing the changes
connection.commit()

# closing the database connection
connection.close()