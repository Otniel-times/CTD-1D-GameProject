import sqlite3

connection = sqlite3.connect("index.db")

cursor = connection.cursor()

## create table command
def createTable():
    cursor.execute("DROP TABLE IF EXISTS playerInfo")
    command = """CREATE TABLE "playerInfo"(
	"id"	INTEGER NOT NULL,
	"firstName"	VARCHAR(255) NOT NULL,
	"lastName"	VARCHAR(255) NOT NULL,
	"userName"	VARCHAR(255) NOT NULL,
	"score"	INTEGER,
	PRIMARY KEY("id" AUTOINCREMENT)
) """
    cursor.execute(command)
    print("Table created successfully.")
    connection.commit()
    connection.close()
##########################################
def getAll():
    try:
        cursor.execute("SELECT * FROM playerInfo")
        results = cursor.fetchall()
        return results
    except sqlite3.Error as e: print(e)

# def bruteforce():
#     try:
#         command = """INSERT INTO playerInfo (firstName, lastName, userName, score) VALUES ('john', 'doe','johnny', 3)"""
#         cursor.execute(command)
#         print("Row inserted.")
#         connection.commit()
#         connection.close
#     except sqlite3.Error as e: print(e)

def getall_username_n_score():
   try:
      command = """SELECT userName, score FROM playerInfo"""
      cursor.execute(command)
      results = cursor.fetchall()
      return results
   except sqlite3.Error as e: print("Failed to retrieve data from table.", e)
   finally:
      if connection:
         connection.close()

def getall_username():
   try:
      command = """SELECT userName FROM playerInfo"""
      cursor.execute(command)
      results = cursor.fetchall()
      return results
   except sqlite3.Error as e: print("Failed to retrieve data from table.", e)
   finally:
      if connection:
         connection.close()
         
def getall_score():
   try:
      command = """SELECT score FROM playerInfo"""
      cursor.execute(command)
      results = cursor.fetchall()
      return results
   except sqlite3.Error as e: print("Failed to retrieve data from table.", e)
   finally:
      if connection:
         connection.close()

def getUSERNAME_by_userName(u):
    try: 
        command = """SELECT userName FROM playerInfo WHERE userName =?"""
        cursor.execute(command, (u,))
        result = cursor.fetchone() 
        if result:
         return result
        else: return "User does not exist."
    except sqlite3.Error as e: return e

def getUSERNAME_by_id(uid):
    try: 
        command = """SELECT userName FROM playerInfo WHERE id =?"""
        cursor.execute(command, (uid,))
        result = cursor.fetchone() 
        if result:
         return result
        else: return "User does not exist."
    except sqlite3.Error as e: return e

def getUSERNAME_by_firstName_plus(firstName): ## Gets all record with identical first names
    try: 
        command = """SELECT userName FROM playerInfo WHERE firstName =?"""
        cursor.execute(command, (firstName,))
        result = cursor.fetchall() 
        if result:
         return result
        else: return "User does not exist."
    except sqlite3.Error as e: return e

def getUSERNAME_by_firstName_pro(firstName): ## Gets the first record with specified firstName
    try: 
        command = """SELECT userName FROM playerInfo WHERE firstName =?"""
        cursor.execute(command, (firstName,))
        result = cursor.fetchone() 
        if result:
         return result
        else: return "User does not exist."
    except sqlite3.Error as e: return e

def getUSERNAME_by_lastName_plus(lastName): ## Gets all record with identical last names
    try: 
        command = """SELECT userName FROM playerInfo WHERE lastName =?"""
        cursor.execute(command, (lastName,))
        result = cursor.fetchall() 
        if result:
         return result
        else: return "User does not exist."
    except sqlite3.Error as e: return e

def getUSERNAME_by_lastName_pro(lastName): ## Gets the first record with specified lastName
    try: 
        command = """SELECT userName FROM playerInfo WHERE lastName =?"""
        cursor.execute(command, (lastName,))
        result = cursor.fetchone() 
        if result:
         return result
        else: return "User does not exist."
    except sqlite3.Error as e: return e

def update_userName_by_id(uid, new_u):
    try:
        command = """UPDATE playerInfo SET userName =? WHERE id =?"""
        cursor.execute(command, (new_u, uid,))
        connection.commit()
        connection.close()
    except sqlite3.Error as e: return e

def update_firstName_by_id(uid, new_n):
    try:
        command = """UPDATE playerInfo SET firstName =? WHERE id =?"""
        cursor.execute(command, (new_n, uid,))
        connection.commit()
        connection.close()
    except sqlite3.Error as e: return e

def update_lastName_by_id(uid, new_n):
    try:
        command = """UPDATE playerInfo SET lastName =? WHERE id =?"""
        cursor.execute(command, (new_n, uid,))
        connection.commit()
        connection.close()
    except sqlite3.Error as e: return e

def update_score_by_id(uid, new_s):
    try:
        command = """UPDATE playerInfo SET score =? WHERE id =?"""
        cursor.execute(command, (new_s, uid,))
        connection.commit()
        connection.close()
    except sqlite3.Error as e: return e

def delete_record_by_uid(uid):
    try:
        command = """DELETE FROM playerInfo WHERE id =?"""
        cursor.execute(command, (uid,))
        connection.commit()
        connection.close()
    except sqlite3.Error as e: return e
