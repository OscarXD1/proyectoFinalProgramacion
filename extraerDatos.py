import requests
import pandas as pd


def extraerDatos(inicio, fin, nombreArchivo):
    """
    Extrae datos de la API de INEGI en un rango específico
    """
    # Token para usar la api de inegi
    token = "b97caaa8-e3c2-40f3-afd6-e5b300217c60"
    # Codigo que representa las farmacias
    codigo = "466330"
    palabra = "farmacias"
    # localidad
    estado = "02"

    url = f"https://www.inegi.org.mx/app/api/denue/v1/consulta/BuscarEntidad/{palabra}/{estado}/{inicio}/{fin}/{token}"

    # Convertir a json lo que extraemos
    response = requests.get(url)
    data = response.json()

    # df de farmacias del estado
    df = pd.DataFrame(data)
    df.to_csv(nombreArchivo, index=False)
    return df


def unirDataFrames():
    #Une los archivos CSV
    #Lee los CSV
    df1 = pd.read_csv("farmaciasEstado.csv")
    df2 = pd.read_csv("farmaciasEstado2.csv")

    # Concatenar los dataframes
    dfCompleto = pd.concat([df1, df2], ignore_index=True)
    dfCompleto.to_csv("farmaciasEstadoCompleto.csv", index=False)


if __name__ == "__main__":
    # Extrae solo los primeros 1500 registros. (La documentación del Api recomiendo no extraer mas de esa cantidad)
    extraerDatos(inicio=1, fin=1500, nombreArchivo="farmaciasEstado.csv")

    # Extraer siguientes 500 registros
    extraerDatos(inicio=1501, fin=2000, nombreArchivo="farmaciasEstado2.csv")

    # PASO 3: Unir ambos DataFrames
    unirDataFrames()
    print("LISTOOOOO")