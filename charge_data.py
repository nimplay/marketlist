import pandas as pd

# Función para cargar datos manualmente
def cargar_datos_manual():
    print("Por favor, ingresa los datos del producto:")
    nombre = input("Nombre: ")
    peso = input("Peso: ")
    medida = input("Medida: ")
    precio = input("Precio: ")
    prioridad = input("Prioridad: ")
    tipo = input("Tipo: ")
    etiqueta = input("Etiqueta: ")

    # Crear un diccionario con los datos ingresados
    nuevo_producto = {
        'Nombre': nombre,
        'Peso': peso,
        'Medida': medida,
        'Precio': precio,
        'Prioridad': prioridad,
        'Tipo': tipo,
        'Etiqueta': etiqueta
    }

    return nuevo_producto

# Función para agregar datos al CSV
def agregar_al_csv(nuevo_producto, archivo_csv):
    # Leer el archivo CSV existente
    df = pd.read_csv(archivo_csv)

    # Convertir el nuevo producto en un DataFrame
    nuevo_df = pd.DataFrame([nuevo_producto])

    # Concatenar el DataFrame existente con el nuevo
    df = pd.concat([df, nuevo_df], ignore_index=True)

    # Guardar el DataFrame actualizado en el archivo CSV
    df.to_csv(archivo_csv, index=False)
    print("Producto agregado exitosamente!")

# Archivo CSV
archivo_csv = 'mainlist.csv'

# Cargar datos manualmente
nuevo_producto = cargar_datos_manual()

# Agregar los datos al CSV
agregar_al_csv(nuevo_producto, archivo_csv)
