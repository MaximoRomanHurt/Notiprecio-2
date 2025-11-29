# main.py
from config.settings import URLS_OBJETIVO, HEADLESS_MODE
from scraping.scraper import PlazaVeaScraper
from scraping.news_scraper import NewsScraper # <--- NUEVO IMPORT
from logic.comparador import generar_tabla_diferencias
from ui.console_ui import mostrar_encabezado, mostrar_reporte_comparativo, mostrar_notificaciones

def main():
    mostrar_encabezado()
    
    # --- FASE 1: PRECIOS ---
    scraper_precios = PlazaVeaScraper(headless=HEADLESS_MODE)
    datos_mercado = []

    # Lista simple de productos para buscar noticias (extraída de las keys de tu config)
    lista_productos_clave = list(URLS_OBJETIVO.keys()) # ['arroz', 'aceite', ...]

    try:
        # Scrapeo de Precios
        for cat, url in URLS_OBJETIVO.items():
            print(f"🛒 Buscando precios de: {cat}...")
            datos = scraper_precios.obtener_productos(url, cat)
            datos_mercado.extend(datos)
    finally:
        scraper_precios.cerrar()

    # --- FASE 2: COMPARACIÓN ---
    print("\n📊 Calculando variaciones de precio...")
    tabla_final = generar_tabla_diferencias(datos_mercado)
    mostrar_reporte_comparativo(tabla_final)

    # --- FASE 3: NOTICIAS Y ALERTAS (NUEVO) ---
    print("\n📰 Escaneando noticias de la última semana en Perú...")
    scraper_noticias = NewsScraper()
    alertas_acumuladas = []

    for prod in lista_productos_clave:
        print(f"   ...buscando contexto sobre '{prod}'")
        noticias = scraper_noticias.buscar_noticias(prod)
        alertas_acumuladas.extend(noticias)

    # --- FASE 4: MOSTRAR NOTIFICACIONES ---
    mostrar_notificaciones(alertas_acumuladas)

if __name__ == "__main__":
    main()