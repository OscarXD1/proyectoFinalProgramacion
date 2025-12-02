import pandas as pd

#aqui estoy leyendo el df ya limpio para poder hacer las agrpaciones con el df ya final
farmaciasCompletoLimpio=pd.read_csv("farmaciasCompletoLimpio.csv")

#¿Cuántas farmacias hay por municipio?
#aquí voy a agrupar por los municipios y contar las farmacias
def farmaciasMunicipio(farmaciasCompletoLimpio):
    farmaciasXmunicipio=(farmaciasCompletoLimpio.groupby("Ubicacion")["Id"].count()
                     .reset_index(name="Numero_farmacias")
                     .sort_values("Numero_farmacias", ascending=False))
    return farmaciasXmunicipio



#¿Cuántas farmacias cuentan con consultorio por municipio?
def farmaciasconsultorio(farmaciasCompletoLimpio):    # Filtramos solo farmacias que tengan consultorio
    #filtramos las q tienen consultorio
    con_consultorio = farmaciasCompletoLimpio[farmaciasCompletoLimpio["Consultorio"].str.upper().str.strip() == "SI"]  # o True, según tus datos

    farmaciasCconsultorio = (con_consultorio.groupby("Ubicacion")["Consultorio"].count()
                    .reset_index(name="Numero_farmacias")
                    .sort_values("Numero_farmacias", ascending=False))

    return farmaciasCconsultorio

#porcentaje de farmacias con consultorio
def consultorioporcentaje(df_farmaciasCconsultorio):
    total = df_farmaciasCconsultorio["Numero_farmacias"].sum()
    df_farmaciasCconsultorio["Porcentaje"] = (df_farmaciasCconsultorio["Numero_farmacias"] / total) * 100

    return df_farmaciasCconsultorio


#Qué porcentaje representa cada municipio en el total de farmacias
# ejemplo: tijuana 50%, rosarito 20%, etc es un pastelito
def porcentajefarmacias(farmaciasCompletoLimpio):
    porcentajeXmunicipio = (farmaciasCompletoLimpio.groupby("Ubicacion")["Id"].count()
                    .reset_index(name="Numero_farmacias")
                    .sort_values("Numero_farmacias", ascending=False))
    total_farmacias = porcentajeXmunicipio["Numero_farmacias"].sum()
    porcentajeXmunicipio["Porcentaje"] = (porcentajeXmunicipio["Numero_farmacias"] / total_farmacias * 100)

    return porcentajeXmunicipio


#En qué vialidad se encuentran más farmacias en el estado
def vialidadfarmacias(farmaciasCompletoLimpio):
    farmaciasXvialidad = (farmaciasCompletoLimpio.groupby(["Ubicacion", "Tipo_vialidad"])["Id"].count()
                             .reset_index(name="Numero_farmacias")
                             .sort_values("Numero_farmacias", ascending=False))

    return farmaciasXvialidad


#Qué tamaño de farmacia predomina en la región
def tamanofarmacia(farmaciasCompletoLimpio):
    farmaciasXtamano = (farmaciasCompletoLimpio.groupby("Clasificacion_tamaño")["Id"].count()
                            .reset_index(name="Numero_farmacias")
                            .sort_values("Numero_farmacias", ascending=False))
    return farmaciasXtamano



#Cuáles son las cadenas de farmacias predominantes en el estado
def cadenaspredominantes(farmaciasCompletoLimpio):
    cadenasfarmacias = (farmaciasCompletoLimpio.groupby("Nombre")["Id"].count()
                            .reset_index(name="Numero_farmacias")
                            .sort_values("Numero_farmacias", ascending=False))
    return cadenasfarmacias


#Farmacias por servicio otorgado
def farmaciasservicio(farmaciasCompletoLimpio,  top_n=15):
    farmaciasXservicio = (farmaciasCompletoLimpio.groupby("Clase_actividad")["Id"]
          .count()
          .reset_index(name="Numero_farmacias")
          .sort_values("Numero_farmacias", ascending=False))

    # Top N
    top = farmaciasXservicio.head(top_n)

    # Sumar el resto como "Otros"
    otros_total = farmaciasXservicio["Numero_farmacias"][top_n:].sum()

    if otros_total > 0:
        top.loc[len(top)] = ["Otros", otros_total]

    return top


#Número de farmacias de cadena e independientes
def independienteocadena(farmaciasCompletoLimpio):
    tipodemodelo = (farmaciasCompletoLimpio.groupby("Modelo_farmacia")["Nombre"].count()
                            .reset_index(name="Numero_farmacias")
                            .sort_values("Numero_farmacias", ascending=False))
    return tipodemodelo


if __name__=="__main__":
    print("farmacias por municipio", farmaciasMunicipio(farmaciasCompletoLimpio))
    print("==============================================")
    print("farmacias con consultorio", farmaciasconsultorio(farmaciasCompletoLimpio))
    print("===============================================")
    df_farmaciasCconsultorio = farmaciasconsultorio(farmaciasCompletoLimpio)
    df_porcentaje = consultorioporcentaje(df_farmaciasCconsultorio)
    print("porcentaje de farmacias con consultorio", df_porcentaje)
    print("===============================================")
    print("porcentaje de farmacias x muni", porcentajefarmacias(farmaciasCompletoLimpio))
    print("===============================================")
    print("farmacias por vialidad", vialidadfarmacias(farmaciasCompletoLimpio))
    print("===============================================")
    print("farmacias por tamaño", tamanofarmacia(farmaciasCompletoLimpio))
    print("===============================================")
    print("top 10 cadenas dominantes", cadenaspredominantes(farmaciasCompletoLimpio).head(10))
    print("===============================================")
    print("farmacias por servicio", farmaciasservicio(farmaciasCompletoLimpio))
    print("===============================================")
    print("farmacias por tipo", independienteocadena(farmaciasCompletoLimpio))