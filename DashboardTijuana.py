# las librerias que vamos a usar pandas para manipular datos streamlit para el dashboard y plotly para las graficas
import streamlit as st
import plotly.express as px
from AgrupacionesTijuana import *

# configuramso la pagina
st.set_page_config(page_title="Dashboard de Farmacias Tijuana", layout="wide")
st.markdown("""
<div style='text-align: center;'>
    <img src='https://upload.wikimedia.org/wikipedia/commons/thumb/f/f7/Escudo_de_Tijuana%2C_Baja_California.svg/973px-Escudo_de_Tijuana%2C_Baja_California.svg.png' 
         width='180'>

</div>
""", unsafe_allow_html=True)

# Fondo blanco + centro + tipografía Roboto, basicamente la configuracion visual del dashboard
st.markdown("""
    <style>
    /* Fuente Roboto */
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Roboto', sans-serif !important;
        background-color: white !important;
        text-align: center !important;
    }
    /* Centrar todos los títulos */
    h1, h2, h3, h4, h5 {
        text-align: center !important;
        font-weight: 700 !important;
    }
    /* Centrar textos */
    p, label, span {
        text-align: center !important;
    }
    .stMarkdown {
        text-align: center !important;
    }
    /* Centrar métricas */
    div[data-testid="metric-container"] {
        text-align: center !important;
        justify-content: center !important;
    }
    /* Ensanchar área de contenido */
    .block-container {
        max-width: 1200px;
        margin: auto;
    }
    </style>
""", unsafe_allow_html=True)

#esta es la paleta de colores decidida para el dashboard
PALETA_AZUL_VERDE = [
    "#0D47A1",  # azul oscuro
    "#1976D2",  # azul fuerte
    "#64B5F6",  # azul claro
    "#00ACC1",  # turquesa
    "#26A69A",  # verde agua
    "#66BB6A",  # verde medio
    "#2E7D32"   # verde intenso
]
# cargo el archivo originals
df = pd.read_csv("farmaciasCompletoLimpio.csv")
df_tijuana = df[df["Ubicacion"].str.lower() == "tijuana"].copy()

# Mis agrupaciones de tijuana
df_colonia = AgrupacionTijuana(df)
df_consultorio = ConsultoriosPorcentajeTijuana(df)
df_cadenas = CadenasTijuana(df)
df_tamano = TamaFarmaT(df)
df_servicios = ServicioT(df)
df_modelo = ModeloFarmaciaTijuana(df)
df_vialidad = TipoVialidadT(df)

#El inicio del dashboard
st.title("Introducción al Dashboard de Farmacias en Baja California, Tijuana 📘 ")
#explicacion
st.markdown("""
Este dashboard presenta un análisis descriptivo de la distribución y características de las farmacias en **Tijuana**,  
basado en el *Directorio Estadístico Nacional de Unidades Económicas (DENUE) del INEGI*.

### ¿Qué podrás visualizar? 📌
- Colonias con mayor concentración de farmacias 🗺️ 
- Farmacias con vs sin consultorio  😷
- Cadenas con más presencia en la ciudad  🏢
- Modelos de operación y tamaño de establecimientos  ✅
- Mapa interactivo por colonia    
- Distribución por tipo de vialidad  

### Objetivo 🎯 
Brindar una visión clara, moderna y profesional del ecosistema de farcamacias en Tijuana.
""")
# tabla filtrada
st.subheader(" Dataframe General de Farmacias en Tijuana 📄")
st.dataframe(df_tijuana, width=1200, height=300)

st.markdown(
        """
        <hr style="
            height:4px;
            border:none;
            background: linear-gradient(to right, #59a1ff, #0c50a8);
        " />
        """,
        unsafe_allow_html=True)
# ==============================
# 1. Colonias con más farmacias
# ==============================
st.subheader("1️⃣ Top Colonias con más Farmacias en Tijuana ")

# Slider para elegir cuántas colonias mostrar o buscador
top_n = st.slider("Colonias a mostrar:", 5, 50, 20, key="inc1_topn")
buscar = st.text_input("Buscar colonia:", "", key="inc1_search")

# Copia del dataframe
df1 = df_colonia.copy()
df1 = df1.sort_values("Num_Farmacias", ascending=False)

if buscar.strip():
    df1 = df1[df1["Colonia"].str.contains(buscar, case=False, na=False)]

# Luego aplicamos el top_n
df1 = df1.head(top_n)

