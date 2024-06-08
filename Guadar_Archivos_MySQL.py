import pandas as pd
from mysql.connector import connect,Error

"""
Araceli Garcia Diaz
30/05/2024
Registrar datos en la tablas de la base de datos
"""


def conectar():
    try:
        conexiondb=connect(host="localhost",user="root",password="",database="HYM")
        return  conexiondb
    except Error as e:
        print(e)

def  GuardarArchivoBaseDatosCategoria(datos):
    try:
        conexion = conectar()  # conectarse a la base de
        cursor=conexion.cursor()
        for index, row in datos.iterrows() :
            categoria = row['Categoría']
            sql = "INSERT INTO Categorias (NombreCate) VALUES ( %s)"
            contenido=(categoria,) # Assuming column names are 'NombrePro' and 'NombreCate'
            cursor.execute(sql, contenido)
            print("datos insertados")
            conexion.commit()  # Commit after each insert
            cursor.execute("SELECT * FROM Categorias;")
            resultados=cursor.fetchall()
            for row in resultados:
                print(row)

        conexion.commit()
        cursor.close()
        conexion.close()
    except Error as e:
        print(e)
def GuardarArchivosBaseDatosMujer(datos2):
    try:
        conexion = conectar()  # Conectarse a la base de datos
        cursor = conexion.cursor()
        for index, row in datos2.iterrows():
            nombre = row['Nombre']
            precio = row['Precio']
            sql = "INSERT INTO Mujer (Nombre, precioMu, Id_cate) VALUES (%s, %s, %s)"
            contenido = (nombre, precio, 2)
            cursor.execute(sql, contenido)
            print("Datos insertados")
            conexion.commit()  # Commit after each insert
            cursor.execute("SELECT * FROM Mujer;")
            resultados = cursor.fetchall()
            for row in resultados:
                print(row)

        conexion.commit()
        cursor.close()
        conexion.close()
    except Error as e:
        print(e)

def GuardarArchivoBaseDatosBebe(datos3):
    try:
        conexion = conectar()  # Conectarse a la base de datos
        cursor = conexion.cursor()
        for index, row in datos3.iterrows():
            nombre = row['Nombre']
            precio = row['Precio']
            sql = "INSERT INTO Bebe (NombreProBebe, precio, Id_cate) VALUES (%s, %s, %s)"
            contenido = (nombre, precio, 1)
            cursor.execute(sql, contenido)
            print("Datos insertados")
            conexion.commit()
            cursor.execute("SELECT * FROM Mujer;")
            resultados = cursor.fetchall()
            for row in resultados:
                print(row)

        conexion.commit()
        cursor.close()
        conexion.close()
    except Error as e:
        print(e)

def GuardarArchivoBaseDatosHombre(datos4):
    try:
        conexion = conectar()  # Conectarse a la base de datos
        cursor = conexion.cursor()
        for index, row in datos4.iterrows():
            nombre = row['Nombre']
            precio = row['Precio']
            sql = "INSERT INTO Hombre (NombreProHombre, precioHombre, Id_cate) VALUES (%s, %s, %s)"
            contenido = (nombre, precio, 3)
            cursor.execute(sql, contenido)
            print("Datos insertados")
            conexion.commit()
            cursor.execute("SELECT * FROM Hombre;")
            resultados = cursor.fetchall()
            for row in resultados:
                print(row)

        conexion.commit()
        cursor.close()
        conexion.close()
    except Error as e:
        print(e)

def GuardarArchivoBaseDatosNiños(datos5):
    try:
        conexion = conectar()  # Conectarse a la base de datos
        cursor = conexion.cursor()
        for index, row in datos5.iterrows():
            nombre = row['Nombre']
            precio = row['Precio']
            sql = "INSERT INTO Niños (NombreProNiño, precioNiños, Id_cate) VALUES (%s, %s, %s)"
            contenido = (nombre, precio, 4)
            cursor.execute(sql, contenido)
            print("Datos insertados")
            conexion.commit()
            cursor.execute("SELECT * FROM Niños;")
            resultados = cursor.fetchall()
            for row in resultados:
                print(row)

        conexion.commit()
        cursor.close()
        conexion.close()
    except Error as e:
        print(e)

def GuardarArchivoBaseDatosBeauty(datos6):
    try:
        conexion = conectar()  # Conectarse a la base de datos
        cursor = conexion.cursor()
        for index, row in datos6.iterrows():
            nombre = row['Nombre']
            precio = row['Precio']
            sql = "INSERT INTO Beauty (NombreProBeauty, precioBeauty, Id_cate) VALUES (%s, %s, %s)"
            contenido = (nombre, precio,5 )
            cursor.execute(sql, contenido)
            print("Datos insertados")
            conexion.commit()
            cursor.execute("SELECT * FROM Beauty;")
            resultados = cursor.fetchall()
            for row in resultados:
                print(row)

        conexion.commit()
        cursor.close()
        conexion.close()
    except Error as e:
        print(e)


def GuardarArchivoBaseDatosHome(datos7):
    try:
        conexion = conectar()  # Conectarse a la base de datos
        cursor = conexion.cursor()
        for index, row in datos7.iterrows():
            nombre = row['Nombre']
            precio = row['Precio']
            sql = "INSERT INTO Home (NombreProSport, precioSport, Id_cate) VALUES (%s, %s, %s)"
            contenido = (nombre, precio, 6)
            cursor.execute(sql, contenido)
            print("Datos insertados")
            conexion.commit()
            cursor.execute("SELECT * FROM Home;")
            resultados = cursor.fetchall()
            for row in resultados:
                print(row)

        conexion.commit()
        cursor.close()
        conexion.close()
    except Error as e:
        print(e)

def GuardarArchivoBaseDatosProductos(datos8):
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        for index, row in datos8.iterrows():
            nombre = row['Nombre']
            precio = row['Precio']
            categoria = row['Categoría']
            sql_categoria = "SELECT Id_cate FROM Categorias WHERE NombreCate = %s"
            cursor.execute(sql_categoria, (categoria,))
            id_categoria = cursor.fetchone()[0]
            sql = "INSERT INTO Productos (NombrePro, Precios, Id_cate) VALUES (%s, %s, %s)"
            contenido = (nombre, precio, id_categoria)
            cursor.execute(sql, contenido)
            print("Datos de producto insertados")
            conexion.commit()
        cursor.close()
        conexion.close()
    except Error as e:
        print(e)

if __name__=="__main__":
    datos=pd.read_csv("DataSet/Categorias.csv")
    datos2=pd.read_csv("DataSet/productosMujer_limpio.csv")
    datos3=pd.read_csv("DataSet/productosBebe.csv_limpio.csv")
    datos4=pd.read_csv("DataSet/productos_Hombre_limpio.csv")
    datos5=pd.read_csv("DataSet/productosninos_limpio.csv")
    datos6=pd.read_csv("DataSet/productoss_Beauty_limpio.csv")
    datos7=pd.read_csv("DataSet/productosHome_limpio.csv")
    datos8=pd.read_csv("DataSet/ProductosUnidos_Limpio.csv")
    GuardarArchivoBaseDatosCategoria(datos)
    GuardarArchivosBaseDatosMujer(datos2)
    GuardarArchivoBaseDatosBebe(datos3)
    GuardarArchivoBaseDatosHombre(datos4)
    GuardarArchivoBaseDatosNiños(datos5)
    GuardarArchivoBaseDatosBeauty(datos6)
    GuardarArchivoBaseDatosHome(datos7)
    GuardarArchivoBaseDatosProductos(datos8)
