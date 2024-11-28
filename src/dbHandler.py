import sqlite3

## Start connection
def connect():
    """
    Starts connection, returns connection and cursor object

    :return val:    (tuple)
    """
    connection = sqlite3.connect("../index.db")
    cursor = connection.cursor()
    return connection, cursor


## create table command
def on_init():
    """
    Run on init to initialise both tables (playerInfo and playerItems)

    :return val: None
    """

    connection, cursor = connect()
    ## Run on init to initialise both tables

    command = """CREATE TABLE "playerInfo" (
    "id" INTEGER NOT NULL,
    "firstName" VARCHAR(255) NOT NULL,
    "lastName" VARCHAR(255) NOT NULL,
    "userName" VARCHAR(255) NOT NULL,
    "score" INTEGER,
    PRIMARY KEY ("id" AUTOINCREMENT))"""
    cursor.execute(command)
    print("Player Info created")

    command = """CREATE TABLE "playerItems" (
    "id" INTEGER PRIMARY KEY NOT NULL,
    "Anycubic" INT,
    "Bambu" INT,
    "DouinIonThrusters" INT,
    "November" INT,
    FOREIGN KEY("id") REFERENCES
    playerInfo ("id"))"""
    cursor.execute(command)
    print("Player items created")

    connection.commit()
    connection.close()

def create_table():

    """
    Creates playerInfo table

    :return val:    None
    """
    connection, cursor = connect()
    cursor.execute("DROP TABLE IF EXISTS playerInfo")
    command = """CREATE TABLE "playerInfo"(
	"id"	INTEGER NOT NULL,
	"firstName"	VARCHAR(255) NOT NULL,
	"lastName"	VARCHAR(255) NOT NULL,
	"userName"	VARCHAR(255) NOT NULL,
	"score"	INTEGER,
	PRIMARY KEY("id" AUTOINCREMENT)) """
    cursor.execute(command)
    print("Table created successfully.")
    connection.commit()
    connection.close()


## View general data
def get_all():
    """
    Get all data from playerInfo

    :return val:    (list)
    """

    connection, cursor = connect()
    try:
        cursor.execute("SELECT * FROM playerInfo")
        results = cursor.fetchall()
        return results
    except sqlite3.Error as e:
        print(e)

    finally:
        connection.close()

def getall_username_n_score():
    """
    Get all usernames and scores

    :return val:    (list)
    """
    
    connection, cursor = connect()
    try:
        command = """SELECT userName, score FROM playerInfo"""
        cursor.execute(command)
        results = cursor.fetchall()
        return results
    except sqlite3.Error as e:
        print("Failed to retrieve data from table.", e)

    finally:
        connection.close()

def getall_username():
    """
    Get all usernames

    :return val:    (list)
    """
    connection, cursor = connect()
    try:
        command = """SELECT userName FROM playerInfo"""
        cursor.execute(command)
        results = cursor.fetchall()
        return results
    except sqlite3.Error as e:
        print("Failed to retrieve data from table.", e)
    finally:
        connection.close()

def getall_score():
    """
    Get the scores of all users

    :return val:    (list)
    """
    connection, cursor = connect()
    try:
        command = """SELECT score FROM playerInfo"""
        cursor.execute(command)
        results = cursor.fetchall()
        return results
    except sqlite3.Error as e:
        print("Failed to retrieve data from table.", e)
    finally:
        if connection:
            connection.close()

def username_exists(username:str):
    """
    Check if username provided exists

    :param username:    Username to check
    :type username:     (str)

    :return val:        (bool)
    """
    
    connection, cursor = connect()
    try:
        command = """SELECT userName FROM playerInfo WHERE userName =?"""
        cursor.execute(command, (username,))
        result = cursor.fetchone()
        connection.close()
        if result:
            return True
        else:
            return False
    except sqlite3.Error as e:
        return e

def get_username_by_id(uid:str):
    """
    Return username with associated ID

    :param uid: User ID to query
    :type uid:  (int)

    :return:    (str)
    """
    
    connection, cursor = connect()
    try:
        command = """SELECT userName FROM playerInfo WHERE id =?"""
        cursor.execute(command, (uid,))
        result = cursor.fetchone()

        connection.close()
        if result:
            return result
        else:
            return "User does not exist."

    except sqlite3.Error as e:
        return e

