# config/settings.py

# Diccionario con las categorías y URLs de Plaza Vea
URLS_OBJETIVO = {
"arroz": "https://www.plazavea.com.pe/abarrotes/arroz",
    "aceite": "https://www.plazavea.com.pe/abarrotes/aceites",
    "azucar": "https://www.plazavea.com.pe/abarrotes/azucar-y-endulzantes",
    "leche": "https://www.plazavea.com.pe/lacteos/leches",
    "huevos": "https://www.plazavea.com.pe/lacteos/huevos",
    "pollo": "https://www.plazavea.com.pe/carnes-y-aves/pollo",
    "fideos": "https://www.plazavea.com.pe/abarrotes/fideos-y-pastas"
}

# Configuración del Scraper
# True = El navegador no se ve (más rápido)
# False = Se abre la ventana de Chrome (bueno para ver qué está haciendo)
HEADLESS_MODE = False