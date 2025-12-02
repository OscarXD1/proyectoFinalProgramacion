import pandas as pd

ruta="farmaciasEstadoCompleto.csv"
dfOriginal=pd.read_csv(ruta)
dfLimpio= dfOriginal.copy()


#checar la estructura que tienen los datos
def estructura(dfLimpio:pd.DataFrame):
    print(dfLimpio.head())
    print(dfLimpio.shape)
    print(dfLimpio.info())
    print(dfLimpio.columns)
    print(dfLimpio.dtypes)
    print(dfLimpio.index)


#checar nulos
def revisarNulos(dfLimpio: pd.DataFrame):
    print(dfLimpio.isnull().sum())
#porcentaje de nulos de cada columna
    print(dfLimpio.isnull().sum() / len(dfLimpio))

""""
despues d esto de los nulos voy a borrar
telefono,correo,corredor industrial,nom corredor industrial,numero local,num exterior, num interior,  duda razon social,
"""

#los duplicados
def verDuplicados(dfLimpio: pd.DataFrame):
    print(dfLimpio.duplicated())
    print(dfLimpio[dfLimpio.duplicated(keep=False)]) #en la salida dio que no tiene duplis
    print(dfLimpio.drop_duplicates().shape[0]) #aqui solo confirme

#revisar duplis por columnas q pueden estar relacionadas
    print(dfLimpio[dfLimpio.duplicated(subset=["Nombre","Colonia"],keep=False)])
    print(dfLimpio[dfLimpio.duplicated(subset=["Latitud", "Longitud"], keep=False)])
    print(dfLimpio[dfLimpio.duplicated(subset=["Nombre", "Colonia", "Latitud", "Longitud"], keep=False)]) #814 duplicados
    print(dfLimpio[dfLimpio.duplicated(subset=["Nombre", "Colonia", "Latitud", "Longitud"], keep=False)].groupby(["Nombre", "Colonia", "Latitud", "Longitud"]).size()) #cuantas veces se repite cada combi
#las xonbinaciones que salen igual en nombre, colonia, latitud y longitud aparecen dos veces

#AQUI BORRARE LOS DUPLIS
def eliminarDuplicados(dfLimpio:pd.DataFrame):
    dfLimpio = dfLimpio.drop_duplicates(subset=["Nombre", "Colonia", "Latitud", "Longitud"])
    print(dfLimpio.duplicated(subset=["Nombre", "Colonia", "Latitud", "Longitud"]).sum())
    print(dfLimpio.shape[0])
    return dfLimpio

#BORRAR COLUMNAS
#estas columnas se borraran por que tienen mas de un 60% de datos
def eliminarColumnas(dfLimpio: pd.DataFrame):
    dfLimpio=dfLimpio.drop(columns=["Num_Interior","Telefono","Sitio_internet","tipo_corredor_industrial", "nom_corredor_industrial","numero_local",
                                "Num_Exterior", "Correo_e","Razon_social","CP"])
    return dfLimpio


#AQUI HARE QUE LAS COLUMNAS DE TEXTO SEAN EN MAYUSCULA Y SIN ACENTO
def mayusculasAcentos(dfLimpio: pd.DataFrame):
    columnasTexto=["Nombre","Colonia","Calle","Ubicacion", "Clase_actividad","Tipo_vialidad","Tipo"]

    reemplazarAcentos={
        "Á": "A","É": "E", "Í": "I","Ó": "O", "Ú": "U",
        "À": "A", "È": "E", "Ì": "I", "Ò": "O","Ù": "U"
    }

    for col in columnasTexto:
        dfLimpio[col]=dfLimpio[col].astype(str).str.strip().str.upper()

        for acento, normal in reemplazarAcentos.items():
            dfLimpio[col]=dfLimpio[col].str.replace(acento,normal)
    return dfLimpio