# Gráfica 1: Barras
fig1 = px.bar(
    df1,
    x="Colonia",
    y="Num_Farmacias",
    text="Num_Farmacias",
    color="Num_Farmacias",
    color_continuous_scale=PALETA_AZUL_VERDE
)
fig1.update_traces(textposition="inside", textfont=dict(size=14, color="white"))
fig1.update_layout(
    title=f"Top {len(df1)} Colonias con más Farmacias",
    xaxis_title="Colonia",
    yaxis_title="Número de Farmacias",
    coloraxis_showscale=False
)

#Gráfica 2: Burbujas se ve bonis
fig11 = px.scatter(
    df1,
    x="Colonia",
    y="Num_Farmacias",
    size="Num_Farmacias",
    hover_name="Colonia",
    size_max=60,
    color="Num_Farmacias",
    color_continuous_scale=PALETA_AZUL_VERDE,
    title="Representación tipo Bubble (Tamaño = Número de Farmacias)"
)
fig11.update_traces(marker=dict(line=dict(width=1, color="#0D47A1")))

#esto es para que se vean lado a lado
col1, col2 = st.columns(2)
col1.plotly_chart(fig1, use_container_width=True)
col2.plotly_chart(fig11, use_container_width=True)
#explicacion
with st.expander("Mirar explicación"):
    st.write('''
            Este gráfico muestra las colonias que queramos,
            muestre las primeras 10 colonias, mas sin embargo puede ver todas y su presencia en la ciudad de Tijuana.''')
#Divisor bonito con markdown
st.markdown(
        """
        <hr style="
            height:4px;
            border:none;
            background: linear-gradient(to right, #59a1ff, #0c50a8);
        " />
        """,
        unsafe_allow_html=True)
# ==============================
# 2. Porcentaje de consultorios
# ==============================
st.subheader("2️⃣ Porcentaje farmacias con Consultorios y sin Consultorios📊")
#de agrupacion consultorios se saca para esta figura de porcentajes
fig2 = px.pie(
    df_consultorio,
    values="Porcentaje",
    names="Consultorio",
    title="Porcentaje de farmacias con consultorio",
    hole=0.35,
    color_discrete_sequence=PALETA_AZUL_VERDE
)
st.plotly_chart(fig2, use_container_width=True)
#explicacion
with st.expander("Mirar explicación"):
    st.write('''
            Este gráfico muestra el porcentaje de farmacias que cuentan con consultorio en comparación con aquellas que no lo tienen en Tijuana.''')
st.markdown(
        """
        <hr style="
            height:4px;
            border:none;
            background: linear-gradient(to right, #59a1ff, #0c50a8);
        " />
        """,
        unsafe_allow_html=True)
# ==============================
# 3. Métricas Consultorios
# ==============================
st.subheader("3️⃣ Total y Porcentajes de Consultorios")

# Totales a partir del df_consultorio del punto 2
total_si = df_consultorio[df_consultorio["Consultorio"].str.lower() == "si"]["Num_Farmacias"].sum()
total_no = df_consultorio[df_consultorio["Consultorio"].str.lower() == "no"]["Num_Farmacias"].sum()

total_farmacias = total_si + total_no
#aqui sumamos los que si y los que no para confirmar la suma total
porc_si = (total_si / total_farmacias) * 100 # sacamos porcentaje
porc_no = (total_no / total_farmacias) * 100 # sacamos porcentaje

col1, col2, col3 = st.columns(3) #para que quede una al lado de la otra
col1.metric("Total de Farmacias", int(total_farmacias))
col2.metric("Con Consultorio", f"{total_si} ({porc_si:.2f}%)")
col3.metric("Sin Consultorio", f"{total_no} ({porc_no:.2f}%)")
st.markdown(
        """
        <hr style="
            height:4px;
            border:none;
            background: linear-gradient(to right, #59a1ff, #0c50a8);
        " />
        """,
        unsafe_allow_html=True)
# ==============================
# 4. Top cadenas
# ==============================
st.subheader("4️⃣ Participación Total de Cadenas en Tijuana 📊")
cadenas_agrupado = CadenasTijuana(df)

# Ordenar de mayor a menor (sin limitar a 20)
cadenas_ordenadas = cadenas_agrupado.sort_values(
    by="Num_Farmacias", ascending=False
)

fig4 = px.pie(
    cadenas_ordenadas,
    names="Nombre",
    values="Num_Farmacias",
    title="Participación total de todas las cadenas en Tijuana (Agrupación)",
    hole=0.4,
    color_discrete_sequence=PALETA_AZUL_VERDE
)
st.plotly_chart(fig4, use_container_width=True)
#explicacion
with st.expander("Mirar explicación"):
    st.write('''
            Este gráfico muestra la participación total de todas las cadenas/empresas de farmacias en Tijuana.''')
