import pandas as pd
import os

def load_final_list():
    """Carga el archivo finallist.csv."""
    return pd.read_csv("data/finallist.csv")

def save_shopping_list(shopping_list, filename):
    """Guarda la lista de compras en un archivo CSV."""
    df = pd.DataFrame(shopping_list)
    df.to_csv(filename, index=False)