#aqui solo le pondre sin calle a lo que dice ninguno pq no se las calles pero como se tienen las coordenadas sigue sirviendo
def reemplazoCalle(dfLimpio: pd.DataFrame):
    dfLimpio["Calle"]= dfLimpio["Calle"].astype(str).str.strip().str.upper()
    dfLimpio["Calle"]= dfLimpio["Calle"].replace("NINGUNO", "SIN CALLE")
    return dfLimpio

#aqui de la columna de ubicacion lo que se hara es extraer y dejar unicamente el municipio
def limpiarUbicacion(dfLimpio: pd.DataFrame):
    municipios = [
        "MEXICALI","PLAYAS DE ROSARITO","ENSENADA",
        "TIJUANA", "TECATE", "SAN FELIPE","SAN QUINTIN"
    ]

    def extraerMuni(texto):
        texto = str(texto).upper().strip()
        for municipio in municipios:
            if municipio in texto:
                return municipio
        return "SIN MUNICIPIO"

    dfLimpio["Ubicacion"] =dfLimpio["Ubicacion"].apply(extraerMuni)
    return dfLimpio

#En la columna colonia se va hacer estandar y quitare lo que diga zona o colonia y
def limpiarColonia(dfLimpio: pd.DataFrame):
    dfLimpio["Colonia"]=dfLimpio["Colonia"].str.replace("ZONA", "")
    dfLimpio["Colonia"]= dfLimpio["Colonia"].str.replace("COLONIA", "")
    dfLimpio["Colonia"]=dfLimpio["Colonia"].str.strip()

    dfLimpio["Colonia"] =dfLimpio["Colonia"].replace({
        "ZONZ RIO": "ZONA RIO",
        "ZONA CENTRO":"CENTRO",
        "CENTRO ZONA":"CENTRO",
        "CENTRO":"CENTRO"
    })
    return dfLimpio

#AQUI SE LIMPIA LA COLUMNA  =NOMBRE=
#Aqui limpiare la columna de nombre que es la mas complicada ya que tiene muchas inconsistencias
def filtrarFarmaciasConsul(dfLimpio: pd.DataFrame):
    incluir =["FARMACIA","PHARMACY", "PHARMA", "BOTICA","DROGUERIA","FARMACIAS","DRUG STORE"]

    #palabras que no tomare en cuenta aunque digan farmacia
    excluir=["VETERINARIA", "DERMATOLOGIA", "DENTAL","SUPLEMENTOS","DISTRIBUIDORA","HOSPITALARIA", "SKIN","BODEGA", "ALMACEN"]

    def esFarmacia(texto):
        texto =str(texto).upper()
        if any(palabra in texto for palabra in excluir):
            return False

        if any(palabra in texto for palabra in incluir):
            return True
        return False

    #firltrar para tener solo lo que si es farmacia
    dfLimpio=dfLimpio[dfLimpio["Nombre"].apply(esFarmacia)].copy()

    #creare columna de si tiene consultorio o no
    dfLimpio["Consultorio"] = dfLimpio["Nombre"].str.upper().str.contains("CONSULTORIO").map({True: "SI", False: "NO"})

    return dfLimpio


#aqui voy a meter una reconstruccion de la columna d econsultorio porque al basarme en nombre se perdian datos
#la reconstruire en base a la columna clase acrividad para que sea confiable la info para el analisis

def rehacerConsultorio(dfLimpio: pd.DataFrame):
    dfLimpio["Consultorio"]=dfLimpio["Clase_actividad"].str.upper().str.contains("CONSULTORIOS")
    dfLimpio["Consultorio"]=dfLimpio["Consultorio"].map({True: "SI", False:"NO"})
    return dfLimpio


