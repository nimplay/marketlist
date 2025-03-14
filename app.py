from utils.data_loader import cargar_lista_default, cargar_listas_usuario, guardar_lista_usuario, guardar_lista_final
from utils.list_manager import crear_lista_compras
from utils.optimizer import generar_lista_final, generar_lista_sugerente
import pandas as pd

def mostrar_lista_sugerente(lista_sugerente, total_gastado, presupuesto):
    """Mostrar la lista de compras sugerente."""
    print("\nLista de Compras Sugerente:")
    for producto in lista_sugerente:
        print(f"- {producto['Nombre']} - {producto['Precio']}")
    print(f"\nTotal gastado: {total_gastado}")
    print(f"Dinero restante: {presupuesto - total_gastado}")

def main():
    # Cargar la lista por default
    df = cargar_lista_default()
    if df is None:
        return

    # Cargar listas de compras del usuario
    listas_usuario = cargar_listas_usuario()

    # Generar la lista final
    df_final = generar_lista_final(df, listas_usuario)
    guardar_lista_final(df_final.to_dict('records'))

    while True:
        print("\nOpciones:")
        print("1. Añadir lista de compras")
        print("2. Generar lista de compras sugerente")
        print("3. Salir")
        opcion = input("Selecciona una opción: ")

        if opcion == '1':
            # Crear una nueva lista de compras
            nueva_lista = crear_lista_compras(df)
            if nueva_lista:
                listas_usuario.append(nueva_lista)
                guardar_lista_usuario(nueva_lista, f"lista_{len(listas_usuario)}")
                print("Lista de compras añadida exitosamente.")

        elif opcion == '2':
            # Solicitar el presupuesto del usuario
            presupuesto = float(input("Ingresa tu presupuesto: "))

            # Generar la lista de compras sugerente
            lista_sugerente, total_gastado = generar_lista_sugerente(df_final, presupuesto)

            # Mostrar la lista sugerente
            mostrar_lista_sugerente(lista_sugerente, total_gastado, presupuesto)

        elif opcion == '3':
            break

        else:
            print("Opción no válida. Intenta de nuevo.")

# Ejecutar la aplicación
if __name__ == "__main__":
    main()
