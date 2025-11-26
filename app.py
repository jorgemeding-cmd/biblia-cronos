import streamlit as st
import pandas as pd

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Biblia del Cronos", page_icon="🚗")

# --- TÍTULO Y PRESENTACIÓN ---
st.title("🚗 La Biblia del Fiat Cronos")
st.markdown("""
**Bienvenido a la base de conocimiento colaborativa.**
Aquí encontrarás soluciones probadas por la comunidad para problemas comunes.
""")

# --- TUS ENLACES (CONFIGURACIÓN) ---
# 1. Tu Base de Datos (Google Sheet)
sheet_url = "https://docs.google.com/spreadsheets/d/1hOwrCKTSbYnq59b4towaTVq7OEPoxRZFZ37LU6hNLYQ/export?format=csv&gid=0"

# 2. Tu Formulario de Aportes (Google Forms)
form_url = "https://docs.google.com/forms/d/e/1FAIpQLSf8_BPE98UODsS9j3dCNq8iYEwXEKhcyz4nzQjT6gzQSwiwZw/viewform?usp=publish-editor"

# --- FUNCIÓN PARA CARGAR DATOS ---
@st.cache_data(ttl=60)  # <--- ESTO LE DICE: "Refresca cada 60 segundos"
def load_data():
    try:
        data = pd.read_csv(sheet_url)
        return data
    except Exception as e:
        return None

# Cargamos los datos
df = load_data()

# --- INTERFAZ PRINCIPAL ---
if df is not None:
    # --- BARRA LATERAL (FILTROS) ---
    st.sidebar.header("🔍 Filtros de Búsqueda")
    
    # Verificamos columnas
    if 'motor' in df.columns and 'categoria' in df.columns:
        # Filtro Motor
        motores_disponibles = ["Todos"] + list(df['motor'].unique())
        motor_select = st.sidebar.selectbox("¿Qué motor tienes?", motores_disponibles)
        
        # Filtro Categoría
        categorias_disponibles = ["Todas"] + list(df['categoria'].unique())
        categoria_select = st.sidebar.selectbox("Categoría del problema:", categorias_disponibles)

        # --- LÓGICA DE FILTRADO ---
        df_filtrado = df.copy()

        if motor_select != "Todos":
            df_filtrado = df_filtrado[df_filtrado['motor'].isin([motor_select, "Todos"])]

        if categoria_select != "Todas":
            df_filtrado = df_filtrado[df_filtrado['categoria'] == categoria_select]

        # --- MOSTRAR RESULTADOS ---
        st.divider()
        st.subheader(f"Resultados encontrados: {len(df_filtrado)}")

        if df_filtrado.empty:
            st.warning("No encontramos problemas con esos filtros. ¡Quizás tu auto está perfecto!")
        else:
            for index, row in df_filtrado.iterrows():
                titulo = row['sintoma'] if 'sintoma' in row else "Problema sin título"
                with st.expander(f"🔴 {titulo}"):
                    st.markdown(f"**🔧 Causa probable:** {row.get('causa', 'Desconocida')}")
                    st.info(f"💡 **Solución Comunidad:** {row.get('solucion_comunidad', 'Sin datos')}")
                    st.caption(f"Motor: {row.get('motor', '-')} | Categoría: {row.get('categoria', '-')}")
    else:
        st.error("Error: Las columnas 'motor' o 'categoria' no coinciden con tu Excel.")

else:
    st.error("⚠️ No se pudo conectar con la base de datos de Google Sheets. Revisa tu internet o el enlace.")

# --- SECCIÓN DE APORTES (SIEMPRE VISIBLE AL FINAL) ---
st.divider()
st.subheader("📢 ¿Te pasó algo distinto?")
st.write("Si encontraste una solución nueva, compártela aquí para actualizar la base.")

# Aquí está tu botón con el enlace nuevo
st.link_button("📝 Reportar nueva solución", form_url)