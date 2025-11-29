# scraping/scraper.py
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

class PlazaVeaScraper:
    def __init__(self, headless=False):
        self.options = Options()
        if headless:
            self.options.add_argument('--headless')
        self.options.add_argument("--start-maximized")
        # Usamos un User-Agent genérico para evitar bloqueos
        self.options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        self.driver = None

    def iniciar(self):
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=self.options)

    def cerrar(self):
        if self.driver:
            self.driver.quit()

    def obtener_productos(self, url, categoria):
        if not self.driver:
            self.iniciar()
            
        print(f"   [Scraper] Navegando a: {categoria.upper()}...")
        self.driver.get(url)
        
        # Espera inteligente a que cargue el elemento específico que me pasaste
        try:
            wait = WebDriverWait(self.driver, 15)
            # Esperamos a que aparezca al menos un elemento con la clase "Showcase__content"
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "Showcase__content")))
        except:
            print("   [Aviso] La página tardó en cargar o cambió de estructura.")

        # Scroll suave para activar Lazy Load (cargar imágenes y precios de abajo)
        print("   [Scraper] Bajando para cargar todos los productos...")
        for _ in range(4):
            self.driver.execute_script("window.scrollBy(0, 500);")
            time.sleep(1)

        datos = []
        
        # BUSCAMOS EXACTAMENTE LA CLASE QUE ME ENVIASTE
        tarjetas = self.driver.find_elements(By.CLASS_NAME, "Showcase__content")
        print(f"   [Debug] Se encontraron {len(tarjetas)} tarjetas 'Showcase'.")

        for tarjeta in tarjetas:
            try:
                # 1. NOMBRE (Clase: Showcase__name)
                try:
                    nombre = tarjeta.find_element(By.CLASS_NAME, "Showcase__name").text
                except:
                    # Intento alternativo: atributo title del contenedor
                    nombre = tarjeta.get_attribute("title")

                # 2. FILTRO PALABRA CLAVE (Para limpiar basura)
                # Quitamos la 's' final (ej: fideos -> fideo)
                keyword = categoria.lower().rstrip('s')
                if keyword not in nombre.lower():
                    # Si buscamos "Aceite" y sale "Atún", lo saltamos
                    continue

                # 3. PRECIO (La joya de la corona)
                # Tu HTML tiene un atributo oculto data-price="9.50". ¡Es perfecto!
                precio_final = None
                
                try:
                    # Intento A: Buscar precio de oferta (Showcase__salePrice)
                    elem_oferta = tarjeta.find_element(By.CLASS_NAME, "Showcase__salePrice")
                    precio_final = elem_oferta.get_attribute("data-price") # Extrae "9.50" directo
                except:
                    pass

                # Intento B: Si no hay oferta, buscar precio normal
                if not precio_final:
                    try:
                        # Buscamos clases que contengan "price"
                        texto_precio = tarjeta.find_element(By.CSS_SELECTOR, "[class*='Showcase__price'], [class*='Showcase__salePrice']").text
                        # Limpiamos "S/ 10.50 x Und" -> "10.50"
                        import re
                        match = re.search(r'[\d.]+', texto_precio.replace(',', '.'))
                        if match:
                            precio_final = match.group(0)
                    except:
                        pass

                # 4. URL (Clase: Showcase__link)
                try:
                    link = tarjeta.find_element(By.CLASS_NAME, "Showcase__link").get_attribute("href")
                except:
                    link = url

                if precio_final:
                    datos.append({
                        "categoria": categoria,
                        "nombre": nombre,
                        "precio_raw": str(precio_final), # Guardamos "9.50" limpio
                        "url": link, 
                        "tienda": "Plaza Vea"
                    })

            except Exception as e:
                # Si falla una tarjeta, pasamos a la siguiente
                continue

        # Eliminar duplicados
        unique_data = {f"{d['nombre']}_{d['precio_raw']}": d for d in datos}.values()
        
        print(f"   [Final] {len(unique_data)} productos válidos extraídos.")
        return list(unique_data)