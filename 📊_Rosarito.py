import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import pandas as pd
from AgrupacionesRosarito import agrupacionRosarito
from AgrupacionesRosarito import consultoriosPorcentaje
from AgrupacionesRosarito import cadenasRosarito
from AgrupacionesRosarito import tamaFarmaR
from AgrupacionesRosarito import servicioR
from AgrupacionesRosarito import modeloFarmaciaRosarito
from AgrupacionesRosarito import tipoVialidadR


farmaciasCompletoLimpio=pd.read_csv("farmaciasCompletoLimpio.csv")

def stremlitApp():
    #Titulo
    st.markdown(
        """
        <h1 style='text-align:center; color:#003f88; font-size:2.2rem; font-weight:600;'>
            Dashboard Playas de Rosarito 📊👩🏻‍⚕️
        </h1>
        """,
        unsafe_allow_html=True
    )


    #Divisor
    st.markdown(
        """
        <hr style="
            height:4px;
            border:none;
            background: linear-gradient(to right, #59a1ff, #0c50a8);
        " />
        """,
        unsafe_allow_html=True
    )

    #Musiquia para relajarse mientras lo ven
    st.audio("MusicaLofi.mp3", format="audio/mpeg", loop=True)

    # Divisor bonito con markdown
    st.markdown(
        """
        <hr style="
            height:4px;
            border:none;
            background: linear-gradient(to right, #59a1ff, #0c50a8);
        " />
        """,
        unsafe_allow_html=True
    )


#Mapa de puntos de rosarito, se puede filtrar por colonia
def mapaFarmaciasColorRosarito(farmaciasCompletoLimpio):
    Rosarito = farmaciasCompletoLimpio[farmaciasCompletoLimpio['Ubicacion'] == 'PLAYAS DE ROSARITO']

    st.subheader("Mapa de farmacias en Rosarito")

    colonias = sorted(Rosarito['Colonia'].dropna().unique())
    colonias_opciones = ['Todas'] + list(colonias)
    colonia_seleccionada = st.selectbox(
        "Selecciona una colonia:",
        colonias_opciones
    )

    #Filtramos de acuerdo a la seleccion
    if colonia_seleccionada == 'Todas':
        datos_filtrados = Rosarito
    else:
        datos_filtrados = Rosarito[Rosarito['Colonia'] == colonia_seleccionada]

    #Con esto mostramos cuantas farmacias hay en cada colonia dependiendo el filtro !!!
    st.write(f"Mostrando {len(datos_filtrados)} farmacias")

    #Mapa de puntos !!!
    mapa_data = datos_filtrados[['Latitud', 'Longitud']].copy()
    mapa_data.columns = ['latitude', 'longitude']

    st.map(mapa_data, zoom=11, size=20, color='#6ba7db')

    with st.expander("Mirar explicación"):
        st.write('''
            Este gráfico muestra las ubicaciones de todas las farmacias en 
            Rosarto, podemos filtrarlo por colonias y a su vez, muestra un 
            conteo de cuantas farmacias hay en cada colonia cuando lo filtramos. 
        ''')

    #Divisor bonito con markdown
    st.markdown(
        """
        <hr style="
            height:4px;
            border:none;
            background: linear-gradient(to right, #59a1ff, #0c50a8);
        " />
        """,
        unsafe_allow_html=True
    )

#Grafico del top 10 colonias con mas farmacias
def graficoTopColoniasRosarito(farmaciasCompletoLimpio):
    df_colonias = agrupacionRosarito(farmaciasCompletoLimpio).sort_values(
        'Num_Farmacias', ascending=False).head(10)

    st.subheader("Top 10 colonias con mas farmacias en Rosarito 💊")


    fig = px.bar(
        df_colonias,
        x='Num_Farmacias',
        y='Colonia',
        orientation='h',
        color='Num_Farmacias',
        title='Top 10 colonias con mas farmacias en Rosarito 🏥'
    )

    fig.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig, use_container_width=True)

    #Explicacion del grafico
    with st.expander("Mirar explicación"):
        st.write('''
            Este gráfico de barras muestra las 10 colonias del municipio de Rosarito
            con mayor concentración de farmacias. Este tipo de visualización 
            permite identificar de manera clara cuáles zonas cuentan con más 
            establecimientos de este tipo, lo que refleja tanto la demanda local
            de servicios de salud como la distribución territorial de la oferta farmacéutica.
        ''')
    # Divisor bonito con markdown
    st.markdown(
        """
        <hr style="
            height:4px;
            border:none;
            background: linear-gradient(to right, #59a1ff, #0c50a8);
        " />
        """,
        unsafe_allow_html=True
    )
    return df_colonias

