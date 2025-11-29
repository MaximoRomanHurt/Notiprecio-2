import mysql.connector
from mysql.connector import Error

def get_connection():
    try:
        connection = mysql.connector.connect(
            host="172.20.64.1",
            port=5432:5432,
            user="admin",
            password="admin123",
            database="01_int.sql"
        )
        return connection

    except Error as e:
        print("Error al conectar:", e)
        return None
