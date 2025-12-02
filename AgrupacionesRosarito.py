import pandas as pd
import plotly.express as px
import streamlit as st
from streamlit import title

farmaciasCompletoLimpio=pd.read_csv("farmaciasCompletoLimpio.csv")


Rosarito = farmaciasCompletoLimpio[farmaciasCompletoLimpio['Ubicacion'] == 'PLAYAS DE ROSARITO']

# 1. CUANTAS FARMACIAS HAY POR COLONIA EN ROSARITO?
#Para ello primero lo agrupamos por colonia y contamos cuantas hay
def agrupacionRosarito(farmaciasCompletoLimpio):
    farmaciasxcoloniaR = Rosarito.groupby('Colonia').size().reset_index(name='Num_Farmacias')
    print(farmaciasxcoloniaR)

    return farmaciasxcoloniaR


# 2. FARMACIAS CON CONSULTORIO (PORCENTAJE)
def consultoriosPorcentaje(farmaciasCompletoLimpio):
    #Contamos cuantas farmacias tienen consultorio y cuantas no
    Rosarito = farmaciasCompletoLimpio[farmaciasCompletoLimpio['Ubicacion'] == 'PLAYAS DE ROSARITO']

    #Los agrupamos por consultorio y contamos cuantos son
    consultorioR = (Rosarito.groupby("Consultorio")["Id"].count()
                    .reset_index(name="Num_Farmacias"))

    totalconR = consultorioR["Num_Farmacias"].sum()
    consultorioR["Porcentaje"] = (consultorioR["Num_Farmacias"] / totalconR * 100).round(2)

    print(consultorioR)
    return consultorioR



# 3. NUMERO DE FARMACIAS CON CONSULTORIO EN ROSARITO (TOTALES)
# Se respónde en el codigo de arriba


# 4. CADENAS DE FARMACIA PREDOMINANTES EN ROSARITO
def cadenasRosarito(farmaciasCompletoLimpio):
    Rosarito = farmaciasCompletoLimpio[farmaciasCompletoLimpio['Ubicacion'] == 'PLAYAS DE ROSARITO']

    CadenasRosarito= (Rosarito.groupby("Nombre")["Id"].count()
            .reset_index(name="Num_Farmacias")
            .sort_values(by="Num_Farmacias", ascending=False))

    cadenasR_filtrado = CadenasRosarito[CadenasRosarito["Num_Farmacias"] > 1]

    print(cadenasR_filtrado)
    return cadenasR_filtrado



# 5. TAMAÑO DE FARMACIA PREDOMINANTE (Clasificacion_tamaño)
def tamaFarmaR(farmaciasCompletoLimpio):
    tamaR = (Rosarito.groupby("Clasificacion_tamaño")["Id"].count()
               .reset_index(name="Num_Farmacias")
               .sort_values(by="Num_Farmacias", ascending=False))

    print(tamaR)
    return tamaR


# 6. FARMACIAS POR SERVICIO OTROGADO
def servicioR(farmaciasCompletoLimpio):
    serviciosR = (Rosarito.groupby("Clase_actividad")["Id"].count()
                  .reset_index(name="Num_Farmacias")
                  .sort_values(by="Num_Farmacias", ascending=False))

    print(serviciosR)
    return serviciosR



# 7. Mapa de puntos
#Está en el archivo de graficas !!


# 8. Número de farmacias de cadena e independientes (Modelo_farmacia)


def modeloFarmaciaRosarito(farmaciasCompletoLimpio):
    ModeloR = (Rosarito.groupby("Modelo_farmacia")["Id"].count()
                  .reset_index(name="Num_Farmacias")
                  .sort_values(by="Num_Farmacias", ascending=False))

    print(ModeloR)
    return ModeloR




# 9. En qué vialidades se encuentran más farmacias dentro del municipio
def tipoVialidadR(farmaciasCompletoLimpio):
    vialidadesR = (Rosarito.groupby("Tipo_vialidad")["Id"].count()
                   .reset_index(name="Num_Farmacias")
                   .sort_values(by="Num_Farmacias", ascending=False))

    print(vialidadesR)
    return vialidadesR



if __name__ == '__main__':
    print("\n1. CUANTAS FARMACIAS HAY POR COLONIA EN ROSARITO?")
    print(" ")
    agrupacionRosarito(farmaciasCompletoLimpio)
    print("\n2⏔⏔⏔ ꒰ ᧔ෆ᧓ ꒱ ⏔⏔⏔⏔⏔⏔ ꒰ ᧔ෆ᧓ ꒱ ⏔⏔⏔⏔⏔⏔ ꒰ ᧔ෆ᧓ ꒱ ⏔⏔⏔")
    print("\n2. FARMACIAS CON CONSULTORIO (PORCENTAJE) y NUMERO DE FARMACIAS CON CONSULTORIO EN ROSARITO (TOTALES)")
    print(" ")
    consultoriosPorcentaje(farmaciasCompletoLimpio)
    print("\n⏔⏔⏔ ꒰ ᧔ෆ᧓ ꒱ ⏔⏔⏔⏔⏔⏔ ꒰ ᧔ෆ᧓ ꒱ ⏔⏔⏔⏔⏔⏔ ꒰ ᧔ෆ᧓ ꒱ ⏔⏔⏔")
    print("\n4. CADENAS DE FARMACIA PREDOMINANTES EN ROSARITO")
    print(" ")
    cadenasRosarito(farmaciasCompletoLimpio)
    print("\n2⏔⏔⏔ ꒰ ᧔ෆ᧓ ꒱ ⏔⏔⏔⏔⏔⏔ ꒰ ᧔ෆ᧓ ꒱ ⏔⏔⏔⏔⏔⏔ ꒰ ᧔ෆ᧓ ꒱ ⏔⏔⏔")
    print(" ")
    tamaFarmaR(farmaciasCompletoLimpio)
    print("\n6. FARMACIAS POR SERVICIO OTROGADO")
    print(" ")
    servicioR(farmaciasCompletoLimpio)
    print("\n⏔⏔⏔ ꒰ ᧔ෆ᧓ ꒱ ⏔⏔⏔⏔⏔⏔ ꒰ ᧔ෆ᧓ ꒱ ⏔⏔⏔⏔⏔⏔ ꒰ ᧔ෆ᧓ ꒱ ⏔⏔⏔")
    print("\n8. Número de farmacias de cadena e independientes (Modelo_farmacia)")
    print(" ")
    modeloFarmaciaRosarito(farmaciasCompletoLimpio)
    print("\n⏔⏔⏔ ꒰ ᧔ෆ᧓ ꒱ ⏔⏔⏔⏔⏔⏔ ꒰ ᧔ෆ᧓ ꒱ ⏔⏔⏔⏔⏔⏔ ꒰ ᧔ෆ᧓ ꒱ ⏔⏔⏔")
    print("\n9. En qué vialidades se encuentran más farmacias dentro del municipio")
    print(" ")
    tipoVialidadR(farmaciasCompletoLimpio)
    print("\n⏔⏔⏔ ꒰ ᧔ෆ᧓ ꒱ ⏔⏔⏔⏔⏔⏔ ꒰ ᧔ෆ᧓ ꒱ ⏔⏔⏔⏔⏔⏔ ꒰ ᧔ෆ᧓ ꒱ ⏔⏔⏔")