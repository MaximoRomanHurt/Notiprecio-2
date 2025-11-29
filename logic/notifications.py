from database.models import *
from logic.price_logic import calcular_diferencia

def generar_notificacion(id_producto):
    diff = calcular_diferencia(id_producto)
    if diff is None:
        return
    
    diferencia, porcentaje = diff

    if porcentaje > 0:
        tipo = "Subida"
        mensaje = f"El producto subió {porcentaje:.2f}%."
    else:
        tipo = "Bajada"
        mensaje = f"El producto bajó {abs(porcentaje):.2f}%."

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO notificacion (id_producto, tipo, mensaje, canal, activa, enviada)
        VALUES (%s, %s, %s, %s, TRUE, FALSE)
    """, (id_producto, tipo, mensaje, "sistema"))

    conn.commit()
    cursor.close()
    conn.close()
