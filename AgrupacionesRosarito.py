import pandas as pd
import plotly.express as px
import streamlit as st
from streamlit import title

farmaciasCompletoLimpio=pd.read_csv("farmaciasCompletoLimpio.csv")


Rosarito = farmaciasCompletoLimpio[farmaciasCompletoLimpio['Ubicacion'] == 'PLAYAS DE ROSARITO']

# 1. CUANTAS FARMACIAS HAY POR COLONIA EN ROSARITO?
#Para ello primero lo agrupamos por colonia y contamos cuantas hay
def AgrupacionRosarito(farmaciasCompletoLimpio):
    farmaciasxcoloniaR = Rosarito.groupby('Colonia').size().reset_index(name='Num_Farmacias')
    print(farmaciasxcoloniaR)


    farmaciasxcoloniaR.to_csv('FarmaciasRosaritoColonia.csv', index=False)

    return farmaciasxcoloniaR


# 2. FARMACIAS CON CONSULTORIO (PORCENTAJE)
def ConsultoriosPorcentaje(farmaciasCompletoLimpio):
    #Contamos cuantas farmacias tienen consultorio y cuantas no
    Rosarito = farmaciasCompletoLimpio[farmaciasCompletoLimpio['Ubicacion'] == 'PLAYAS DE ROSARITO']

    #Los agrupamos por consultorio y contamos cuantos son
    consultorioR = (Rosarito.groupby("Consultorio")["Id"].count()
                    .reset_index(name="Num_Farmacias"))

    totalconR = consultorioR["Num_Farmacias"].sum()
    consultorioR["Porcentaje"] = (consultorioR["Num_Farmacias"] / totalconR * 100).round(2)

    consultorioR.to_csv('FarmaciasConsultorioRosarito.csv', index=False)

    print(consultorioR)

    return consultorioR



# 3. NUMERO DE FARMACIAS CON CONSULTORIO EN ROSARITO (TOTALES)
# Se respónde en el codigo de arriba


# 4. CADENAS DE FARMACIA PREDOMINANTES EN ROSARITO
def CadenasRosarito(farmaciasCompletoLimpio):
    Rosarito = farmaciasCompletoLimpio[farmaciasCompletoLimpio['Ubicacion'] == 'PLAYAS DE ROSARITO']

    CadenasRosarito= (Rosarito.groupby("Nombre")["Id"].count()
            .reset_index(name="Num_Farmacias")
            .sort_values(by="Num_Farmacias", ascending=False))

    cadenasR_filtrado = CadenasRosarito[CadenasRosarito["Num_Farmacias"] > 1]
    cadenasR_filtrado.to_csv('CadenasProdominantesRosarito.csv', index=False)


    print(cadenasR_filtrado)


# 5. TAMAÑO DE FARMACIA PREDOMINANTE (Clasificacion_tamaño)
def TamaFarmaR(farmaciasCompletoLimpio):
    tamaR = (Rosarito.groupby("Clasificacion_tamaño")["Id"].count()
               .reset_index(name="Num_Farmacias")
               .sort_values(by="Num_Farmacias", ascending=False))

    tamaR.to_csv('farmacias_por_tamaño_rosarito.csv', index=False)

    print(tamaR)


# 6. FARMACIAS POR SERVICIO OTROGADO
def ServicioR(farmaciasCompletoLimpio):
    serviciosR = (Rosarito.groupby("Clase_actividad")["Id"].count()
                  .reset_index(name="Num_Farmacias")
                  .sort_values(by="Num_Farmacias", ascending=False))

    serviciosR.to_csv('ServiciosFarmaciasRosarito.csv', index=False)


    print(serviciosR)



# 7. Mapa de puntos


# 8. Número de farmacias de cadena e independientes (Modelo_farmacia)


