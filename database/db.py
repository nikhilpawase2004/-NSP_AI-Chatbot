import pymysql
from config import Config

connection = pymysql.connect(

    host=Config.MYSQL_HOST,

    user=Config.MYSQL_USER,

    password=Config.MYSQL_PASSWORD,

    database=Config.MYSQL_DATABASE,

    cursorclass=pymysql.cursors.DictCursor
)


# SAVE CHAT

def save_chat(user_message, bot_response):

    try:

        cursor = connection.cursor()

        query = """
        INSERT INTO chats
        (user_message, bot_response)
        VALUES (%s, %s)
        """

        values = (user_message, bot_response)

        cursor.execute(query, values)

        connection.commit()

        cursor.close()

    except Exception as e:

        print("DATABASE ERROR:", e)


# GET ALL CHATS

def get_all_chats():

    try:

        cursor = connection.cursor()

        query = "SELECT * FROM chats ORDER BY id DESC"

        cursor.execute(query)

        chats = cursor.fetchall()

        cursor.close()

        return chats

    except Exception as e:

        print("DATABASE ERROR:", e)

        return []


# DELETE ONE CHAT

def delete_chat(chat_id):

    try:

        cursor = connection.cursor()

        query = "DELETE FROM chats WHERE id=%s"

        cursor.execute(query, (chat_id,))

        connection.commit()

        cursor.close()

    except Exception as e:

        print("DATABASE ERROR:", e)


# DELETE ALL CHATS

def delete_all_chats():

    try:

        cursor = connection.cursor()

        query = "DELETE FROM chats"

        cursor.execute(query)

        connection.commit()

        cursor.close()

    except Exception as e:

        print("DATABASE ERROR:", e)