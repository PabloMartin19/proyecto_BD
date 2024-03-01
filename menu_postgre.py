import psycopg2
from funciones_postgre import (
    Conexion_BD,
    desconectar,
    listar_informacion,
    buscar_informacion,
    buscar_informacion_relacionada,
    insertar_informacion,
    borrar_informacion,
    actualizar_informacion
)

usuario = 'postgres'
password = 'messi'
host = 'localhost'
database = 'proyecto'

conexion = Conexion_BD(usuario, password, host, database)

def mostrar_menu():
    print("\n════════════════════════════════════════════════════")
    print("               MENÚ PRINCIPAL")
    print("════════════════════════════════════════════════════")
    print("1. Mostrar información de fechas y temperaturas en ESTIMACION_DEMANDA.")
    print("2. Buscar información por temperatura en ESTIMACION_DEMANDA.")
    print("3. Muestra información de la tabla CENTRALES en base a el nombre de la EMPRESA.")
    print("4. Insertar nueva fila en ESTIMACION_DEMANDA con fecha, cuota, temperatura y demanda.")
    print("5. Eliminar filas en ESTIMACION_DEMANDA por fecha.")
    print("6. Actualizar temperatura en ESTIMACION_DEMANDA por fecha.")
    print("0. Salir")
    print("════════════════════════════════════════════════════")


def ejecutar_opcion(opcion, connection):
    if opcion == "1":
        listar_informacion(connection)
    elif opcion == "2":
        buscar_informacion(connection)
    elif opcion == "3":
        buscar_informacion_relacionada(connection)
    elif opcion == "4":
        insertar_informacion(connection)
    elif opcion == "5":
        borrar_informacion(connection)
    elif opcion == "6":
        actualizar_informacion(connection)
    elif opcion == "0":
        print("\nSaliendo del programa.")
    else:
        print("\nOpción no válida. Introduce un número del 0 al 6.")

if __name__ == "__main__":
    try:
        while True:
            mostrar_menu()
            opcion = input("Selecciona una opción (0-6): ")
            ejecutar_opcion(opcion, conexion)
            if opcion == "0":
                break

    finally:
        desconectar(conexion)

