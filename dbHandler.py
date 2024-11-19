import sqlite3

connection = sqlite3.connect("index.db")

cursor = connection.cursor()

## create table command
def createTable():
    command = """CREATE TABLE IF NOT EXISTS
    test(test_id INTEGER PRIMARY KEY) """
    cursor.execute(command)

    cursor.execute("INSERT INTO <TABLE NAME> VALUES (...)")

## get data
def getAll(tableName):
    cursor.execute("SELECT * FROM {}",tableName)
    results = cursor.fetchall()
    return results
