import altair as alt
import plotly.express as px
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from diccionario_estado import dicc
from AgrupacionesEstado import (farmaciasMunicipio, farmaciasconsultorio,
                               consultorioporcentaje, porcentajefarmacias,
                               vialidadfarmacias, tamanofarmacia, cadenaspredominantes,
                               farmaciasservicio, independienteocadena)
farmaciasCompletoLimpio = pd.read_csv("farmaciasCompletoLimpio.csv")

LOGO_URL = "https://images.vexels.com/media/users/3/136559/isolated/preview/624dd0a951a1e8a118215b1b24a0da59-logotipo-de-farmacia.png"
st.logo(
    LOGO_URL,
    icon_image=LOGO_URL,
    size="large"
)


def graficas():
    # GRAFICA 1
    fig_mapa = px.scatter_map(dicc,
                        lat="Latitud",
                        lon="Longitud",
                        hover_name= "Nombre",
                        zoom=7)


    #GRAFICA 2
    #lo hare en una escala y que cada barra sea un municipio para facilitar la lectura

    source = farmaciasMunicipio(farmaciasCompletoLimpio) #llamo la función
    escala = alt.Scale(
        domain = ["ENSENADA", "MEXICALI", "PLAYAS DE ROSARITO", "SAN FELIPE", "SAN QUINTIN", "TECATE", "TIJUANA"],
        range= ["#ade8f4", "#90e0ef", "#48cae4", "#00b4d8", "#0096c7", "#0077b6", "#023e8a"]
    ) #personalizamos

    #con esto hacemos que resalte la barra cuando pasa el mouse
    highlight = alt.selection_single(on='mouseover', fields=['Ubicacion'], empty='all')

    #creamos barritas
    fig_totalfarmacias = (
        alt.Chart(source)
        .mark_bar()
        .encode(
            x=alt.X("Numero_farmacias:Q", title="Total de farmacias"),
            y=alt.Y("Ubicacion:N", title="Municipio", sort="-x"),
            color=alt.condition(highlight,
                                alt.Color("Ubicacion:N", scale=escala),
                                alt.value("lightgray")))
            .add_params(highlight)
            .properties(width=600, height=350))

    #GRAFICA 3
    source3 = porcentajefarmacias(farmaciasCompletoLimpio)

    #colores q usaremmos
    colores = ["#ade8f4", "#90e0ef", "#48cae4", "#00b4d8", "#0096c7", "#0077b6", "#023e8a"]

    fig_farmaciasporcentaje = px.pie(
        source3,
        names="Ubicacion",
        values="Numero_farmacias",
        color="Ubicacion",
        color_discrete_sequence=colores,
        hole=0)

    fig_farmaciasporcentaje.update_traces(textinfo='percent+label',
                                          marker=dict(line=dict(color='white', width=2)))


    #GRAFICA 4
    source1 = farmaciasconsultorio(farmaciasCompletoLimpio)
    escala1 = alt.Scale(
        domain = ["ENSENADA", "MEXICALI", "PLAYAS DE ROSARITO", "SAN FELIPE", "SAN QUINTIN", "TECATE", "TIJUANA"],
        range= ["#ade8f4", "#90e0ef", "#48cae4", "#00b4d8", "#0096c7", "#0077b6", "#023e8a"]
    ) #personalizamos

    #con esto hacemos que resalte la barra cuando pasa el mouse
    highlight = alt.selection_single(on='mouseover', fields=['Ubicacion'], empty='all')

    #creamos barritas
    fig_consultorio = (
        alt.Chart(source1)
        .mark_bar()
        .encode(
            x=alt.X("Numero_farmacias:Q", title="Total de farmacias con consultorio"),
            y=alt.Y("Ubicacion:N", title="Municipio", sort="-x"),
            color=alt.condition(highlight,
                                alt.Color("Ubicacion:N", scale=escala1),
                                alt.value("lightgray")))
            .add_params(highlight)
            .properties(width=600, height=350))

    # GRAFICA 5
    source2 = farmaciasconsultorio(farmaciasCompletoLimpio)
    df_porcentaje = consultorioporcentaje(source2)

    # esta gráfica será de pasteles para representar los porcentajes
    fig_consultorioporentaje = px.pie(
        df_porcentaje,
        names="Ubicacion",
        values="Numero_farmacias",
        title=" % farmacias con consultorio⚕️",
        hole=0.30,
        color="Ubicacion",
        color_discrete_sequence=colores)
    fig_consultorioporentaje.update_traces(textinfo="percent+label")


    #GRAFICA 6
    source4 = vialidadfarmacias(farmaciasCompletoLimpio)
    fig_farmaciasvialidad = px.bar(
        source4,
        x = "Numero_farmacias",
        y="Tipo_vialidad",
        orientation="h",
        color="Tipo_vialidad",
        animation_frame="Ubicacion",
        labels={
            "Tipo_vialidad": "Tipo de vialidad",
            "Numero_farmacias": "Total de farmacias",
            "color": "Categoría"},
        title="Vialidades",
        color_discrete_sequence=colores)

    #para q aparezcan ordenadas
    fig_farmaciasvialidad.update_layout(
    title_x=0.5,
    yaxis=dict(categoryorder="total ascending"))

    #bordecitos y un buen hover
    fig_farmaciasvialidad.update_traces(
    hovertemplate="<b>%{y}</b><br>Total: %{x} farmacias<extra></extra>",
    marker=dict(line=dict(color="white", width=1)))


    #GRAFICA 7
    source5 = tamanofarmacia(farmaciasCompletoLimpio)

    fig_tamanofarmacia = px.scatter(
        source5,
        x="Clasificacion_tamaño",
        y="Numero_farmacias",
        size="Numero_farmacias",
        color="Clasificacion_tamaño",
        hover_name="Clasificacion_tamaño",
        size_max=60,
        title="Farmacias por tamaño.")

    fig_tamanofarmacia.update_layout(
        xaxis_title="Clasificacion_tamaño",
        yaxis_title="Número de farmacias",
        height=550,
        showlegend=False)


    #GRAFICA 8
    source6 = cadenaspredominantes(farmaciasCompletoLimpio).head(10)

    fig_cademapredo = go.Figure()

    #las líneas del gráfico
    fig_cademapredo.add_trace(go.Scatter(
        x=source6["Numero_farmacias"],
        y=source6["Nombre"],
        mode="lines",
        line=dict(width=2, color="gray"),
        name="Líneas"))

    #puntitos del gráfico
    fig_cademapredo.add_trace(go.Scatter(
        x=source6["Numero_farmacias"],
        y=source6["Nombre"],
        mode="markers",
        marker=dict(size=18, color="#6ba7db", line=dict(width=1, color="Blue")),
        name="Número de farmacias"))

    fig_cademapredo.update_layout(
        title="Cadenas predominante de farmacias en BC",
        xaxis_title="Número de farmacias",
        yaxis_title="Cadena",
        height=500)


    #GRAFICO 9
    source7 = farmaciasservicio(farmaciasCompletoLimpio, top_n=10)

    fig_servicio = px.bar(
    source7,
    x="Numero_farmacias",
    y="Clase_actividad",
    orientation="h",
    title="Farmacias por servicios otorgados🩺")

    fig_servicio.update_layout(
        xaxis_title="Número farmacias",
        yaxis_title="Servicio",
        height=700)

    #GRAFICA 10
    source8 = independienteocadena(farmaciasCompletoLimpio)

    fig_modelo = px.treemap(source8,
                     path=['Modelo_farmacia'],
                     values='Numero_farmacias',
                     title='Farmacias por modelo🏥',
                     color='Numero_farmacias',
                     color_continuous_scale='Blues',
                     hover_data={'Numero_farmacias': True})

    fig_modelo.update_traces(
        textinfo="label+value+percent root",
        textfont_size=14)

    fig_modelo.update_layout(height=500)



    return (fig_mapa, fig_totalfarmacias, fig_farmaciasporcentaje,
            fig_consultorio, fig_consultorioporentaje,fig_farmaciasvialidad,
            fig_tamanofarmacia, fig_cademapredo, fig_servicio, fig_modelo)

