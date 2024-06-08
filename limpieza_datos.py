"""
Araceli Garcia Diaz Y Divani Tovilla Barradas
14/05/2024
Limpieza de los datos en los archivos csv
"""
import pandas as pd


def LimpiarValores(df: pd.DataFrame) -> pd.DataFrame:
    # Identificar los elementos nulos
    nulos = df.isnull()
    # Eliminar elementos nulos
    df.dropna(axis="columns", inplace=True)

    # Identificar duplicados
    dupli = df.duplicated()
    # Eliminar duplicados
    df.drop_duplicates(inplace=True)

    # Reemplazar el valor de $
    if "Precio" in df.columns:
        df["Precio"] = df["Precio"].str.replace("$", "")

    return df  # Asegúrate de devolver el DataFrame limpio


def UnirArchivos(dataframes: list) -> pd.DataFrame:
    # Unir todas las categorías
    union = pd.concat(dataframes, axis="index", ignore_index=True)
    return union


def UnionCategorias(dataframes: list) -> pd.DataFrame:
    for df in dataframes:
        df.drop(["Nombre", "Precio"], axis="columns", inplace=True)

    datos_eliminados = pd.concat(dataframes,ignore_index=True)
    return datos_eliminados




if __name__ == "__main__":
    archivos = [
        "productosBebe.csv",
        "productosMujer.csv",
        "productos_Hombre.csv",
        "productosninos.csv",
        "productoss_Beauty.csv",
        "productosHome.csv",
        "productoSport.csv"
    ]

    dataframes = []

    for archivo in archivos:
        rutaEntrada = "DataSet/" + archivo
        rutaSalida = "DataSet/" + archivo[:-4] + "_limpio.csv"

        # Cargar el archivo CSV
        df = pd.read_csv(rutaEntrada)

        # Limpiar datos
        df_limpio = LimpiarValores(df)
        dataframes.append(df_limpio)

        # Guardar el archivo limpio
        df_limpio.to_csv(rutaSalida, index=False)

    # Unir todos los archivos limpios en uno solo
    union = UnirArchivos(dataframes)


    union_limpio = LimpiarValores(union)

    union_limpio.to_csv("DataSet/ProductosUnidos_Limpio.csv", index=False)


    datos_eliminados = UnionCategorias(dataframes)
    datos_eliminados_limpio = LimpiarValores(datos_eliminados)
    datos_eliminados_limpio.to_csv("DataSet/Categorias.csv", index=False)

