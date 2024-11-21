import sqlite3

connection = sqlite3.connect("index.db")

cursor = connection.cursor()

## create table command
def createTable(tableName, priKey) -> None:
    command = "CREATE TABLE IF NOT EXISTS{0}({1} INTEGER PRIMARY KEY)".format(
        tableName, priKey)
    
    cursor.execute(command)

## get data
def getAll(tableName) -> list:
    cursor.execute("SELECT * FROM ?",(tableName))
    results = cursor.fetchall()
    return results

## add data
def addData(tableName, data) -> None:
    cursor.execute("INSERT INTO ? VALUES (?)", (tableName, data))

## del one data entry
def delOne(tableName, data) -> None:
    cursor.execute("DELETE FROM ? WHERE")

## Get specific data
def getOne(tableName, queryType, query):
    cursor.execute("SELECT ?  FROM ? WHERE ?", (queryType, tableName, query))


## Commit changes
def commit():
    connection.commit()

## Undo changes
def undo():
    connection.rollback()

## Close
def close():
    connection.close()
