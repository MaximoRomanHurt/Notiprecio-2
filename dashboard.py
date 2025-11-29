# dashboard.py
import streamlit as st
import pandas as pd
import plotly.express as px
import time

# Importamos nuestros módulos (el cerebro del proyecto)
from scraping.scraper import PlazaVeaScraper
from scraping.news_scraper import NewsScraper
from logic.comparador import generar_tabla_diferencias, cargar_precios_fijos
from config.settings import URLS_OBJETIVO, HEADLESS_MODE

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Notiprecio Dashboard",
    page_icon="📈",
    layout="wide"
)

# --- ESTILOS CSS PARA DARLE LOOK "BOLSA" ---
st.markdown("""
<style>
    .metric-card {
        background-color: #1e1e1e;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #333;
    }
</style>
""", unsafe_allow_html=True)

# --- GESTIÓN DE ESTADO (MEMORIA TEMPORAL) ---
# Como no usamos BD, guardamos los datos en la "memoria" del navegador
if 'datos_mercado' not in st.session_state:
    st.session_state['datos_mercado'] = []
if 'noticias' not in st.session_state:
    st.session_state['noticias'] = []
if 'ultimo_update' not in st.session_state:
    st.session_state['ultimo_update'] = "Nunca"

# --- TÍTULO ---
st.title("📈 Notiprecio: Monitor de Mercado")
st.markdown("### Control de Precios de Canasta Básica - Perú")

# --- BARRA LATERAL (CONTROLES) ---
with st.sidebar:
    st.header("🎮 Panel de Control")
    
    # BOTÓN 1: ESCANEAR PRECIOS
    if st.button("🔄 Actualizar Precios (Scraping)", use_container_width=True):
        with st.spinner('Conectando con Plaza Vea...'):
            scraper = PlazaVeaScraper(headless=HEADLESS_MODE)
            datos_temp = []
            try:
                # Barra de progreso
                progress_bar = st.progress(0)
                total_cats = len(URLS_OBJETIVO)
                
                for i, (cat, url) in enumerate(URLS_OBJETIVO.items()):
                    items = scraper.obtener_productos(url, cat)
                    datos_temp.extend(items)
                    progress_bar.progress((i + 1) / total_cats)
                
                # Guardamos en memoria
                st.session_state['datos_mercado'] = datos_temp
                st.session_state['ultimo_update'] = time.strftime("%H:%M:%S")
                st.success(f"¡Datos actualizados a las {st.session_state['ultimo_update']}!")
            except Exception as e:
                st.error(f"Error: {e}")
            finally:
                scraper.cerrar()

    # BOTÓN 2: NOTICIAS
    if st.button("📰 Analizar Noticias", use_container_width=True):
        with st.spinner('Leyendo noticias de la semana...'):
            news_scraper = NewsScraper()
            alertas = []
            # Buscamos noticias solo de las categorías configuradas
            for cat in URLS_OBJETIVO.keys():
                noticias = news_scraper.buscar_noticias(cat)
                alertas.extend(noticias)
            st.session_state['noticias'] = alertas

    st.markdown("---")
    st.info("Sistema corriendo en memoria local. Al cerrar esta pestaña, los datos se reinician.")

# --- LÓGICA DE COMPARACIÓN ---
# Si hay datos escrapeados, calculamos las diferencias
if st.session_state['datos_mercado']:
    
    # Generamos la tabla comparativa usando tu lógica existente
    df_comparativo = generar_tabla_diferencias(st.session_state['datos_mercado'])
    
    if not df_comparativo:
        st.warning("Se escanearon productos, pero ninguno coincide con tus 'Precios Fijos' (JSON). Revisa los nombres.")
    else:
        # Convertimos a DataFrame de Pandas para graficar fácil
        df = pd.DataFrame(df_comparativo)

        # --- SECCIÓN 1: KPI / INDICADORES (ESTILO BOLSA) ---
        st.subheader("📊 Cotización en Tiempo Real")
        
        # Grid de métricas (3 columnas)
        cols = st.columns(3)
        for index, row in df.iterrows():
            col = cols[index % 3] # Distribuir en columnas
            
            # Calcular delta (diferencia) para la flecha
            delta = row['diferencia']
            color = "normal"
            if delta > 0: color = "inverse" # Rojo si sube (malo para el comprador)
            elif delta < 0: color = "normal" # Verde si baja (bueno)
            
            with col:
                st.metric(
                    label=row['producto'],
                    value=f"S/ {row['precio_mercado']}",
                    delta=f"{delta} Soles",
                    delta_color=color
                )

        # --- SECCIÓN 2: GRÁFICA COMPARATIVA ---
        st.markdown("---")
        st.subheader("🆚 Comparativa Visual: Fijo vs. Variable")
        
        # Preparamos datos para la gráfica (Formato Largo)
        # Esto crea una tabla para que Plotly entienda las barras agrupadas
        df_grafico = pd.melt(df, id_vars=['producto'], value_vars=['precio_fijo', 'precio_mercado'], var_name='Tipo', value_name='Precio')
        
        fig = px.bar(
            df_grafico, 
            x='producto', 
            y='Precio', 
            color='Tipo', 
            barmode='group',
            color_discrete_map={'precio_fijo': '#3498db', 'precio_mercado': '#e74c3c'},
            title="Diferencial de Precios"
        )
        st.plotly_chart(fig, use_container_width=True)

        # --- SECCIÓN 3: TABLA DETALLADA ---
        with st.expander("Ver Tabla de Datos Completa"):
            st.dataframe(df)

else:
    st.info("👋 ¡Bienvenido! Presiona el botón 'Actualizar Precios' en la barra lateral para iniciar el escaneo.")

# --- SECCIÓN 4: NOTIFICACIONES (NOTICIAS) ---
if st.session_state['noticias']:
    st.markdown("---")
    st.subheader("🔔 Alertas de Mercado (Noticias)")
    
    for n in st.session_state['noticias']:
        # Definir color según nivel de alerta
        tipo_alerta = "info"
        icono = "ℹ️"
        if "ALTA" in n['nivel']: 
            tipo_alerta = "error"
            icono = "🔥"
        elif "BUENA" in n['nivel']: 
            tipo_alerta = "success"
            icono = "✅"
        elif "MEDIA" in n['nivel']:
            tipo_alerta = "warning"
            icono = "⚠️"

        # Mostrar alerta bonita
        if tipo_alerta == "error":
            st.error(f"**{icono} {n['producto'].upper()}**: {n['mensaje']}  \n[{n['titulo']}]({n['url']})")
        elif tipo_alerta == "warning":
            st.warning(f"**{icono} {n['producto'].upper()}**: {n['mensaje']}  \n[{n['titulo']}]({n['url']})")
        elif tipo_alerta == "success":
            st.success(f"**{icono} {n['producto'].upper()}**: {n['mensaje']}  \n[{n['titulo']}]({n['url']})")
        else:
            st.info(f"**{icono} {n['producto'].upper()}**: {n['mensaje']}  \n[{n['titulo']}]({n['url']})")