import sqlite3

## Start connection DO NOT USE THIS
def connect():
    """
    Starts connection, returns connection and cursor object
    DO NOT USE THIS IN YOUR PROGRAM

    :return val:    (tuple)
    """
    connection = sqlite3.connect("../index.db")
    cursor = connection.cursor()
    return connection, cursor


## create table command
def on_init():
    """
    Run on init to initialise table (playerInfo)

    :return val: None
    """
    connection, cursor = connect()
    ## Run on init to initialise table

    command = """CREATE TABLE "playerInfo" (
    "id" INTEGER NOT NULL,
    "userName" VARCHAR(255) NOT NULL,
    "score" INTEGER,
    PRIMARY KEY ("id" AUTOINCREMENT))"""
    cursor.execute(command)
    print("Player Info created")

    cursor.execute(command)

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
	"userName"	VARCHAR(255) NOT NULL,
	"score"	INTEGER,
	PRIMARY KEY("id" AUTOINCREMENT)) """
    cursor.execute(command)
    print("Table created successfully.")
    connection.commit()
    connection.close()


## Manage players
## View player data
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


#### Manage items
## View item data
# def get_powerups(userID:int):
#     """
#     Get list of all powerups associated with the userID

#     :param userID:  User id to query
#     :type userID:   (int)

#     :return val:    (list)
#     """
#     connection, cursor = connect()
#     try:
#         command = """SELECT * FROM playerItems WHERE id =?"""
#         cursor.execute(command, (userID,))
#         result = cursor.fetchall()
#         if result:
#             return result
#         else:
#             return "User does not exist."

#     except sqlite3.Error as e:
#         return e


# ## Update item data
# def update_powerups(userID:int, items: dict[str,int]):
#     """
#     Update number of powerups associated with the userID

#     :param userID:  User id assocated with the update
#     :type userID:   (int)

#     :param items:   Dictionary of item and count (item:count)
#     :type items:    (dict)

#     :return val:    None
#     """

#     connection, cursor = connect()
#     try:
#         command = """UPDATE playerItems SET Anycubic =? WHERE id =?"""
#         cursor.execute(command,(items['anycubic'], userID,))

#         command = """UPDATE playerItems SET Bambu =? WHERE id =?"""
#         cursor.execute(command,(items['bambu'], userID,))

#         command = """UPDATE playerItems SET DouyinIonThrusters =? WHERE id =?"""
#         cursor.execute(command,(items['douyin'], userID,))

#         command = """UPDATE playerItems SET November =? WHERE id =?"""
#         cursor.execute(command,(items['november'], userID,))


#         connection.commit()
#         connection.close()

#     except sqlite3.Error as e:
#         connection.close()
#         return e