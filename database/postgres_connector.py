# database/postgres_connector.py
import psycopg2
import pandas as pd

# --- ESTA VARIABLE DEBE ESTAR AQUÍ ARRIBA (VARIABLES GLOBALES) ---
DB_CONFIG = {
   'dbname': '..',    # OJO: Cambié 'postgres' por 'Products' según tu comentario
    'user': '..',
    'password': "..", 
    'host': '...',
    'port': '...'
}

def obtener_conexion():
    try:
        # Usamos la variable DB_CONFIG que definimos arriba
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Error conectando a la BD: {e}")
        return None

def guardar_datos_scraping(lista_datos):
    conn = obtener_conexion()
    if not conn: return
    
    try:
        cur = conn.cursor()
        nuevos = 0
        
        for item in lista_datos:
            cur.execute("""
                INSERT INTO precios_variables (fecha_registro, tienda, nombre_producto, precio_mercado, url)
                VALUES (NOW(), %s, %s, %s, %s)
                ON CONFLICT (url) DO UPDATE 
                SET precio_mercado = EXCLUDED.precio_mercado,
                    fecha_registro = NOW();
            """, (item['tienda'], item['nombre'], item['precio_raw'], item['url']))
            nuevos += 1
            
        conn.commit()
        cur.close()
        return f"Se actualizaron {nuevos} registros."
    except Exception as e:
        conn.rollback()
        return f"Error guardando: {e}"
    finally:
        conn.close()

def obtener_reporte_bolsa():
    conn = obtener_conexion()
    if not conn: return pd.DataFrame()
    
    try:
        query = "SELECT * FROM vista_reporte_bolsa ORDER BY diferencia DESC"
        df = pd.read_sql_query(query, conn)
        return df
    except Exception as e:
        print(f"Error leyendo reporte: {e}")
        return pd.DataFrame()
    finally:
        conn.close()