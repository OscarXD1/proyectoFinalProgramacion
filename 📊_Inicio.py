import streamlit as st

def app_principal():
    st.set_page_config(page_title="Proyecto final",
                       page_icon="🏥")

    #Logo de la barra lateral
    LOGO_URL = "https://images.vexels.com/media/users/3/136559/isolated/preview/624dd0a951a1e8a118215b1b24a0da59-logotipo-de-farmacia.png"

    st.logo(
        LOGO_URL,
        icon_image=LOGO_URL,
        size="large"
    )

    #Logo de uabc
    st.image("https://fca.tij.uabc.mx/web/image/website/1/logo/FCA%20Tijuana?unique=b8c791b", width=250)
    #Titulo de la pagina
    st.markdown(
        """
        <h1 style='text-align:center; color:#0a2a43; font-size:45px;'>
            Farmacias y acceso a la salud en Baja California 💊
        </h1>
        """,
        unsafe_allow_html=True
    )

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

    st.subheader("Bienvenidos, en esta app podrán encontrar dashboards interactivos sobre el acceso a medicamentos en el estado de baja california. Pueden poner música dando click a la barra inferior para relajarse mientras observan los datos 😺")

    #Musiquia para relajarse mientras lo ven
    st.audio("MusicaLofi.mp3", format="audio/mpeg", loop=True)

    st.subheader("Veremos dashboards sobre: ")

    st.markdown(
        ":violet-badge[📍 Baja California] :orange-badge[📍 Tijuana] :red-badge[📍 Rosarito]"
    )

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


    #Bloque de texto para el contexto del proyecto
    st.markdown(
        """
        <div style="
            background-color:#f7f9fc;
            padding:20px;
            border-radius:15px;
            border-left:5px solid #0a2a43;
            font-size:18px;
            line-height:1.6;
        ">
            <b>Contexto del proyecto:</b><br><br>
            Este proyecto busca que a través de la aplicación de las habilidades técnicas 
            desarrolladas a lo largo del semestre, como lo son los procesos de la extracción, 
            transformación, manipulación y visualización de datos, se puedan identificar 
            patrones y comportamientos del sector salud en distintos municipios de Baja California. 
            Este proyecto aporta evidencia sobre la distribución de farmacias y farmacias con 
            consultorio por colonias, por los municipios seleccionados Tijuana y Rosarito, 
            así como distribución en Baja California en general, se analizan las farmacias 
            predominantes, el tamaño, entre otras cosas. Esto es útil para docentes, instituciones 
            de salud y de gobierno del estado de Baja California.
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == '__main__':
    app_principal()