def ModeloFarmaciaRosarito(farmaciasCompletoLimpio):
    ModeloR = (Rosarito.groupby("Modelo_farmacia")["Id"].count()
                  .reset_index(name="Num_Farmacias")
                  .sort_values(by="Num_Farmacias", ascending=False))

    ModeloR.to_csv('ModeloFarmaciaRosarito.csv', index=False)


    print(ModeloR)




# 9. En qué vialidades se encuentran más farmacias dentro del municipio
def TipoVialidadR(farmaciasCompletoLimpio):
    vialidadesR = (Rosarito.groupby("Tipo_vialidad")["Id"].count()
                   .reset_index(name="Num_Farmacias")
                   .sort_values(by="Num_Farmacias", ascending=False))

    vialidadesR.to_csv('VialidadesRosarito.csv', index=False)


    print(vialidadesR)



if __name__ == '__main__':
    print("\n1. CUANTAS FARMACIAS HAY POR COLONIA EN ROSARITO?")
    print(" ")
    AgrupacionRosarito(farmaciasCompletoLimpio)
    print("\n2⏔⏔⏔ ꒰ ᧔ෆ᧓ ꒱ ⏔⏔⏔⏔⏔⏔ ꒰ ᧔ෆ᧓ ꒱ ⏔⏔⏔⏔⏔⏔ ꒰ ᧔ෆ᧓ ꒱ ⏔⏔⏔")
    print("\n2. FARMACIAS CON CONSULTORIO (PORCENTAJE) y NUMERO DE FARMACIAS CON CONSULTORIO EN ROSARITO (TOTALES)")
    print(" ")
    ConsultoriosPorcentaje(farmaciasCompletoLimpio)
    print("\n⏔⏔⏔ ꒰ ᧔ෆ᧓ ꒱ ⏔⏔⏔⏔⏔⏔ ꒰ ᧔ෆ᧓ ꒱ ⏔⏔⏔⏔⏔⏔ ꒰ ᧔ෆ᧓ ꒱ ⏔⏔⏔")
    print("\n4. CADENAS DE FARMACIA PREDOMINANTES EN ROSARITO")
    print(" ")
    CadenasRosarito(farmaciasCompletoLimpio)
    print("\n2⏔⏔⏔ ꒰ ᧔ෆ᧓ ꒱ ⏔⏔⏔⏔⏔⏔ ꒰ ᧔ෆ᧓ ꒱ ⏔⏔⏔⏔⏔⏔ ꒰ ᧔ෆ᧓ ꒱ ⏔⏔⏔")
    print(" ")
    TamaFarmaR(farmaciasCompletoLimpio)
    print("\n6. FARMACIAS POR SERVICIO OTROGADO")
    print(" ")
    ServicioR(farmaciasCompletoLimpio)
    print("\n⏔⏔⏔ ꒰ ᧔ෆ᧓ ꒱ ⏔⏔⏔⏔⏔⏔ ꒰ ᧔ෆ᧓ ꒱ ⏔⏔⏔⏔⏔⏔ ꒰ ᧔ෆ᧓ ꒱ ⏔⏔⏔")
    print("\n8. Número de farmacias de cadena e independientes (Modelo_farmacia)")
    print(" ")
    ModeloFarmaciaRosarito(farmaciasCompletoLimpio)
    print("\n⏔⏔⏔ ꒰ ᧔ෆ᧓ ꒱ ⏔⏔⏔⏔⏔⏔ ꒰ ᧔ෆ᧓ ꒱ ⏔⏔⏔⏔⏔⏔ ꒰ ᧔ෆ᧓ ꒱ ⏔⏔⏔")
    print("\n9. En qué vialidades se encuentran más farmacias dentro del municipio")
    print(" ")
    TipoVialidadR(farmaciasCompletoLimpio)
    print("\n⏔⏔⏔ ꒰ ᧔ෆ᧓ ꒱ ⏔⏔⏔⏔⏔⏔ ꒰ ᧔ෆ᧓ ꒱ ⏔⏔⏔⏔⏔⏔ ꒰ ᧔ෆ᧓ ꒱ ⏔⏔⏔")