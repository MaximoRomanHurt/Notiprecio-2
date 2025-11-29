# logic/comparador.py
import json
import os

def cargar_precios_fijos():
    """Carga tu tabla de precios fijos desde el archivo JSON"""
    ruta = os.path.join("data", "productos_fijos.json")
    try:
        with open(ruta, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: No se encontró data/productos_fijos.json")
        return []

def generar_tabla_diferencias(datos_mercado):
    """
    Compara: (Tabla 2) Mercado vs (Tabla 1) Fijos
    Genera: (Tabla 3) Diferencias
    """
    precios_fijos = cargar_precios_fijos()
    tabla_diferencias = []

    for producto_mercado in datos_mercado:
        match_encontrado = None
        
        # Lógica de emparejamiento: Buscamos si el producto escrapeado 
        # contiene las palabras clave de nuestro producto fijo.
        nombre_mercado_limpio = producto_mercado['nombre'].lower()
        
        for fijo in precios_fijos:
            # Verificamos si TODAS las palabras clave están en el nombre del producto escrapeado
            if all(clave in nombre_mercado_limpio for clave in fijo['palabras_clave']):
                match_encontrado = fijo
                break
        
        if match_encontrado:
            # CALCULAMOS LA DIFERENCIA
            precio_real = float(producto_mercado['precio_raw'])
            precio_base = match_encontrado['precio_fijo']
            diferencia = precio_real - precio_base
            
            # Determinamos el estado
            if diferencia > 0:
                estado = "SUBIÓ 🔺"
            elif diferencia < 0:
                estado = "BAJÓ 🔻"
            else:
                estado = "IGUAL ➖"

            # Creamos la fila de la Tabla 3
            tabla_diferencias.append({
                "producto": producto_mercado['nombre'],
                "precio_fijo": precio_base,
                "precio_mercado": precio_real,
                "diferencia": round(diferencia, 2),
                "estado": estado,
                "url": producto_mercado['url']
            })
            
    return tabla_diferencias