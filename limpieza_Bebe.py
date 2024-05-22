import pandas as pd


def LimpiarValores(df: pd.read_csv):
    # Identificar los elementos nulos
    nulos = df.isnull()
    # Eliminar elementos nulos
    df.dropna(axis="columns", inplace=True)

    # Identificar duplicados
    dupli = df.duplicated()
    # Eliminar duplicados
    df.drop_duplicates(inplace=True)

    #Reemplazar el valor de $
    df["Precio"]=df["Precio"].str.replace("$","")
def UnirArchivos(d1,d2,d3,d4,d5,d6,d7):
    #Unir todas las categorias
    union = pd.concat([d1, d2,d3,d4,d5,d6,d7],axis="index",ignore_index=True)
    pd.DataFrame(union)
    unionarc=union.to_csv("DataSet/ProductosUnidos.csv")
    return unionarc


if __name__ == "__main__":
    archivos = [
        "productosBebe.csv",
        "productos.csv",
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
        LimpiarValores(df)

        # Guardar el archivo limpio
        df.to_csv(rutaSalida, index=False)
        dataframes.append(df)

    # Unir todos los archivos limpios en uno solo
    UnirArchivos(*dataframes)