#Frafico de pastel para mostrar el total de farmacias con o sin consultorios
def graficoConsultoriosRosarito(farmaciasCompletoLimpio):
    df_con = consultoriosPorcentaje(farmaciasCompletoLimpio)
    st.subheader("Total de farmacias con y sin consultorios")


    #Creamos el grafico de pastel para esta agrupación
    fig = px.pie(
        df_con,
        names="Consultorio",
        values="Num_Farmacias",
        title="Farmacias con consultorio vs sin consultorio ⚕️",
        hole=0.40
    )
    fig.update_traces(textinfo="percent+label")

    st.plotly_chart(fig, use_container_width=True)

    #Metricas para mostrar abajo del grafico de pastel
    total = df_con["Num_Farmacias"].sum()
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total de Farmacias", total)

    #Las filtramos para obtener el valor de cada metrica
    con = df_con[df_con["Consultorio"] == "SI"]["Num_Farmacias"].values[0]
    porc_con = df_con[df_con["Consultorio"] == "SI"]["Porcentaje"].values[0]

    sin = df_con[df_con["Consultorio"] == "NO"]["Num_Farmacias"].values[0]
    porc_sin = df_con[df_con["Consultorio"] == "NO"]["Porcentaje"].values[0]

    with col2:
        st.metric("Con Consultorio", f"{con} ({porc_con}%)")

    with col3:
        st.metric("Sin Consultorio", f"{sin} ({porc_sin}%)")

    #Explicacion del grafico
    with st.expander("Mirar explicación"):
        st.write('''
            Este gráfico de pastel muestra la proporción de farmacias en Rosarito
            que cuentan con consultorio médico frente a aquellas que no lo tienen. 
            Esta visualización permite identificar de manera clara el nivel de 
            integración de servicios de salud adicionales dentro de las farmacias del municipio.
        ''')

    # Divisor bonito con markdown
    st.markdown(
        """
        <hr style="
            height:4px;
            border:none;
            background: linear-gradient(to right, #59a1ff, #0c50a8);
        " />
        """,
        unsafe_allow_html=True
    )

    return df_con

#Grafico treemap para mostrar las cadenas de rosarito
def graficoCadenasRosarito(farmaciasCompletoLimpio):
    cadenasR = cadenasRosarito(farmaciasCompletoLimpio)
    st.subheader("Cadenas de farmacias predominantes en Rosarito")


    #Hacemos un treemap para las cadenas de farmacias
    fig = px.treemap(cadenasR,
                     path=['Nombre'],
                     values='Num_Farmacias',
                     title='Cadenas de farmacias predominantes en Rosarito 💊🏥',
                     color='Num_Farmacias',
                     color_continuous_scale='Blues',
                     hover_data={'Num_Farmacias': True})

    fig.update_traces(
        textinfo="label+value+percent root",
        textfont_size=14
    )

    fig.update_layout(height=500)

    st.plotly_chart(fig, use_container_width=True)

    #Explicacion del grafico
    with st.expander("Mirar explicación"):
        st.write('''
            Este gráfico tipo treemap muestra la distribución de las principales cadenas 
            de farmacias en Rosarito, destacando el número de establecimientos que cada 
            una concentra en el municipio. Esta visualización permite identificar de 
            manera clara cuáles cadenas tienen mayor presencia y cómo se comparan entre 
            sí en términos de cobertura.
        ''')

    # Divisor bonito con markdown
    st.markdown(
        """
        <hr style="
            height:4px;
            border:none;
            background: linear-gradient(to right, #59a1ff, #0c50a8);
        " />
        """,
        unsafe_allow_html=True
    )

    return cadenasR


#Grafico  para el tamaño predominante de farmacias en rosarito
def graficoTamanoFarmaciasRosarito(farmaciasCompletoLimpio):
    tamaR = tamaFarmaR(farmaciasCompletoLimpio)


    st.subheader("Tamaño predominante de farmacias en Rosarito 📏🏥")

    fig = go.Figure()

    #Lineas del grafico
    fig.add_trace(go.Scatter(
        x=tamaR["Num_Farmacias"],
        y=tamaR["Clasificacion_tamaño"],
        mode="lines",
        line=dict(width=2, color="gray"),
        name="Líneas"
    ))

    #Puntos del grafico
    fig.add_trace(go.Scatter(
        x=tamaR["Num_Farmacias"],
        y=tamaR["Clasificacion_tamaño"],
        mode="markers",
        marker=dict(size=20, color="#6ba7db", line=dict(width=1, color="Blue")),
        name="Puntos"
    ))

    fig.update_layout(
        title="Tamaño predominante de farmacias en Rosarito",
        xaxis_title="Número de farmacias",
        yaxis_title="Clasificación de tamaño",
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)

    with st.expander("Mirar explicación"):
        st.write('''
            Este gráfico del tipo lollipop, muestra la clasificación de farmacias
            en Rosarito según su tamaño, representando tanto las líneas de tendencia 
            como los puntos de cada categoría. Esta visualización permite observar 
            cuántas farmacias existen en cada clasificación de tamaño y facilita la 
            comparación entre ellas.
        ''')


    # Divisor bonito con markdown
    st.markdown(
        """
        <hr style="
            height:4px;
            border:none;
            background: linear-gradient(to right, #59a1ff, #0c50a8);
        " />
        """,
        unsafe_allow_html=True
    )

    return tamaR