#hare que todas las palabras que anteriormente inclui ya no varien y que todas sean farmacia
def estandarFarmacias(dfLimpio: pd.DataFrame):
    renombre = {
        "PHARMACY":"FARMACIA",
        "PHARMA":"FARMACIA",
        "BOTICA":"FARMACIA",
        "DROGUERIA": "FARMACIA",
        "FARMACIAS": "FARMACIA",
        "DRUG STORE":"FARMACIA" }

    for viejo, nuevo in renombre.items():
        dfLimpio["Nombre"] = dfLimpio["Nombre"].str.replace(viejo, nuevo)


    dfLimpio["Nombre"] = dfLimpio["Nombre"].str.replace("  ", " ").str.strip()
    return dfLimpio


#Aqui hare unos arreglitos con los espacios en la columnad nombre aun
def espacios(dfLimpio: pd.DataFrame):
    dfLimpio["Nombre"] = dfLimpio["Nombre"].str.replace("4LESS", "4 LESS")

    dfLimpio["Nombre"] = dfLimpio["Nombre"].str.replace("G I", "GI")

    dfLimpio["Nombre"] = dfLimpio["Nombre"].str.replace("  ", " ").str.strip() #aqui vuelvo a checar los espacios aunqe en gernal ya lo habia hecho

    return dfLimpio

#aqui quitare las palabas suc o sucursal en generla
def quitarSucursal(dfLimpio: pd.DataFrame):
    dfLimpio["Nombre"] = dfLimpio["Nombre"].str.upper()
    dfLimpio["Nombre"] = dfLimpio["Nombre"].str.split("SUCURSAL").str[0].str.strip()
    dfLimpio["Nombre"] = dfLimpio["Nombre"].str.split("SUC ").str[0].str.strip()
    return dfLimpio


def recortarNombreFarmacias(dfLimpio: pd.DataFrame):
    #hago una lista de nombre que quiero que se queden asi, sin nada mas o menos ya quue quiero quitar cosas como ubicacines que solo son repetidas
    # elegi estas porque como son cadenas grndes de farmacias hacen que haya mucha inconsistencia en la columna de nombre y tienen variaciones
    nombreNormal = [
        "FARMACIA DEL AHORRO",
        "FARMACIA SIMILARES",
        "FARMACIA DE SIMILARES",
        "FARMACIA LA MAS BARATA",
        "FARMACIA ROMA",
        "FARMACIA BENAVIDES",
        "FARMACIA YZA",
        "FARMACIA GUADALAJARA",
        "FARMACIA INTEGRA"]
    def limpiar(texto):
        texto = str(texto).upper().strip()
        for nombre in nombreNormal:
            if nombre in texto:
                return nombre
        return texto

    dfLimpio["Nombre"] = dfLimpio["Nombre"].apply(limpiar)
    return dfLimpio

#hubo una confusion con el nombre de las farmacias similares asi que corregire este error de escritura para que las graficas sean confiables
#Usare un diccionario para coregir los nombres porque si usaba el replace uno por uno se hacia un desastre com los nombres.
#porque reemplazaba las incidencias y se terminaba cambiando el nombre a cosas como similareses, con el diccionario es mas esfectivo
def corregirSimilares(dfLimpio: pd.DataFrame):
    dfLimpio["Nombre"] = dfLimpio["Nombre"].replace({
        "FARMACIA DE SIMILARES": "FARMACIA SIMILARES",
        "FARMACIA SIMILAR": "FARMACIA SIMILARES",
        "FARMACIA SIMILARS":"FARMACIA SIMILARES",
        "FARMACIA SIMILIARES":"FARMACIA SIMILARES",
        "FARMACIA DE GENERICOS CVS SIMILARES": "FARMACIA SIMILARES"
    })
    return dfLimpio

#checo datos por ultima vez para ver que tal estan
def revision(dfLimpio: pd.DataFrame):
    print(dfLimpio.columns)
    print(dfLimpio.isnull().sum())
    print(dfLimpio.isnull().sum()/len(dfLimpio))

