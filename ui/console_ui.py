# ui/console_ui.py

def mostrar_encabezado():
    print("\n" + "="*80)
    print(f"{'NOTIPRECIO - MONITOR DE CANASTA BÁSICA':^80}")
    print("="*80)

def mostrar_tabla(datos):
    if not datos:
        print("No hay datos para mostrar.")
        return

    # Encabezados de tabla
    print(f"{'CATEGORIA':<10} | {'PRODUCTO (Resumido)':<30} | {'PRECIO':<8} | {'P. UNITARIO':<12}")
    print("-" * 80)

    for d in datos:
        nombre_corto = (d['nombre'][:27] + '..') if len(d['nombre']) > 27 else d['nombre']
        print(f"{d['categoria']:<10} | {nombre_corto:<30} | S/{d['precio']:<6} | S/{d['precio_unitario']}/{d['unidad']}")
    print("-" * 80)
    print(f"Total encontrados: {len(datos)}")

def consultar_mejores_ofertas(datos_totales):
    """ Simula una consulta SQL: SELECT * ORDER BY precio_unitario ASC LIMIT 3 """
    print("\n>>> ANALISIS: TOP 3 MÁS BARATOS POR UNIDAD DE MEDIDA <<<")
    
    # Agrupamos por categoría para buscar el mejor de cada una
    categorias = set(d['categoria'] for d in datos_totales)
    
    for cat in categorias:
        print(f"\n--- Mejor opción en {cat.upper()} ---")
        # Filtramos por categoría
        items_cat = [d for d in datos_totales if d['categoria'] == cat]
        # Ordenamos por precio unitario (el más barato por kilo/litro)
        items_cat.sort(key=lambda x: x['precio_unitario'])
        
        # Mostramos el top 1
        mejor = items_cat[0]
        print(f"GANADOR: {mejor['nombre']}")
        print(f"PRECIO:  S/{mejor['precio']} (Sale a S/{mejor['precio_unitario']} el {mejor['unidad']})")
        
        # ui/console_ui.py

def mostrar_encabezado():
    print("\n" + "█"*90)
    print(f"{'NOTIPRECIO - MONITOR DE VARIACIÓN DE PRECIOS':^90}")
    print("█"*90)

def mostrar_reporte_comparativo(tabla_diferencias):
    if not tabla_diferencias:
        print("\nNo se encontraron coincidencias entre el mercado y tus productos fijos.")
        print("Revisa si las 'palabras_clave' en tu JSON coinciden con los nombres de Plaza Vea.")
        return

    print("\n" + "="*90)
    print(f"{'PRODUCTO':<35} | {'P. FIJO':<8} | {'MERCADO':<8} | {'DIFERENCIA':<10} | {'ESTADO':<8}")
    print("="*90)

    for fila in tabla_diferencias:
        # Recortar nombre si es muy largo
        nombre = (fila['producto'][:33] + '..') if len(fila['producto']) > 33 else fila['producto']
        
        # Colores simples para consola (si tu terminal lo soporta, sino sale texto normal)
        signo = "+" if fila['diferencia'] > 0 else ""
        
        print(f"{nombre:<35} | S/{fila['precio_fijo']:<6} | S/{fila['precio_mercado']:<6} | {signo}S/{fila['diferencia']:<8} | {fila['estado']}")

    print("-" * 90)

    # Agregar al final de ui/console_ui.py

def mostrar_notificaciones(noticias):
    print("\n" + "🔔"*45)
    print(f"{'NOTIFICACIONES Y ALERTAS DE MERCADO':^90}")
    print("🔔"*45)

    if not noticias:
        print("\n   [Tranquilidad] No hay noticias alarmantes sobre escasez o subidas esta semana.")
        return

    print(f"\n{'NIVEL':<10} | {'PRODUCTO':<10} | {'MENSAJE DEL SISTEMA':<45}")
    print("-" * 90)

    for n in noticias:
        # Título recortado para que no rompa la tabla
        titulo_corto = (n['titulo'][:85] + '...') if len(n['titulo']) > 85 else n['titulo']
        
        print(f"{n['nivel']:<10} | {n['producto'].upper():<10} | {n['mensaje']}")
        print(f"   └── Fuente: {titulo_corto}")
        print(f"   └── Link: {n['url']}")
        print("-" * 90)