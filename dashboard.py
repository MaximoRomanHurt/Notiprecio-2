# dashboard.py
import streamlit as st
import plotly.express as px
import time

# Módulos propios
from scraping.scraper import PlazaVeaScraper
from scraping.news_scraper import NewsScraper
from config.settings import URLS_OBJETIVO, HEADLESS_MODE
# IMPORTANTE: Ahora importamos el conector de BD
from database.postgres_connector import guardar_datos_scraping, obtener_reporte_bolsa

st.set_page_config(page_title="Notiprecio DB", page_icon="🏦", layout="wide")

# Estilos
st.markdown("""<style>.metric-card {background-color: #222; padding: 10px; border-radius: 8px;}</style>""", unsafe_allow_html=True)

st.title("🏦 Bolsa de Valores: Canasta Básica")
st.markdown("### Monitor de Precios en Tiempo Real (Conectado a PostgreSQL)")

# --- SIDEBAR: BOTÓN DE ACCIÓN ---
with st.sidebar:
    st.header("Operaciones")
    
    if st.button("🔄 Ejecutar Scraper y Guardar en BD", type="primary"):
        with st.spinner('Escaneando Plaza Vea...'):
            scraper = PlazaVeaScraper(headless=HEADLESS_MODE)
            datos_totales = []
            
            # Barra de progreso
            bar = st.progress(0)
            for i, (cat, url) in enumerate(URLS_OBJETIVO.items()):
                items = scraper.obtener_productos(url, cat)
                datos_totales.extend(items)
                bar.progress((i + 1) / len(URLS_OBJETIVO))
            
            scraper.cerrar()
            
            # GUARDAR EN POSTGRESQL
            if datos_totales:
                mensaje = guardar_datos_scraping(datos_totales)
                st.success(mensaje)
                time.sleep(1) # Pequeña pausa para que la BD procese
                st.rerun() # Recargar la página para ver los datos nuevos
            else:
                st.error("No se encontraron productos.")

# --- CUERPO PRINCIPAL: LECTURA DE BD ---

# 1. Consultamos a la Base de Datos
df = obtener_reporte_bolsa()

if df.empty:
    st.info("📭 La base de datos no tiene registros de HOY. Dale al botón 'Ejecutar Scraper' en la barra lateral.")
else:
    # --- KPI INDICADORES ---
    st.subheader("📊 Indicadores de Mercado (Hoy)")
    
    # Mostramos los 4 productos más relevantes
    cols = st.columns(4)
    for i, row in df.head(4).iterrows():
        col = cols[i % 4]
        
        # Lógica de color (Bolsa de valores)
        dif = row['diferencia']
        delta_color = "inverse" if dif > 0 else "normal" # Rojo si sube, Verde si baja
        
        with col:
            st.metric(
                label=row['producto'],
                value=f"S/ {row['precio_actual']}",
                delta=f"{dif} Soles",
                delta_color=delta_color
            )

    # --- GRÁFICA ---
    st.markdown("---")
    col_graf, col_tabla = st.columns([2, 1])
    
    with col_graf:
        st.subheader("🆚 Diferencial: Objetivo vs Realidad")
        # Gráfico de barras comparativo
        fig = px.bar(
            df, 
            x='producto', 
            y=['precio_fijo', 'precio_actual'],
            barmode='group',
            color_discrete_map={'precio_fijo': '#2ecc71', 'precio_actual': '#e74c3c'},
            title="Comparativa de Precios"
        )
        st.plotly_chart(fig, use_container_width=True)
        
    with col_tabla:
        st.subheader("📋 Detalle de Registros")
        st.dataframe(df[['producto', 'precio_fijo', 'precio_actual', 'diferencia']], hide_index=True)

    # --- NOTICIAS (Opcional) ---
    with st.expander("📰 Ver Noticias Relacionadas"):
        if st.button("Buscar Noticias Ahora"):
            ns = NewsScraper()
            for prod in df['producto'].unique():
                st.write(f"**Noticias sobre {prod}:**")
                noticias = ns.buscar_noticias(prod)
                if not noticias:
                    st.write("Sin novedades.")
                for n in noticias:
                    st.info(f"{n['nivel']} | {n['mensaje']} - [{n['titulo']}]({n['url']})")