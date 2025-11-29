from config.db import get_connection

def obtener_productos():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM producto")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

def insertar_precio_variable(id_producto, precio):
    conn = get_connection()
    cursor = conn.cursor()
    sql = """
    INSERT INTO precio_variable (id_producto, precio, fecha_registro)
    VALUES (%s, %s, NOW())
    """
    cursor.execute(sql, (id_producto, precio))
    conn.commit()
    cursor.close()
    conn.close()

def insertar_precio_fijo(id_producto, precio):
    conn = get_connection()
    cursor = conn.cursor()
    sql = """
    INSERT INTO precio_fijo (id_producto, precio, fecha_registro)
    VALUES (%s, %s, NOW())
    """
    cursor.execute(sql, (id_producto, precio))
    conn.commit()
    cursor.close()
    conn.close()
