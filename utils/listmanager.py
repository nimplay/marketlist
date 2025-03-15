import pandas as pd

def generate_shopping_list_logic(df, budget):
    """
    Genera una lista de compras basada en el presupuesto.
    - Prioriza productos preferidos y de alta prioridad.
    - Maximiza la variedad de productos.
    - Respeta el presupuesto.
    """
    # Filtrar productos alcanzables
    df = df[df["Precio"] <= budget]

    # Ordenar por Preferencia, Prioridad y Frecuencia de Compra
    df = df.sort_values(by=["Preferencia", "Prioridad", "FrecuenciaCompra"], ascending=[False, False, False])

    shopping_list = []
    remaining_budget = budget
    used_types = set()  # Para rastrear tipos de productos ya añadidos

    # Primera fase: Agregar un producto de cada tipo
    for _, row in df.iterrows():
        if row["Tipo"] not in used_types and row["Precio"] <= remaining_budget:
            quantity = 1  # Empezar con 1 unidad
            shopping_list.append({
                "Nombre": row["Nombre"],
                "Peso": row["Peso"],
                "Medida": row["Medida"],
                "Cantidad": quantity,
                "PrecioUnitario": row["Precio"],
                "PrecioTotal": quantity * row["Precio"],
                "Tipo": row["Tipo"]
            })
            remaining_budget -= quantity * row["Precio"]
            used_types.add(row["Tipo"])

    # Segunda fase: Aumentar cantidades de los productos ya seleccionados
    while remaining_budget >= df["Precio"].min():
        product_added = False
        for _, row in df.iterrows():
            if row["Tipo"] in used_types and row["Precio"] <= remaining_budget:
                # Buscar el producto en la lista de compras
                item = next((item for item in shopping_list if item["Nombre"] == row["Nombre"]), None)
                if item:
                    max_quantity = int(remaining_budget // row["Precio"])
                    additional = min(max_quantity, int(row["FrecuenciaCompra"] * 10))
                    if additional > 0:
                        item["Cantidad"] += additional
                        item["PrecioTotal"] += additional * row["Precio"]
                        remaining_budget -= additional * row["Precio"]
                        product_added = True
        if not product_added:
            break  # Salir si no se puede agregar más

    return shopping_list, remaining_budget
