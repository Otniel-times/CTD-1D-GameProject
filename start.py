print('Hello World')
print('You suck')

import sqlite3

connection = sqlite3.connect("index.db")
print(connection.total_changes)