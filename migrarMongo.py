import pymysql
from pymysql import MySQLError
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from decimal import Decimal

# Convertir decimal a float, pq mongo es nena y no lo acepta
def convertir(document):
    for key, value in document.items():
        if isinstance(value, Decimal):
            document[key] = float(value)
    return document


# *************************************
# MIGRACIÓN
def migrar():
    # Conexion con SQL
    try:
        mysql_conn = pymysql.connect(
            host='localhost',
            user='root',
            password='1234',
            database='proyectobd'
        )
        print("Conexión a MySQL exitosa.")
    except MySQLError as e:
        print("Error al conectar a MySQL:", e)
        exit()

    # *************************************
    # Conectar con mongo
    try:
        mongo_client = MongoClient("mongodb://localhost:27017/")
        mongo_db = mongo_client["proyectobd_mongo"]
        print("Conexión a MongoDB exitosa.")
    except PyMongoError as e:
        print("Error al conectar a MongoDB:", e)
        mysql_conn.close()
        exit()

    # *************************************
    # Mapeo de sp's pq no usamos los mismos nombres de las tablas xd

    sp_select = {
        "municipio": "sp_getAll_municipio",
        "tipo_vialidad": "sp_getAll_tipovia",
        "colonia": "sp_getAll_colonia",
        "direccion": "sp_getAll_direccion",
        "tipo_farmacia": "sp_getAll_tipofarma",
        "farmacia": "sp_getAll_farma",
        "clase_actividad": "sp_getAll_claseact",
        "cantidad_trabajadores": "sp_getAll_cantidadtraba",
        "sucursal": "sp_getAll_sucursal",
        "loggs": "sp_getall_logs"
    }

    tables = list(sp_select.keys())
    print("\nTablas:", tables)

    # *************************************
    # Migracion tabla por tabla

    for table in tables:
        print(f"\n========== Migrando tabla: {table} ==========")

        try:
            with mysql_conn.cursor(pymysql.cursors.DictCursor) as cursor:

                sp_name = sp_select[table]
                print(f"Llamando SP: {sp_name}")

                cursor.callproc(sp_name)
                data = cursor.fetchall()

                if not data:
                    print("No se encontraron datos en esta tabla.")
                    continue

                # Convertir Decimales a float con la funcion convertir
                data = [convertir(doc) for doc in data]

                # Insertar en MongoDB
                mongo_db[table].insert_many(data)

                print(f"Migración completada para '{table}'. Registros: {len(data)}")

        except MySQLError as e:
            print(f"Error MySQL en la tabla '{table}': {e}")

        except PyMongoError as e:
            print(f"Error MongoDB en la tabla '{table}': {e}")

        except Exception as e:
            print(f"Error en tabla '{table}': {e}")

    # *************************************
    # Cerrar conexiones
    mysql_conn.close()
    mongo_client.close()
    print(" BUENA MIGRACIÓN BRO  ")


# Ejecutar
if __name__ == "__main__":
    migrar()
