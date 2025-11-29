# logic/transform.py
import re
from datetime import datetime

def extraer_unidad(nombre):
    """
    Busca patrones de peso/volumen en el nombre del producto.
    Ejemplos: 
      - "Arroz 5kg" -> devuelve 5.0, 'kg'
      - "Aceite 900ml" -> devuelve 0.9, 'lt'
    """
    # Regex para detectar números seguidos de unidades (kg, g, l, ml)
    match = re.search(r'(\d+[\.,]?\d*)\s*(kg|g|l|ml|litros|kilos|gramos)', nombre, re.IGNORECASE)
    
    cantidad = 1.0
    unidad_norm = 'unid' # Por defecto si no encuentra nada

    if match:
        # Extraemos el número y reemplazamos coma por punto (ej: 1,5 -> 1.5)
        val_str = match.group(1).replace(',', '.')
        val = float(val_str)
        unit_str = match.group(2).lower()

        # Normalización a KILOS (kg)
        if unit_str in ['kg', 'kilos']:
            cantidad = val
            unidad_norm = 'kg'
        elif unit_str in ['g', 'gramos']:
            cantidad = val / 1000  # Convertimos gramos a kilos
            unidad_norm = 'kg'
            
        # Normalización a LITROS (lt)
        elif unit_str in ['l', 'litros']:
            cantidad = val
            unidad_norm = 'lt'
        elif unit_str in ['ml']:
            cantidad = val / 1000  # Convertimos mililitros a litros
            unidad_norm = 'lt'
            
    return cantidad, unidad_norm

def limpiar_data(lista_cruda):
    """
    Recibe la lista sucia del scraper y devuelve una lista limpia
    con precios numéricos y cálculo de precio unitario.
    """
    lista_limpia = []
    
    for item in lista_cruda:
        # 1. Limpiar Precio (Convertir "S/ 24.90" a 24.90)
        if not item['precio_raw']:
            continue
            
        # Elimina todo lo que no sea número o punto
        p_str = re.sub(r'[^\d.]', '', item['precio_raw'])
        
        try:
            precio = float(p_str)
        except ValueError:
            continue # Si falla la conversión, saltamos este producto

        # 2. Extraer peso y calcular precio unitario real
        cantidad, unidad = extraer_unidad(item['nombre'])
        
        # Evitamos división por cero
        if cantidad > 0:
            p_unitario = round(precio / cantidad, 2)
        else:
            p_unitario = precio

        # 3. Construir el diccionario final
        lista_limpia.append({
            "fecha": datetime.now().strftime("%Y-%m-%d"),
            "tienda": item['tienda'],
            "categoria": item['categoria'],
            "nombre": item['nombre'],
            "precio": precio,
            "cantidad": cantidad,
            "unidad": unidad,
            "precio_unitario": p_unitario, # Dato clave para comparar
            "url": item['url']
        })
    
    return lista_limpia