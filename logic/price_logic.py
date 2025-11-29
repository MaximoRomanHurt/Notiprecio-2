from database.models import *

def calcular_diferencia(id_producto):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT pf.precio AS fijo, pv.precio AS variable
        FROM precio_fijo pf
        JOIN precio_variable pv
        ON pf.id_producto = pv.id_producto
        WHERE pf.id_producto = %s
        ORDER BY pv.fecha_registro DESC
        LIMIT 1
    """, (id_producto,))

    data = cursor.fetchone()
    cursor.close()
    conn.close()

    if not data:
        return None

    diferencia = data["variable"] - data["fijo"]
    porcentaje = (diferencia / data["fijo"]) * 100

    return diferencia, porcentaje
