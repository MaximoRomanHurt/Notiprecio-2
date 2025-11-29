# scraping/news_scraper.py
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import urllib.parse

class NewsScraper:
    def __init__(self):
        # Usamos Google News RSS específico para Perú (geo=PE) y español (hl=es-419)
        self.base_url = "https://news.google.com/rss/search?q={query}+when:7d&hl=es-419&gl=PE&ceid=PE:es-419"

    def analizar_impacto(self, texto):
        """
        Analiza el título de la noticia para determinar la alerta.
        Retorna: (Nivel de Alerta, Mensaje)
        """
        texto = texto.lower()
        
        # DICCIONARIO DE PALABRAS CLAVE
        palabras_subida = ["sube", "alza", "incremento", "caro", "dispara", "elevado"]
        palabras_bajada = ["baja", "cae", "barato", "desciende", "oferta", "menor precio"]
        palabras_riesgo = ["escasez", "desabastecimiento", "paro", "bloqueo", "huelga", "fenómeno", "lluvias", "sequía", "crisis"]

        # 1. Detectar SUBIDA confirmada
        if any(p in texto for p in palabras_subida):
            return "🔴 ALTA", "¡ALERTA! El precio está subiendo."
            
        # 2. Detectar RIESGO (Posible subida)
        if any(p in texto for p in palabras_riesgo):
            return "🟠 MEDIA", "PRECAUCIÓN: Riesgo de escasez o subida (Clima/Conflictos)."
            
        # 3. Detectar BAJADA
        if any(p in texto for p in palabras_bajada):
            return "🟢 BUENA", "Oportunidad: El precio podría bajar."

        return "⚪ NEUTRA", "Noticia informativa."

    def buscar_noticias(self, producto):
        """
        Busca noticias sobre un producto específico (ej: 'Arroz precio').
        """
        # Codificamos la búsqueda para URL (ej: 'precio arroz peru')
        busqueda = urllib.parse.quote(f"precio {producto} peru")
        url_final = self.base_url.format(query=busqueda)
        
        try:
            response = requests.get(url_final, timeout=10)
            # Parseamos el XML del RSS
            soup = BeautifulSoup(response.content, features='xml')
            items = soup.find_all('item')
            
            noticias_relevantes = []
            
            # Analizamos las 3 noticias más recientes
            for item in items[:3]:
                titulo = item.title.text
                link = item.link.text
                fecha = item.pubDate.text
                
                nivel, mensaje = self.analizar_impacto(titulo)
                
                # Solo guardamos si NO es neutra (para no llenar de ruido), 
                # o si tú quieres ver todo, quita el 'if nivel != ...'
                if nivel != "⚪ NEUTRA":
                    noticias_relevantes.append({
                        "producto": producto,
                        "titulo": titulo,
                        "nivel": nivel,
                        "mensaje": mensaje,
                        "url": link,
                        "fecha": fecha
                    })
            
            return noticias_relevantes

        except Exception as e:
            print(f"Error buscando noticias de {producto}: {e}")
            return []