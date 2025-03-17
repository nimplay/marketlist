import pandas as pd
import os

def create_new_shopping_list(list_name, items):
    """
    Crea un nuevo archivo CSV con una lista de compras en la carpeta data/userlists.
    Si un producto no existe en finallist.csv, lo añade.

    :param list_name: Nombre del archivo CSV (sin extensión).
    :param items: Lista de diccionarios con los items de la lista de compras.
    """
    # Definir las columnas del CSV
    columns = ["Nombre", "Peso", "Medida", "Precio", "Prioridad", "Tipo", "Etiqueta", "FrecuenciaCompra", "Preferencia"]

    # Crear un DataFrame con los items
    df = pd.DataFrame(items, columns=columns)

    # Guardar la lista en userlists
    file_path = os.path.join("data", "userlists", f"{list_name}.csv")
    df.to_csv(file_path, index=False)
    print(f"Lista guardada en {file_path}")

    # Actualizar finallist.csv
    update_final_list(items)

def update_final_list(items):
    """
    Actualiza finallist.csv con los nuevos productos si no existen.

    :param items: Lista de diccionarios con los items de la lista de compras.
    """
    final_list_path = os.path.join("data", "finallist.csv")

    if os.path.exists(final_list_path):
        final_list = pd.read_csv(final_list_path)
    else:
        final_list = pd.DataFrame(columns=["Nombre", "Peso", "Medida", "Precio", "Prioridad", "Tipo", "Etiqueta", "FrecuenciaCompra", "Preferencia"])

    # Añadir productos nuevos a finallist.csv
    for item in items:
        if item["Nombre"] not in final_list["Nombre"].values:
            final_list = final_list.append(item, ignore_index=True)

    # Guardar finallist.csv actualizado
    final_list.to_csv(final_list_path, index=False)
    print(f"finallist.csv actualizado.")
