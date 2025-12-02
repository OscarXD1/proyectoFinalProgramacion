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
def farmaciasconsultorio(farmaciasCompletoLimpio):
    farmaciasCconsultorio =  (farmaciasCompletoLimpio.groupby("Ubicacion")["Consultorio"].count()
                              .reset_index(name= "Numero_farmacias")
                              .sort_values("Numero_farmacias", ascending=False))

    return farmaciasCconsultorio

#porcentaje de farmacias con consultorio
def consultorioporcentaje(df_farmaciasCconsultorio):
    total = df_farmaciasCconsultorio["Numero_farmacias"].sum()
    df_farmaciasCconsultorio["Porcentaje"] = (df_farmaciasCconsultorio["Numero_farmacias"] / total) * 100

    return df_farmaciasCconsultorio


#Qué porcentaje representa del total de farmacias representa cada municipio


#En qué vialidad se encuentran más farmacias en el estado
def vialidadfarmacias(farmaciasCompletoLimpio):
    farmaciasXvialidad = (farmaciasCompletoLimpio.groupby("Tipo_vialidad")["Id"].count()
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
def farmaciasservicio(farmaciasCompletoLimpio):
    farmaciasXservicio = (farmaciasCompletoLimpio.groupby("Clase_actividad")["Id"].count()
                            .reset_index(name="Numero_farmacias")
                            .sort_values("Numero_farmacias", ascending=False))
    return farmaciasXservicio


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
    print("farmacias por vialidad", vialidadfarmacias(farmaciasCompletoLimpio))
    print("===============================================")
    print("farmacias por tamaño", tamanofarmacia(farmaciasCompletoLimpio))
    print("===============================================")
    print("top 10 cadenas dominantes", cadenaspredominantes(farmaciasCompletoLimpio).head(10))
    print("===============================================")
    print("farmacias por servicio", farmaciasservicio(farmaciasCompletoLimpio))
    print("===============================================")
    print("farmacias por tipo", independienteocadena(farmaciasCompletoLimpio))