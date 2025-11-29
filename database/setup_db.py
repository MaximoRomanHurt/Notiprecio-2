# database/setup_db.py
import psycopg2
from postgres_connector import DB_CONFIG

def inicializar_base_datos():
    print("🔌 Conectando a PostgreSQL...")
    
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        print("🗑️ Borrando tablas antiguas (si existen)...")
        # Borramos en cascada para evitar errores de dependencia
        cur.execute("DROP VIEW IF EXISTS vista_reporte_bolsa CASCADE;")
        cur.execute("DROP TABLE IF EXISTS precios_variables CASCADE;")
        cur.execute("DROP TABLE IF EXISTS precios_fijos CASCADE;")

        print("🏗️ Creando Tabla: Precios Fijos...")
        cur.execute("""
            CREATE TABLE precios_fijos (
                id SERIAL PRIMARY KEY,
                nombre_referencia VARCHAR(100) NOT NULL,
                keywords VARCHAR(100) NOT NULL,
                precio_objetivo DECIMAL(10, 2) NOT NULL
            );
        """)

        print("🏗️ Creando Tabla: Precios Variables...")
        cur.execute("""
            CREATE TABLE precios_variables (
                id SERIAL PRIMARY KEY,
                fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                tienda VARCHAR(50),
                nombre_producto TEXT,
                precio_mercado DECIMAL(10, 2),
                url TEXT UNIQUE
            );
        """)

        print("👀 Creando Vista: Reporte de Bolsa...")
        # Esta vista cruza las dos tablas automáticamente
        cur.execute("""
            CREATE OR REPLACE VIEW vista_reporte_bolsa AS
            SELECT 
                v.fecha_registro,
                f.nombre_referencia AS producto,
                f.precio_objetivo AS precio_fijo,
                v.precio_mercado AS precio_actual,
                (v.precio_mercado - f.precio_objetivo) AS diferencia,
                v.url
            FROM precios_variables v
            JOIN precios_fijos f 
            ON v.nombre_producto ILIKE '%' || split_part(f.keywords, ',', 1) || '%'
            WHERE v.fecha_registro::DATE = CURRENT_DATE;
        """)

        print("🌱 Insertando datos de prueba (Precios Fijos)...")
        cur.execute("""
            INSERT INTO precios_fijos (nombre_referencia, keywords, precio_objetivo) VALUES 
            ('Aceite Primor', 'primor,900', 9.00),
            ('Arroz Costeño', 'arroz,costeño', 23.00),
            ('Leche Gloria', 'gloria,pack', 25.50),
            ('Azucar Rubia', 'azucar,rubia', 19.00),
            ('Fideos Don Vittorio', 'vittorio,fideo', 3.80),
            ('Huevos Pardos', 'huevos,pardos', 16.50);
        """)

        conn.commit()
        cur.close()
        conn.close()
        print("\n✅ ¡Base de datos instalada y configurada con éxito!")

    except Exception as e:
        print(f"\n❌ Error al crear las tablas: {e}")
        print("Asegúrate de que la base de datos 'Products' exista en pgAdmin.")

if __name__ == "__main__":
    inicializar_base_datos()