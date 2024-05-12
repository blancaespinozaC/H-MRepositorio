#Ademir Galindo 08/05/2024
#EXTRACCION - CATEGORIA: BEAUTY

import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup


def extraer_datos_producto():
    s = Service(ChromeDriverManager().install())
    option = Options()
    option.add_argument("--window-size=1100,1200")
    navegador = webdriver.Chrome(service=s, options=option)

    navegador.get("https://www2.hm.com/")
    navegador.refresh()
    time.sleep(2)

    #aceptar cookies de la pagina
    btnCli = navegador.find_element(By.ID, "onetrust-accept-btn-handler")
    btnCli.click()
    time.sleep(3)

    #escoger categoria Beauty
    categoria_beauty = navegador.find_element(By.XPATH, "//a[@href='/es_mx/beauty.html']")
    categoria_beauty.click()
    time.sleep(3)

    #seleccionar ver todos en la categoria Beauty
    ver_todo_link = navegador.find_element(By.LINK_TEXT, "Ver Todo")
    ver_todo_link.click()
    time.sleep(10)

    datos = {"Nombre": [], "Precio": []}

    for i in range(5):
        time.sleep(6)
        soup = BeautifulSoup(navegador.page_source, "html.parser")
        productos = soup.find_all("div", class_="eed2a5 ec329a d5728c")

        for producto in productos:
            nombre_elemento = producto.find("h2", class_="d1cd7b a09145 e07e0d a04ae4").text.strip()
           precio_elemento = producto.find("span", class_=["aeecde", "ac3d9e", "b19650"])

            # Para el nombre del producto
            if nombre_elemento:
                nombre = nombre_elemento.text
            else:
                nombre = ""

            if nombre:
                nombre = nombre
            else:
                nombre = "No disponible"

            # Para el precio del producto
            if precio_elemento:
                precio = precio_elemento.text
            else:
                precio = ""

            if precio:
                precio = precio
            else:
                precio = "No disponible"


            datos["Nombre"].append(Nombre)
            datos["Precio"].append(Precio)

        NextPag = navegador.find_element(By.XPATH,"//button[contains(@class, 'f05bd4') and contains(@class, 'aaa2a2') and contains(@class, 'ab0e07') and contains(text(), 'Cargar siguiente página')]")
        NextPag.click()

    df = pd.DataFrame(datos)
    df.to_csv("DataSet/productoss_Beauty.csv")

    time.sleep(10)
    navegador.close()

if __name__ == "__main__":
    extraer_datos_producto()