def graficoServiciosRosarito(farmaciasCompletoLimpio):
    servicios = servicioR(farmaciasCompletoLimpio)

    st.subheader("Tipos de servicios de farmacias en Rosarito 💊")

    fig = px.sunburst(
        servicios,
        path=["Clase_actividad"],
        values="Num_Farmacias",
        color="Num_Farmacias",
        color_continuous_scale="Blues",
        title="Servicios ofrecidos en farmacias de Rosarito"
    )

    fig.update_traces(
        textinfo="label+value+percent entry",
        marker=dict(line=dict(width=1, color="white"))
    )

    fig.update_layout(
        margin=dict(t=50, l=10, r=10, b=10),
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)

    #Explicacion del grafico
    with st.expander("Mirar explicación"):
        st.write('''
            Este gráfico del tipo sunsburn miestra los diferentes servicios 
            ofrecidos en las farmacias de Rosarito, podemos ver el porcentaje
            de cada uno de estos servicios para iodentificar cual se ofrece en las farmacias.
        ''')

    # Divisor bonito con markdown
    st.markdown(
        """
        <hr style="
            height:4px;
            border:none;
            background: linear-gradient(to right, #59a1ff, #0c50a8);
        " />
        """,
        unsafe_allow_html=True
    )
    return servicios

#Grafico de barras para el modelo de farmacia
def graficoModeloFarmaciaRosarito(farmaciasCompletoLimpio):
    ModeloR = modeloFarmaciaRosarito(farmaciasCompletoLimpio)
    st.subheader("Modelos de farmacias en Rosarito")


    fig = px.bar(
        ModeloR,
        x="Modelo_farmacia",
        y="Num_Farmacias",
        title="Número de farmacias por modelo en Rosarito",
    )

    st.plotly_chart(fig, use_container_width=True)

    #Explicacion del grafico
    with st.expander("Mirar explicación"):
        st.write('''
            Este gráfico de barras muestra la cantidad de farmacias de cadenas
            grandes y las farmacias independiente. Esta visualización permite 
            identificar la estructura del mercado farmacéutico local, mostrando 
            qué tipo de establecimiento tiene mayor presencia en el municipio.
        ''')

    # Divisor bonito con markdown
    st.markdown(
        """
        <hr style="
            height:4px;
            border:none;
            background: linear-gradient(to right, #59a1ff, #0c50a8);
        " />
        """,
        unsafe_allow_html=True
    )


def graficoBubbleTipoVialidad(farmaciasCompletoLimpio):
    vialidadesR = tipoVialidadR(farmaciasCompletoLimpio)
    st.subheader("Numero de farmacias por vialidad en Rosarito")


    fig = px.scatter(
        vialidadesR,
        x="Tipo_vialidad",
        y="Num_Farmacias",
        size="Num_Farmacias",
        color="Tipo_vialidad",
        hover_name="Tipo_vialidad",
        size_max=60,
        title="Farmacias por tipo de vialidad",
    )

    fig.update_layout(
        xaxis_title="Tipo de vialidad",
        yaxis_title="Número de farmacias",
        height=550,
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)

    # Explicacion del grafico
    with st.expander("Mirar explicación"):
        st.write('''
             Este gráfico de burbujas representa la cantidad de farmacias 
             en Rosarito según el tipo de vialidad donde se ubican, como 
             calles, avenidas, bulevares y carreteras. Cada burbuja refleja 
             el número de establecimientos asociados a cada categoría, 
             permitiendo visualizar de forma clara la concentración de 
             farmacias en distintos entornos urbanos. Destaca que la mayoría 
             se localiza en calles y bulevares, lo que sugiere una preferencia 
             por zonas de tránsito local y comercial. 
         ''')

    # Divisor bonito con markdown
    st.markdown(
        """
        <hr style="
            height:4px;
            border:none;
            background: linear-gradient(to right, #59a1ff, #0c50a8);
        " />
        """,
        unsafe_allow_html=True
    )

if __name__ == '__main__':
    stremlitApp()
    mapaFarmaciasColorRosarito(farmaciasCompletoLimpio)
    graficoTopColoniasRosarito(farmaciasCompletoLimpio)
    graficoConsultoriosRosarito(farmaciasCompletoLimpio)
    graficoCadenasRosarito(farmaciasCompletoLimpio)
    graficoTamanoFarmaciasRosarito(farmaciasCompletoLimpio)
    graficoServiciosRosarito(farmaciasCompletoLimpio)
    graficoModeloFarmaciaRosarito(farmaciasCompletoLimpio)
    graficoBubbleTipoVialidad(farmaciasCompletoLimpio)