import mysql.connector
from mysql.connector import Error

def get_connection():
    try:
        connection = mysql.connector.connect(
            host="IP_DE_TU_AMIGO",
            port=3306,
            user="admin",
            password="admin123",
            database="precios_db"
        )
        return connection

    except Error as e:
        print("Error al conectar:", e)
        return None
