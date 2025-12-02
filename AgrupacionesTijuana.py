import pandas as pd
#Aqui cargo el archivo
farmaciasCompletoLimpio = pd.read_csv("farmaciasCompletoLimpio.csv")

# Filtramos SOLO Tijuana
Tijuana = farmaciasCompletoLimpio[farmaciasCompletoLimpio['Ubicacion'] == 'TIJUANA']

# ============================================================
# 1. ¿CUÁNTAS FARMACIAS HAY POR COLONIA EN TIJUANA?
# ============================================================
def AgrupacionTijuana(farmaciasCompletoLimpio):
    farmaciasxcoloniaT = Tijuana.groupby('Colonia').size().reset_index(name='Num_Farmacias')
    print(farmaciasxcoloniaT)
    farmaciasxcoloniaT.to_csv('TijuanaFarmaciasColonia.csv', index=False)
    return farmaciasxcoloniaT

# ============================================================
# 2. FARMACIAS CON CONSULTORIO (PORCENTAJE)
# ============================================================
def ConsultoriosPorcentajeTijuana(farmaciasCompletoLimpio):
    Tijuana = farmaciasCompletoLimpio[farmaciasCompletoLimpio['Ubicacion'] == 'TIJUANA']

    consultorioT = (
        Tijuana.groupby("Consultorio")["Id"].count()
        .reset_index(name="Num_Farmacias")
    )
    totalT = consultorioT["Num_Farmacias"].sum()
    consultorioT["Porcentaje"] = (consultorioT["Num_Farmacias"] / totalT * 100).round(2)
    consultorioT.to_csv('TijuanaFarmaciasConsultorio.csv', index=False)
    print(consultorioT)
    return consultorioT
#el 3 se realiza sacando del 2
# ============================================================
# 4. CADENAS DE FARMACIA PREDOMINANTES EN TIJUANA
# ============================================================
def CadenasTijuana(farmaciasCompletoLimpio):
    Tijuana = farmaciasCompletoLimpio[farmaciasCompletoLimpio['Ubicacion'] == 'TIJUANA']

    CadenasTijuana = (
        Tijuana.groupby("Nombre")["Id"].count()
        .reset_index(name="Num_Farmacias")
        .sort_values(by="Num_Farmacias", ascending=False)
    )
    cadenasT_filtrado = CadenasTijuana[CadenasTijuana["Num_Farmacias"] > 1]
    cadenasT_filtrado.to_csv('TijuanaCadenasProdominantes.csv', index=False)

    print(cadenasT_filtrado)
    return cadenasT_filtrado

# ============================================================
# 5. TAMAÑO DE FARMACIA PREDOMINANTE (Clasificación_tamaño)
# ============================================================
def TamaFarmaT(farmaciasCompletoLimpio):
    tamaT = (
        Tijuana.groupby("Clasificacion_tamaño")["Id"].count()
        .reset_index(name="Num_Farmacias")
        .sort_values(by="Num_Farmacias", ascending=False)
    )
    tamaT.to_csv('TijuanaFarmacias_por_tamaño.csv', index=False)
    print(tamaT)
    return tamaT

# ============================================================
# 6. FARMACIAS POR SERVICIO OTORGADO
# ============================================================
def ServicioT(farmaciasCompletoLimpio):
    serviciosT = (
        Tijuana.groupby("Clase_actividad")["Id"].count()
        .reset_index(name="Num_Farmacias")
        .sort_values(by="Num_Farmacias", ascending=False)
    )

    serviciosT.to_csv('TijuanaServiciosFarmacias.csv', index=False)
    print(serviciosT)
    return serviciosT
#el 7 se realiza con csv original

# ============================================================
# 8. Modelo de farmacia (cadena / independiente)
# ============================================================
def ModeloFarmaciaTijuana(farmaciasCompletoLimpio):
    ModeloT = (
        Tijuana.groupby("Modelo_farmacia")["Id"].count()
        .reset_index(name="Num_Farmacias")
        .sort_values(by="Num_Farmacias", ascending=False)
    )

    ModeloT.to_csv('TijuanaModeloFarmacia.csv', index=False)
    print(ModeloT)
    return ModeloT

# ============================================================
# 9. Vialidades con más farmacias
# ============================================================
def TipoVialidadT(farmaciasCompletoLimpio):
    vialidadesT = (
        Tijuana.groupby("Tipo_vialidad")["Id"].count()
        .reset_index(name="Num_Farmacias")
        .sort_values(by="Num_Farmacias", ascending=False)
    )

    vialidadesT.to_csv('TijuanaVialidades.csv', index=False)
    print(vialidadesT)
    return vialidadesT

if __name__ == '__main__':
    print("1. CUÁNTAS FARMACIAS HAY POR COLONIA EN TIJUANA?")
    AgrupacionTijuana(farmaciasCompletoLimpio)
    print("2. FARMACIAS CON CONSULTORIO (PORCENTAJE)")
    ConsultoriosPorcentajeTijuana(farmaciasCompletoLimpio)
    #el 3 se realiza sacando del 2
    print("4. CADENAS DE FARMACIA PREDOMINANTES EN TIJUANA")
    CadenasTijuana(farmaciasCompletoLimpio)
    print("5. TAMAÑO DE FARMACIAS EN TIJUANA")
    TamaFarmaT(farmaciasCompletoLimpio)
    print("6. FARMACIAS POR SERVICIO OTORGADO")
    ServicioT(farmaciasCompletoLimpio)
    #el 7 se realiza con el csv original
    print("8. MODELO DE FARMACIA (CADENA / INDEPENDIENTE)")
    ModeloFarmaciaTijuana(farmaciasCompletoLimpio)
    print("9. VIALIDADES CON MÁS FARMACIAS")
    TipoVialidadT(farmaciasCompletoLimpio)
