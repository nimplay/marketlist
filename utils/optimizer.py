def ajustar_prioridades(df, listas_usuario):
    """Ajustar las prioridades basado en las listas de compras del usuario."""
    for lista in listas_usuario:
        for producto in lista:
            nombre = producto['Nombre']
            if nombre in df['Nombre'].values:
                df.loc[df['Nombre'] == nombre, 'Prioridad'] += 1
    return df

def generar_lista_final(df, listas_usuario):
    """Generar la lista final basada en la mainlist y las listas del usuario."""
    df_final = df.copy()
    if listas_usuario:
        df_final = ajustar_prioridades(df_final, listas_usuario)
    return df_final

def generar_lista_sugerente(df_final, presupuesto):
    """Generar una lista de compras sugerente basada en el presupuesto."""
    lista_sugerente = []
    total_gastado = 0
    categorias_incluidas = set()

    # Ordenar productos por prioridad (de mayor a menor)
    df_ordenado = df_final.sort_values(by='Prioridad', ascending=False)

    for _, producto in df_ordenado.iterrows():
        if (total_gastado + producto['Precio'] <= presupuesto and
            producto['Etiqueta'] not in categorias_incluidas):
            lista_sugerente.append(producto.to_dict())
            categorias_incluidas.add(producto['Etiqueta'])
            total_gastado += producto['Precio']

    return lista_sugerente, total_gastado
