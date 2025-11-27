import streamlit as st
import pandas as pd

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Biblia del Cronos", page_icon="🚗", layout="centered")

# --- TÍTULO Y PRESENTACIÓN ---
st.title("🚗 La Biblia del Fiat Cronos")
st.markdown("""
**Base de conocimiento colaborativa.** Escribe tu problema abajo o usa los filtros del menú para encontrar soluciones probadas.
""")

# --- TUS ENLACES ---
sheet_url = "https://docs.google.com/spreadsheets/d/1hOwrCKTSbYnq59b4towaTVq7OEPoxRZFZ37LU6hNLYQ/export?format=csv&gid=0"
form_url = "https://docs.google.com/forms/d/e/1FAIpQLSf8_BPE98UODsS9j3dCNq8iYEwXEKhcyz4nzQjT6gzQSwiwZw/viewform?usp=publish-editor"

# --- FUNCIÓN PARA CARGAR DATOS ---
@st.cache_data(ttl=60)
def load_data():
    try:
        data = pd.read_csv(sheet_url)
        # Aseguramos que todo sea texto para evitar errores en la búsqueda
        return data.astype(str) 
    except Exception as e:
        return None

df = load_data()

# --- INTERFAZ PRINCIPAL ---
if df is not None:
    # ---------------------------------------------------------
    # 1. BARRA LATERAL (FILTROS)
    # ---------------------------------------------------------
    st.sidebar.header("🎛️ Filtros")
    
    # Filtro Motor
    motores_disponibles = ["Todos"] + list(df['motor'].unique())
    motor_select = st.sidebar.selectbox("Motor:", motores_disponibles)
    
    # Filtro Categoría
    categorias_disponibles = ["Todas"] + list(df['categoria'].unique())
    categoria_select = st.sidebar.selectbox("Categoría:", categorias_disponibles)

    # ---------------------------------------------------------
    # 2. BUSCADOR DE PALABRAS CLAVE (NUEVO)
    # ---------------------------------------------------------
    busqueda = st.text_input("🔍 ¿Qué está fallando? (Ej: ruido, aceite, luces, baúl)")

    # ---------------------------------------------------------
    # 3. LÓGICA DE FILTRADO
    # ---------------------------------------------------------
    df_filtrado = df.copy()

    # Aplicar filtro de Motor
    if motor_select != "Todos":
        df_filtrado = df_filtrado[df_filtrado['motor'].isin([motor_select, "Todos"])]

    # Aplicar filtro de Categoría
    if categoria_select != "Todas":
        df_filtrado = df_filtrado[df_filtrado['categoria'] == categoria_select]

    # Aplicar Buscador de Texto (Busca en Sintoma, Causa o Solucion)
    if busqueda:
        df_filtrado = df_filtrado[
            df_filtrado['sintoma'].str.contains(busqueda, case=False) | 
            df_filtrado['causa'].str.contains(busqueda, case=False) |
            df_filtrado['solucion_comunidad'].str.contains(busqueda, case=False)
        ]

    # ---------------------------------------------------------
    # 4. ESTADÍSTICAS Y GRÁFICO (NUEVO)
    # ---------------------------------------------------------
    # Solo mostramos el gráfico si hay datos y no estamos buscando algo muy específico
    if not df_filtrado.empty:
        with st.expander("📊 Ver Estadísticas de Fallas (Click aquí)"):
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.metric("Problemas encontrados", len(df_filtrado))
                top_categoria = df_filtrado['categoria'].mode()[0]
                st.metric("Categoría más frecuente", top_categoria)
            
            with col2:
                st.caption("Distribución de problemas por categoría")
                # Contamos cuántos problemas hay por categoría
                conteo = df_filtrado['categoria'].value_counts()
                st.bar_chart(conteo)

    # ---------------------------------------------------------
    # 5. MOSTRAR RESULTADOS
    # ---------------------------------------------------------
    st.divider()
    
    if df_filtrado.empty:
        st.warning(f"No encontramos nada buscando '{busqueda}'. ¡Prueba con otra palabra!")
    else:
        for index, row in df_filtrado.iterrows():
            titulo = row['sintoma'] if 'sintoma' in row else "Problema sin título"
            with st.expander(f"🔴 {titulo}"):
                st.markdown(f"**🔧 Causa probable:** {row.get('causa', '-')}")
                st.info(f"💡 **Solución Comunidad:** {row.get('solucion_comunidad', '-')}")
                st.caption(f"Motor: {row.get('motor', '-')} | Categoría: {row.get('categoria', '-')}")

else:
    st.error("⚠️ Error de conexión con Google Sheets.")

# --- SECCIÓN DE APORTES ---
st.divider()
st.subheader("📢 ¿Tienes una solución nueva?")
st.link_button("📝 Agregar Aporte", form_url)