st.markdown(
        """
        <hr style="
            height:4px;
            border:none;
            background: linear-gradient(to right, #59a1ff, #0c50a8);
        " />
        """,
        unsafe_allow_html=True)
# ==============================
# 5. Tamaño predominante
# ==============================
st.subheader("5️⃣ Tamaños de Farmacias según la Vialidad")

# Filtro único: tipo de vialidad
vialidad_select = st.selectbox(
    "Selecciona la vialidad para saber que tamanos predominan:",
    sorted(df_tijuana["Tipo_vialidad"].dropna().unique())
)

# Filtrar df por esa vialidad
df_vial = df_tijuana[df_tijuana["Tipo_vialidad"] == vialidad_select]

# Agrupar tamaños dinámicamente
df_tam_vial = (
    df_vial["Clasificacion_tamaño"]
    .value_counts()
    .reset_index()
)
df_tam_vial.columns = ["Tamaño", "Cantidad"]

fig5 = px.bar(
    df_tam_vial,
    x="Tamaño",
    y="Cantidad",
    text="Cantidad",
    title=f"Tamaños de farmacias en la vialidad: {vialidad_select}",
    color="Tamaño",
    color_discrete_sequence=PALETA_AZUL_VERDE
)

fig5.update_traces(textposition="outside")
fig5.update_layout( #update para configurar la figura un update layout
    xaxis_title="Tamaño del establecimiento",
    yaxis_title="Número de farmacias"
)
st.plotly_chart(fig5, use_container_width=True)
#explicacion
with st.expander("Mirar explicación"):
    st.write('''
            Este gráfico puede filtrar por vialidad y se muestra segun la vialidad, la cantidad de los tamaños de farmacias que hay.''')

# Gráfica total no interactiva de agrupaciones
st.subheader(" Totales Tamaño Predominante de Farmacias 📦")
fig51 = px.bar(
    df_tamano,
    x="Clasificacion_tamaño",
    y="Num_Farmacias",
    title="Distribución por tamaño de farmacia",
    color="Clasificacion_tamaño",
    color_discrete_sequence=PALETA_AZUL_VERDE
)
st.plotly_chart(fig51, use_container_width=True)
#explicacion
with st.expander("Mirar explicación"):
    st.write('''
            Este gráfico muestra la suma total por los diferentes tamaños de farmacias que hay en Tijuana.''')
st.markdown(
        """
        <hr style="
            height:4px;
            border:none;
            background: linear-gradient(to right, #59a1ff, #0c50a8);
        " />
        """,
        unsafe_allow_html=True)
# ==============================
# 6. Clase de actividad (Treemap)
# ==============================
#grafica no inveractiva de agrupaciones
st.subheader("6️⃣ Farmacias por Clase de Actividad 🏷️🧩")
fig6 = px.treemap(
    df_servicios,
    path=["Clase_actividad"],
    values="Num_Farmacias",
    title="Distribución por clase de actividad",
    color="Clase_actividad",
    color_discrete_sequence=PALETA_AZUL_VERDE
)
fig6.update_traces(
    textfont=dict(
        color="white",  # azul profesional
        size=18,  # más grande y visible
        family="Roboto"
    ),
    marker=dict(
        line=dict(
            color="#0D47A1",  # borde azul
            width=2  # grosor
        )
    )
)
st.plotly_chart(fig6, use_container_width=True)
#explicacion
with st.expander("Mirar explicación"):
    st.write('''
            Este gráfico muestra en totalidad que clase_actividad 
            predomina en las farmacias de Tijuana''')
#una agrupacion extra para ver la relacion entre clase_actividad y nombre usando el df original
clase_count = df_tijuana.groupby(["Clase_actividad", "Nombre"]).size().reset_index(name="Total")
fig61 = px.bar(clase_count, x="Clase_actividad", y="Total", color="Nombre",
              title="Farmacias por clase de actividad")
st.plotly_chart(fig61, use_container_width=True)
#explicacion
with st.expander("Mirar explicación"):
    st.write('''
            Este gráficoy se pueden ver las diferentes farmacias; muestra que clase_actividad predomina en las farmacias 
            de Tijuana.''')
st.markdown(
        """
        <hr style="
            height:4px;
            border:none;
            background: linear-gradient(to right, #59a1ff, #0c50a8);
        " />
        """,
        unsafe_allow_html=True)
# ==============================
# 7. Mapa interactivo
# ==============================
st.subheader("7️⃣ Distribución Geográfica de Farmacias 🗺️")