def app_streamlit():
    #te permite abrir todas tus gráficas juntas

    #logo del estado d bc
    st.markdown("""
    <div style='text-align: center;'>
        <img src='https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/Escudo_Baja_California.png/626px-Escudo_Baja_California.png' 
             width='180'>

    </div>
    """, unsafe_allow_html=True)
    #título
    st.markdown(
        """
        <h1 style='text-align:center; color:#003f88; font-size:3.2rem; font-weight:600;'>
            Dashboard estado de Baja California 🗺 ‍⚕
        </h1>
        """,
        unsafe_allow_html=True
    )
    st.write("En esta página se visualiza la distribución de las farmacias a lo largo de el estado"
             " de Baja California, siguiendo métricas impuestas por el equipo y abriendo el análisis para los siguientes dashboards.")  #texto

    (fig_mapa, fig_totalfarma, fig_farmaciasporcentaje,
     fig_consultorio, fig_consultorioporentaje, fig_farmaciasvialidad,
     fig_tamanofarmacia, fig_cademapredo, fig_servicio, fig_modelo) = graficas()

    #divisor !!!
    st.markdown(
        """
        <hr style="
            height:4px;
            border:none;
            background: linear-gradient(to right, #59a1ff, #0c50a8);
        " />
        """,
        unsafe_allow_html=True)
    #--------- PRIMERA GRAFICA ----------------
    st.subheader("Gráfica 1. 🗺️ Mapa de la distribución de farmacias en todo el estado.")  # es para subtítulos
    st.write("Este mapa tiene la intención de mostrar la distribución de todas las farmacias de Baja California,"
             " permitiendo la visualización de la concentración por municipio.")
    with st.expander("Instrucciones del mapa:"):
        st.write("""
        🔹 Utilice mouse para mejor interacción.\n  
        🔹 Scroll = Zoom in / Zoom out.\n  
        🔹 Click derecho: mover el mapa de izquierda a derecha / arriba a abajo.\n  
        🔹 Click izquierdo: deslizarse dentro del mapa.
        """)
    st.plotly_chart(fig_mapa, key= "grafico_mapita")  # lo que se ponga dentro del parentesis es lo que mostrara xq es como un .show()
    #solo que acomoda en orden de aparición

    #divisor !!!
    st.markdown(
        """
        <hr style="
            height:4px;
            border:none;
            background: linear-gradient(to right, #59a1ff, #0c50a8);
        " />
        """,
        unsafe_allow_html=True)
    #----------- SEGUNDA GRAFICA -------------------
    st.subheader("Gráfica 2. 🏥📍 Total de farmacias por municipio.")
    st.write("Esta escala tiene el propósito de mostrar la cantidad total de farmacias que hay por municipio.")
    with st.expander("Instrucciones del gráfico:"):
        st.write("""
        🔹 Al tener el cursor dentro de una barra en específico, podrá ver el total de farmacias exacto.
        """)
    st.altair_chart(fig_totalfarma, use_container_width=True)

    #divisor !!!
    st.markdown(
        """
        <hr style="
            height:4px;
            border:none;
            background: linear-gradient(to right, #59a1ff, #0c50a8);
        " />
        """,
        unsafe_allow_html=True)
    #---------- TERCERA GRAFICA ------------------
    st.subheader("Gráfica 3. 📊📍 Porcentaje de farmacias por municipio.")
    st.write("La gráfica muestra cómo se distribuyen las farmacias en el estado según el municipio. "
             "Cada sector representa el porcentaje de farmacias que se encuentran en ese municipio respecto al total del estado.")
    with st.expander("Instrucciones del gráfico:"):
        st.write("""
        🔹 Para interactuar con el gráfico, haga click en las casillas de los municipios.
        """)
    st.plotly_chart(fig_farmaciasporcentaje, width='stretch', key="grafico_porcentajefarmacias")

    #divisor !!!
    st.markdown(
        """
        <hr style="
            height:4px;
            border:none;
            background: linear-gradient(to right, #59a1ff, #0c50a8);
        " />
        """,
        unsafe_allow_html=True)
    #--------- CUARTA GRAFICA ------------------
    st.subheader("Gráfica 4. 🥼💉 Total de farmacias con consultorio.")
    st.write("Este gráfico muestra el total de farmacias con consultorio que hay por municipio. Cada barra es un municipio "
             "y la altura refleja la cantidad de consultorios con los que cuenta.")
    with st.expander("Instrucciones del gráfico:"):
        st.write("""
        🔹 Al tener el cursor dentro de una barra en específico, podrá ver el total de farmacias exacto.
        """)
    st.altair_chart(fig_consultorio, use_container_width=True)

    #divisor !!!
    st.markdown(
        """
        <hr style="
            height:4px;
            border:none;
            background: linear-gradient(to right, #59a1ff, #0c50a8);
        " />
        """,
        unsafe_allow_html=True)
    #--------- QUINTA GRAFICA -----------------
    st.subheader("Gráfica 5. 📊🩺 Porcentaje de farmacias con consultorio.")
    st.write("Este gráfico de pastel representa la proporción de consultorios por municipio. "
             "Cada sector indica la participación relativa de cada municipio en el total.")
    with st.expander("Instrucciones del gráfico:"):
        st.write("""
        🔹 Para interactuar con el gráfico, haga click en las casillas de los municipios.
        """)
    st.plotly_chart(fig_consultorioporentaje, width='stretch', key="grafico_porcentajeconsultorio") #se agregan las key xk son muchos plotly y se perroconfunde

    #divisor !!!
    st.markdown(
        """
        <hr style="
            height:4px;
            border:none;
            background: linear-gradient(to right, #59a1ff, #0c50a8);
        " />
        """,
        unsafe_allow_html=True)
    #--------- SEXTA GRAFICA ---------------
    st.subheader("Gráfica 6. 🚗 Total de farmacias por tipo de vialidad.")
    st.write("La gráfica muestra cuántas farmacias hay en cada tipo de vialidad, permitiendo ver cómo cambia la distribución dependiendo del municipio. "
             "Gracias a la animación, es fácil comparar las diferencias entre localidades.")
    with st.expander("Instrucciones del gráfico:"):
        st.write("""
        🔹 Para interactuar con el gráfico, haga click en las casillas de las vialidades.\n
        🔹 De click en el botón de reproducción (►) para ver la animación.\n
        🔹 Mantenga el cursor sobre una barra para ver la ubicación y el total de farmacias.  
        """)
    st.plotly_chart(fig_farmaciasvialidad, width='stretch', key="grafico_tipovialidad")

    #divisor !!!
    st.markdown(
        """
        <hr style="
            height:4px;
            border:none;
            background: linear-gradient(to right, #59a1ff, #0c50a8);
        " />
        """,
        unsafe_allow_html=True)
    #---------- SEPTIMA GRAFICA -------------
    st.subheader("Gráfica 7. 🏪 Tamaño de farmacia que predomina.")
    st.write("El gráfico muestra cuántas farmacias pertenecen a cada categoría de tamaño."
             "Las categorías aparecen ordenadas de mayor a menor, y el tamaño con el punto más largo hacia la derecha "
             "representa el tamaño predominante en el estado.")
    with st.expander("Instrucciones del gráfico:"):
        st.write("""
        🔹 Para interactuar con el gráfico, posicione el cursor en alguno de los círculos para obtener datos precisos.
        """)
    st.plotly_chart(fig_tamanofarmacia, use_container_width=True, key="grafico_tamanovia")

    #divisor !!!
    st.markdown(
        """
        <hr style="
            height:4px;
            border:none;
            background: linear-gradient(to right, #59a1ff, #0c50a8);
        " />
        """,
        unsafe_allow_html=True)
    #--------- OCTAVA GRAFICA ----------
    st.subheader("Gráfica 8. 🔝🔟 Cadenas de farmacias que predominan en el estado.")
    st.write("La gráfica muestra las 10 cadenas de farmacias con mayor presencia en Baja California, "
             "ordenadas de mayor a menor número de sucursales (ascendente). Cada punto representa cuántas farmacias tiene cada cadena, "
             "y la línea horizontal ayuda a visualizar esa cantidad de forma más clara.")
    with st.expander("Instrucciones del gráfico:"):
        st.write("""
        🔹 Para interactuar con el gráfico, posicione el cursor en alguno de los círculos para obtener datos precisos.
        """)
    st.plotly_chart(fig_cademapredo, use_container_width=True, key="grafico_cadenapredo")

    # divisor !!!
    st.markdown(
        """
        <hr style="
            height:4px;
            border:none;
            background: linear-gradient(to right, #59a1ff, #0c50a8);
        " />
        """,
        unsafe_allow_html=True)
    #--------- NOVENA GRAFICA --------------
    st.subheader("Gráfica 9. 🩺💊 Farmacias por servicio otorgado en el estado.")
    st.write("La gráfica de barras muestra cuántas farmacias ofrecen cada tipo de servicio dentro del estado. "
             "Cada barra representa una clase de actividad (por ejemplo: venta al público, consultorio, laboratorio, etc.) "
             "y su altura indica el número de establecimientos que brindan ese servicio.")
    with st.expander("Instrucciones del gráfico:"):
        st.write("""
        🔹 Para interactuar con el gráfico, posicione el cursor en alguna de las barras para obtener datos precisos.
        """)
    st.plotly_chart(fig_servicio, use_container_width=True, key="grafico_servicio")

    # divisor !!!
    st.markdown(
        """
        <hr style="
            height:4px;
            border:none;
            background: linear-gradient(to right, #59a1ff, #0c50a8);
        " />
        """,
        unsafe_allow_html=True)

    #---------- DECIMA GRAFICA ---------------
    st.subheader("Gráfica 10. 🏥Farmacias por modelo en el estado.")
    st.write("El treemap muestra cómo se distribuyen las farmacias según su modelo de operación, ya sea independientes "
             "o pertenecientes a una cadena. El tamaño de cada recuadro representa cuántas farmacias hay en cada categoría, "
             "mientras que el color indica la intensidad de su presencia.")
    with st.expander("Instrucciones del gráfico:"):
        st.write("""
        🔹 Para interactuar con el gráfico, posicione el cursor en alguna de las barras para obtener datos precisos.
        """)
    st.plotly_chart(fig_modelo, use_container_width=True, key="grafico_modelo")

    # divisor !!!
    st.markdown(
        """
        <hr style="
            height:4px;
            border:none;
            background: linear-gradient(to right, #59a1ff, #0c50a8);
        " />
        """,
        unsafe_allow_html=True)

if __name__ == "__main__":
    app_streamlit()