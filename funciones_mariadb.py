import pymysql
import sys

def Conexion_BD(usuario, password, host, database):
    try:
        conexion = pymysql.connect(user=usuario, password=password, host=host, database=database)
        print("Conectado a la base de datos:")
        return conexion
    except pymysql.Error as e:
        print("No puedo conectar a la base de datos:", e)
        sys.exit(1)

def desconectar(connection):
    if connection:
        connection.close()

def listar_informacion(connection):
    try:
        cursor = connection.cursor()
        query = "SELECT FECHA, TEMP FROM ESTIMACION_DEMANDA"
        cursor.execute(query)
        rows = cursor.fetchall()
        total = len(rows)

        print("\nListado de información:")
        print("{:<12} {:<15}".format("Fecha", "Temperatura"))
        print("-" * 30)

        for row in rows:
            fecha, temp = row
            print("{:<12} {:<15}".format(str(fecha), str(temp)))

        print("-" * 30)
        print(f"Total de registros: {total}")

    except pymysql.Error as error:
        print("Error al listar información:", error)


def buscar_informacion(connection):
    try:
        cursor = connection.cursor()
        temp = float(input("Introduce la temperatura a buscar: "))
        query = f"SELECT * FROM ESTIMACION_DEMANDA WHERE TEMP = {temp}"
        cursor.execute(query)
        rows = cursor.fetchall()

        print("\nResultado de la búsqueda:")
        if not rows:
            print("No se encontraron resultados para la temperatura proporcionada.")
        else:
            print("{:<12} {:<8} {:<15} {:<15}".format("Fecha", "ID", "Temperatura", "Demanda"))
            print("-" * 55)

            for row in rows:
                fecha, id, temperatura, demanda = row
                print("{:<12} {:<8} {:<15} {:<15}".format(str(fecha), str(id), str(temperatura), str(demanda)))

    except pymysql.Error as error:
        print("Error al buscar información:", error)


def buscar_informacion_relacionada(connection):
    try:
        cursor = connection.cursor()
        nombre_empresa = input("Introduce el nombre de la empresa para buscar información relacionada: ")
        
        query = f"SELECT C.COD_CENTRAL, C.FECHA, C.UBICACION, C.CAPACIDAD_MAX " \
                f"FROM CENTRALES C " \
                f"INNER JOIN EMPRESA E ON C.CIF = E.CIF " \
                f"WHERE E.NOMBRE = %s"

        cursor.execute(query, (nombre_empresa,))
        rows = cursor.fetchall()

        print("\nInformación relacionada para la empresa:", nombre_empresa)
        if not rows:
            print(f"No se encontraron resultados para la empresa {nombre_empresa}.")
        else:
            print("{:<12} {:<15} {:<30} {:<15}".format("Código", "Fecha", "Ubicación", "Capacidad Máxima"))
            print("-" * 80)

            for row in rows:
                codigo, fecha, ubicacion, capacidad_max = row
                formatted_fecha = fecha.strftime('%Y-%m-%d')
                print("{:<12} {:<15} {:<30} {:<15}".format(str(codigo), str(formatted_fecha), str(ubicacion), str(capacidad_max)))

    except pymysql.connector.Error as error:
        print("Error al buscar información relacionada:", error)


def insertar_informacion(connection):
    try:
        cursor = connection.cursor()
        fecha = input("Introduce la fecha (YYYY-MM-DD): ")
        cuota_produccion = float(input("Introduce la cuota de producción: "))
        temp = float(input("Introduce la temperatura: "))
        demanda = float(input("Introduce la demanda: "))
        query = f"INSERT INTO ESTIMACION_DEMANDA VALUES (STR_TO_DATE('{fecha}', '%Y-%m-%d'), {cuota_produccion}, {temp}, {demanda})"
        cursor.execute(query)
        connection.commit()
        print("\nInformación insertada correctamente.")

    except pymysql.Error as error:
        connection.rollback()
        print("Error al insertar información:", error)

def borrar_informacion(connection):
    try:
        cursor = connection.cursor()
        fecha = input("Introduce la fecha para borrar información: ")
        query = f"DELETE FROM ESTIMACION_DEMANDA WHERE FECHA = STR_TO_DATE('{fecha}', '%Y-%m-%d')"
        
        cursor.execute(query)
        rows_deleted = cursor.rowcount

        if rows_deleted > 0:
            connection.commit()
            print("\nInformación borrada correctamente.")
        else:
            print("\nNo se encontró información para la fecha especificada.")

    except pymysql.connector.Error as error:
        connection.rollback()
        print("Error al borrar información:", error)

def actualizar_informacion(connection):
    try:
        cursor = connection.cursor()
        fecha = input("Introduce la fecha para actualizar información: ")
        nueva_temp = float(input("Introduce la nueva temperatura: "))
        query = f"UPDATE ESTIMACION_DEMANDA SET TEMP = {nueva_temp} WHERE FECHA = STR_TO_DATE('{fecha}', '%Y-%m-%d')"
        cursor.execute(query)
        connection.commit()
        print("\nInformación actualizada correctamente.")

    except pymysql.Error as error:
        connection.rollback()
        print("Error al actualizar información:", error)

if __name__ == "__main__":
    usuario = 'tu_usuario'
    password = 'tu_password'
    host = 'localhost'
    database = 'tu_base_de_datos'
    connection = Conexion_BD(usuario, password, host, database)

    if connection:
        try:
            listar_informacion(connection)
            buscar_informacion(connection)
            buscar_informacion_relacionada(connection)
            insertar_informacion(connection)
            borrar_informacion(connection)
            actualizar_informacion(connection)

        finally:
            desconectar(connection)
