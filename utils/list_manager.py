def crear_lista_compras(df):
    """Permitir al usuario crear una lista de compras manualmente."""
    lista_compras = []
    while True:
        print("\nSelecciona un producto para agregar:")
        print(df.to_string(index=False))

        producto_id = int(input("Ingresa el ID del producto (0 para terminar): "))
        if producto_id == 0:
            break

        producto = df.iloc[producto_id - 1].to_dict()
        lista_compras.append(producto)
        print(f"Producto '{producto['Nombre']}' agregado a la lista de compras.")

    return lista_compras