colonias = sorted(df_tijuana["Colonia"].dropna().unique())
#este es el filto intectivo para seleccionar las colonias
filtro = st.multiselect("Selecciona una colonia en el municipio para saber que tipo de farmacias encuentras:", colonias)
df_mapa = df_tijuana if not filtro else df_tijuana[df_tijuana["Colonia"].isin(filtro)]
#acomodamos nuestras variables para el mapa
fig7 = px.scatter_mapbox(
    df_mapa,
    lat="Latitud",
    lon="Longitud",
    hover_name="Nombre",
    hover_data=["Colonia", "Consultorio", "Clase_actividad"],
    color="Colonia",
    zoom=10,
    height=500,
    color_discrete_sequence=PALETA_AZUL_VERDE
)
fig7.update_layout(mapbox_style="open-street-map") #se configura el mapa/figura
st.plotly_chart(fig7, use_container_width=True)
#explicacion
with st.expander("Mirar explicación"):
    st.write('''
            Este mapa interactivo de Tijuana, Baja california, 
            permite a los usuarios explorar la distribución geográfica 
            de las farmacias por la colonia que queramos en la ciudad.''')
st.markdown(
        """
        <hr style="
            height:4px;
            border:none;
            background: linear-gradient(to right, #59a1ff, #0c50a8);
        " />
        """,
        unsafe_allow_html=True)
# ==============================
# 8. Cadena vs independiente
# ==============================
st.subheader("8️⃣ Modelos de Farmacia — Cadena o Independiente 🏪")

# Filtro por colonia
colonia_8 = st.selectbox(
    "Selecciona una colonia (opcional) para saber si destacan farmacias de cadena o independientes en dicha colonia:",
    ["Todas"] + sorted(df_tijuana["Colonia"].dropna().unique()),
    key="filtro_inc8"
)

# Filtrar dataframe
df_filtrado_8 = df_tijuana.copy()
if colonia_8 != "Todas":
    df_filtrado_8 = df_tijuana[df_tijuana["Colonia"] == colonia_8]

# Agrupar modelo
df_modelo_filtro = (
    df_filtrado_8["Modelo_farmacia"]
    .value_counts()
    .reset_index()
)
df_modelo_filtro.columns = ["Modelo_farmacia", "Num_Farmacias"]

#Grafica dona
fig81 = px.pie(
    df_modelo_filtro,
    names="Modelo_farmacia",
    values="Num_Farmacias",
    hole=0.45,
    title=f"Modelo de farmacia en {colonia_8}",
    color_discrete_sequence=PALETA_AZUL_VERDE
)
fig81.update_traces(
    textinfo="percent+label",
    textfont_size=16
)
st.plotly_chart(fig81, use_container_width=True)
#explicacion
with st.expander("Mirar explicación"):
    st.write('''
            Este gráfico puede filtrar por la colonia que nosotros queramos spara mostrar la distribución entre farmacias que operan como parte 
            de una cadena y aquellas que son independientes en Tijuana.''')
#en este total que no es interactivo usamos nuestra agrupacion
st.subheader("Total de Modelos de Farmacia Cadena o Independientes 🏪")

fig81= px.pie(
    df_modelo,
    names="Modelo_farmacia",
    values="Num_Farmacias",
    hole=0.45,
    title="Distribución Total: Cadenas vs Independientes",
    color_discrete_sequence=PALETA_AZUL_VERDE
)
fig81.update_traces(
    textinfo="percent+label",
    textfont_size=16
)
st.plotly_chart(fig81, use_container_width=True)
#explicacion
with st.expander("Mirar explicación"):
    st.write('''
            Este gráfico muestra la distribución total entre farmacias que operan como parte de una cadena y aquellas que son independientes en Tijuana.''')
st.markdown(
        """
        <hr style="
            height:4px;
            border:none;
            background: linear-gradient(to right, #59a1ff, #0c50a8);
        " />
        """,
        unsafe_allow_html=True)
# ==============================
# 9. Tipo de vialidad
# ==============================
st.subheader("9️⃣ Farmacias por Tipo de Vialidad 🚗")
#en esta figura simplemente mandamos a llamar la agrupacion de vialidades
fig9 = px.scatter(
    df_vialidad,
    x="Num_Farmacias",
    y="Tipo_vialidad",
    size=[15]*len(df_vialidad),
    color_discrete_sequence=PALETA_AZUL_VERDE
)
fig9.update_traces(mode="markers+lines", line=dict(width=2))
st.plotly_chart(fig9, use_container_width=True)
#explicacion
with st.expander("Mirar explicación"):
    st.write('''
            Este gráfico muestra las farmacias distribuidas según el tipo de vialidad en Tijuana.''')
st.markdown(
        """
        <hr style="
            height:4px;
            border:none;
            background: linear-gradient(to right, #59a1ff, #0c50a8);
        " />
        """,
        unsafe_allow_html=True)