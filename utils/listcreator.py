# utils/listcreator.py
import pandas as pd
import os

def create_new_shopping_list(list_name, items):
    """
    Crea un nuevo archivo CSV con una lista de compras en la carpeta data/userlists.

    :param list_name: Nombre del archivo CSV (sin extensión).
    :param items: Lista de diccionarios con los items de la lista de compras.
    """
    # Definir las columnas del CSV
    columns = ["Nombre", "Peso", "Medida", "Precio", "Prioridad", "Tipo", "Etiqueta", "FrecuenciaCompra", "Preferencia"]

    # Crear un DataFrame con los items
    df = pd.DataFrame(items, columns=columns)

    # Crear la ruta completa del archivo
    file_path = os.path.join("data", "userlists", f"{list_name}.csv")

    # Guardar el DataFrame como CSV
    df.to_csv(file_path, index=False)
    print(f"Lista guardada en {file_path}")