def get_usernames_by_firstName(firstName:str):  ## Gets all record with identical first names
    """
    Fetch all usernames with a matching first name

    :param firstName:   Search for this first name
    :type firstName:    (str)

    :return val:        (list) if matches exist
    """
    connection, cursor = connect()
    try:
        command = """SELECT userName FROM playerInfo WHERE firstName =?"""
        cursor.execute(command, (firstName,))
        result = cursor.fetchall()

        connection.close()
        if result:
            return result
        else:
            return "User does not exist."

    except sqlite3.Error as e:
        connection.close()
        return e

def get_username_by_firstName(firstName:str):  ## Gets the first record with specified firstName
    """
    Fetches the first username with a matching first name

    :param firstName:   Search for this first name
    :type firstName:    (str)

    :return val:        (str)
    """
    connection, cursor = connect()
    try:
        command = """SELECT userName FROM playerInfo WHERE firstName =?"""
        cursor.execute(command, (firstName,))
        result = cursor.fetchone()

        connection.close()
        if result:
            return result
        else:
            return "User does not exist."

    except sqlite3.Error as e:
        connection.close()
        return e

def get_usernames_by_lastName(lastName:str):  ## Gets all record with identical last names
    """
    Fetch all usernames with matching last names

    :param lastName:    Player's last name
    :type lastName:     (str)
    """
    connection, cursor = connect()
    try:
        command = """SELECT userName FROM playerInfo WHERE lastName =?"""
        cursor.execute(command, (lastName,))
        result = cursor.fetchall()

        connection.close()
        if result:
            return result
        else:
            return "User does not exist."

    except sqlite3.Error as e:
        connection.close()
        return e

def get_username_by_lastName(lastName:str):  ## Gets the first record with specified lastName
    """
    Fetch first username with matching last name

    :param lastName:    Player's last Name
    :type lastName:     (str)
    """
    connection, cursor = connect()
    try:
        command = """SELECT userName FROM playerInfo WHERE lastName =?"""
        cursor.execute(command, (lastName,))
        result = cursor.fetchone()
        if result:
            return result
        else:
            return "User does not exist."

    except sqlite3.Error as e:
        return e


## Update general data
def update_userName_by_id(uid:int, new_u:str):
    """
    Update username with the associated userID

    :param uid:     User ID associated with username to be changed
    :type uid:      (int)

    :param new_u:   New username to replace original username
    :type new_u:    (str)
    """
    connection, cursor = connect()
    try:
        command = """UPDATE playerInfo SET userName =? WHERE id =?"""
        cursor.execute(command,(new_u,uid,),)

        connection.commit()
        connection.close()

    except sqlite3.Error as e:
        connection.close
        return e

def update_firstName_by_id(uid:int, new_n:str):
    """
    Update first name of user with associated userID

    :param uid:     User ID associated with first name to be changed
    :type uid:      (int)

    :param new_n:   New first name to replace original first name
    :type new_n:    (str)
    """
    
    connection, cursor = connect()
    try:
        command = """UPDATE playerInfo SET firstName =? WHERE id =?"""
        cursor.execute(command,(new_n,uid,),)

        connection.commit()
        connection.close()

    except sqlite3.Error as e:
        connection.close()
        return e

def update_lastName_by_id(uid:int, new_n:str):
    """
    Update last name of user with associated userID

    :param uid:     User ID associated with last name to be changed
    :type uid:      (int)

    :param new_n:   New last name to replace original last name
    :type new_n:    (str)
    """

    connection, cursor = connect()
    try:
        command = """UPDATE playerInfo SET lastName =? WHERE id =?"""
        cursor.execute(command,(new_n,uid,),)

        connection.commit()
        connection.close()

    except sqlite3.Error as e:
        connection.close()
        return e

def update_score_by_id(uid:int, new_s:int):
    """
    Update score of the user with associated userID

    :param uid:     User ID associated with the score to be changed
    :type uid:      (int)

    :param new_s:   New score to update
    :type new_s:    (int)
    """

    connection, cursor = connect()
    try:
        command = """UPDATE playerInfo SET score =? WHERE id =?"""
        cursor.execute(command,(new_s,uid,),)

        connection.commit()
        connection.close()

    except sqlite3.Error as e:
        connection.close()
        return e

def delete_record_by_uid(uid:int):
    """
    Delete the records of a userID

    :param uid: User ID of the user to be deleted
    :type uid:  (int)
    """

    connection, cursor = connect()
    try:
        command = """DELETE FROM playerInfo WHERE id =?"""
        cursor.execute(command, (uid,))

        connection.commit()
        connection.close()
    except sqlite3.Error as e:
        connection.close()
        return e

