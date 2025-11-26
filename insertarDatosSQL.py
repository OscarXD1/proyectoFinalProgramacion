import pandas as pd
import mysql.connector


#  CONEXIÓN A LA BASE DE DATOS
def conectar():
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="1234",
        database="proyectoBD"
    )
    cursor = conexion.cursor()
    return cursor, conexion


#  LEER ARCHIVO CSV
def leerCSV():
    df = pd.read_csv('farmaciasCompletoLimpio.csv')
    return df

#  OBTENER O INSERTAR VALOR EN TABLAS
def obtenerOInsertar(cursor, conexion, tabla, columna, valor):

    # MAPEO DE LAS PRIMARY KEY
    id_map = {
        "municipio": "idMunicipio",
        "colonia": "idColonia",
        "tipo_vialidad": "idTipoVialidad",
        "tipo_farmacia": "idTipoFarmacia",
        "cantidad_trabajadores": "idCantidadTrabajadores",
        "clase_actividad": "idClaseActividad",
        "farmacia": "idFarmacia"
    }

    id_col = id_map[tabla]

    if pd.isna(valor):
        return None

    #BUSCAR EL REGISTRO
    sqlSelect = f"SELECT {id_col} FROM {tabla} WHERE {columna} = %s"
    cursor.execute(sqlSelect, (valor,))
    resultado = cursor.fetchone()

    if resultado:
        return resultado[0]

    # SI NO EXISTE LO INSERTA
    sqlInsert = f"INSERT INTO {tabla} ({columna}) VALUES (%s)"
    cursor.execute(sqlInsert, (valor,))
    conexion.commit()

    return cursor.lastrowid


#  PROCESO PRINCIPAL
def main():
    cursor, conexion = conectar()
    df = leerCSV()

    for _, fila in df.iterrows():
        #  TABLAS DE DIRECCIÓN (llaves foraneas)

        idMunicipio = obtenerOInsertar(cursor, conexion, "municipio", "nombre", fila["Ubicacion"])
        idColonia = obtenerOInsertar(cursor, conexion, "colonia", "nombre", fila["Colonia"])
        idTipoVialidad = obtenerOInsertar(cursor, conexion, "tipo_vialidad", "descripcion", fila["Tipo_vialidad"])

        # Insertar Dirección
        sqlInsertDireccion = """
            INSERT INTO direccion (idMunicipio, idTipoVialidad, idColonia, Calle)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(sqlInsertDireccion, (
            idMunicipio,
            idTipoVialidad,
            idColonia,
            fila["Calle"]
        ))
        conexion.commit()
        idDireccion = cursor.lastrowid



        #  TABLAS DE SUCURSAL (llaves foraneas)
        idTipoFarmacia = obtenerOInsertar(cursor, conexion, "tipo_farmacia", "descripcion", fila["Tipo"])
        idCantidadTrab = obtenerOInsertar(cursor, conexion, "cantidad_trabajadores", "descripcion", fila["Estrato"])
        idClaseActividad = obtenerOInsertar(cursor, conexion, "clase_actividad", "descripcion", fila["Clase_actividad"])

        # Nombre de la farmacia
        idFarmacia = obtenerOInsertar(cursor, conexion, "farmacia", "nombre", fila["Nombre"])

        # Consultorio
        consultorio_bool = True if str(fila["Consultorio"]).lower() == "si" else False

        #  INSERTAR SUCURSAL COMPLETA
        sqlInsertSucursal = """
            INSERT INTO sucursal 
                (consultorio, idFarmacia, idClaseActividad, idCantidadTrabajadores, idTipoFarmacia, longitud, latitud, idDireccion)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(sqlInsertSucursal, (
            consultorio_bool,
            idFarmacia,
            idClaseActividad,
            idCantidadTrab,
            idTipoFarmacia,
            fila["Longitud"],
            fila["Latitud"],
            idDireccion
        ))
        conexion.commit()


    cursor.close()
    conexion.close()
    print("LO LOGRASTE PAPU B)")


if __name__ == '__main__':
    main()
