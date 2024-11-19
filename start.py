print('Hello World')
print('You suck')

import sqlite3

connection = sqlite3.connect("index.db")

cursor = connection.cursor()

## create table command
command = """CREATE TABLE IF NOT EXISTS
test(test_id INTEGER PRIMARY KEY) """
cursor.execute(command)

cursor.execute("INSERT INTO <TABLE NAME> VALUES (...)")

## get data
cursor.execute("SELECT * FROM <TABLE>")
results = cursor.fetchall()
print(results)