#Voy a crear una columna para poder clasificar el tama;o de las farmacias segun los trabajadores que tenga, para esto voy a guiarme con la columna de estrato
def clasificacionTamaño(dfLimpio: pd.DataFrame): #me marcaba error si usaba la ñ
    clasificacion = {
        "0 a 5 personas": "MICRO",
        "6 a 10 personas": "PEQUEÑA",
        "11 a 30 personas": "MEDIANA",
        "31 a 50 personas": "MEDIANA GRANDE",
        "101 a 250 personas": "GRANDE",
        "251 y más personas": "CORPORATIVA",
    }

    dfLimpio["Clasificacion_tamaño"] = dfLimpio["Estrato"].map(clasificacion).fillna("Sin clasificar")

    return dfLimpio

#aqui voy a hacer otra columna para clasificar si las farmacias son cadenas o si son independientes me ayudare de la columna de nombre con las farmacias que
#yo por propio conocimiento se que son cadenas y de las que no se si lo son hare un conteo para la columna nombre
def clasificarModelo(dfLimpio: pd.DataFrame):
    #esta es la lista de las farmacias que yo ya se que son cadenas
    farmacias = [
        "FARMACIA GUADALAJARA",
        "FARMACIA SIMILARES",
        "FARMACIA DEL AHORRO",
        "FARMACIA BENAVIDES",
        "FARMACIA YZA",
        "FARMACIA ROMA",
        "FARMACIA INTEGRA",
        "FARMACIA LA MAS BARATA"
    ]
    conteo = dfLimpio["Nombre"].value_counts()
    cadenasEncontradas = set(conteo[conteo > 5].index)

    #aqui unire las dos listas de cadenas anteriores
    totalCadenas= set(farmacias).union(cadenasEncontradas)

#aqui esta funcion es para asignar la clasificacion
    def modelo(nombre):
        if nombre in totalCadenas:
            return "CADENA"
        else:
            return "INDEPENDIENTE"

#aplico la función
    dfLimpio["Modelo_farmacia"] = dfLimpio["Nombre"].apply(modelo)

    return dfLimpio

if __name__=="__main__":
    estructura(dfLimpio)
    print("=====================================================")
    revisarNulos(dfLimpio)
    print("=====================================================")
    verDuplicados(dfLimpio)
    print("=====================================================")
    dfLimpio=eliminarDuplicados(dfLimpio)
    print("=====================================================")
    dfLimpio=eliminarColumnas(dfLimpio)
    print("=====================================================")
    dfLimpio=mayusculasAcentos(dfLimpio)
    print("=====================================================")
    dfLimpio=reemplazoCalle(dfLimpio)
    print("=====================================================")
    dfLimpio= limpiarUbicacion(dfLimpio)
    print("=====================================================")
    dfLimpio=limpiarColonia(dfLimpio)
    print("=====================================================")
    dfLimpio=filtrarFarmaciasConsul(dfLimpio)
    print("=====================================================")
    dfLimpio=rehacerConsultorio(dfLimpio)
    print("=====================================================")
    dfLimpio=estandarFarmacias(dfLimpio)
    print("=====================================================")
    dfLimpio=espacios(dfLimpio)
    print("=====================================================")
    dfLimpio=quitarSucursal(dfLimpio)
    print("=====================================================")
    dfLimpio=recortarNombreFarmacias(dfLimpio)
    print("=====================================================")
    dfLimpio=corregirSimilares(dfLimpio)
    print("======================================================")
    revision(dfLimpio)
    print("======================================================")
    clasificacionTamaño(dfLimpio)
    print("=======================================================")
    clasificarModelo(dfLimpio)

    #rviso cambios q no he guardado
    print(dfLimpio[[ "Ubicacion", "Clase_actividad"]].head(20))
    print(dfLimpio[["Calle"]].head(20))
    print(dfLimpio[["Ubicacion"]].head(20))
    print(dfLimpio[["Colonia"]].head(20))
    print(dfLimpio[["Nombre"]].head(40))
    print(dfLimpio[["Consultorio"]].head(40))
    print(dfLimpio[["Nombre"]].head(60))

    dfLimpio.to_csv("farmaciasCompletoLimpio.csv", index=False)

