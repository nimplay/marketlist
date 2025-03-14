import pandas as pd
import json
import os

def cargar_lista_default():
    """Cargar la lista por default desde 'data/mainlist.csv'."""
    try:
        df = pd.read_csv('data/mainlist.csv')
        return df
    except FileNotFoundError:
        print("Error: No se encontró el archivo 'data/mainlist.csv'.")
        return None

def cargar_listas_usuario():
    """Cargar las listas de compras del usuario desde 'data/listas_usuario/'."""
    listas_usuario = []
    try:
        for archivo in os.listdir('data/listas_usuario'):
            if archivo.endswith('.json'):
                with open(f'data/listas_usuario/{archivo}', 'r') as f:
                    listas_usuario.append(json.load(f))
        return listas_usuario
    except FileNotFoundError:
        return []

def guardar_lista_usuario(lista, nombre_archivo):
    """Guardar una lista de compras del usuario en 'data/listas_usuario/'."""
    os.makedirs('data/listas_usuario', exist_ok=True)
    with open(f'data/listas_usuario/{nombre_archivo}.json', 'w') as f:
        json.dump(lista, f)

def guardar_lista_final(lista_final):
    """Guardar la lista final en 'data/final_list.csv'."""
    df = pd.DataFrame(lista_final)
    df.to_csv('data/final_list.csv', index=False)
