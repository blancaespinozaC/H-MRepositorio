"""
Divani Tovilla Barradas
07/05/2024
Extraccion de datos productos: NIÑOS
"""

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

    # Abre la página web de H&M
    navegador.get("https://www2.hm.com/")
    navegador.refresh()
    time.sleep(2)

    # Acepta las cookies
    btnCli = navegador.find_element(By.ID, "onetrust-accept-btn-handler")
    btnCli.click()
    time.sleep(20)

    # Hace clic en la categoría deseada
    CateCli = navegador.find_element(By.XPATH, "//a[@href='/es_mx/ninos.html']")
    CateCli.click()
    time.sleep(20)

    # Hace clic en "Ver todos"
    #ver_todo_link = navegador.find_element(By.LINK_TEXT, "Ver todok")
    #ver_todo_link.click()
    #time.sleep(10)


    # Seleccionar todos los elementos "Ver todos"
    ver_todo_links = navegador.find_elements(By.LINK_TEXT, "Ver todo")

    ver_todo_links[4].click()

    datos = {"Nombre": [], "Precio": []}

    for _ in range(9):  # Cambia el número de páginas
        time.sleep(10)
        soup = BeautifulSoup(navegador.page_source, "html.parser")
        productos = soup.find_all("div", class_="eed2a5 ec329a d5728c")

        for producto in productos:
            nombre_elemento = producto.find("h2", class_="d1cd7b a09145 e07e0d a04ae4")
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

            datos["Nombre"].append(nombre)
            datos["Precio"].append(precio)

        siguiente_pagina = navegador.find_element(By.XPATH,"//button[contains(@class, 'f05bd4') and contains(@class, 'aaa2a2') and contains(@class, 'ab0e07') and contains(text(), 'Cargar siguiente página')]")
        siguiente_pagina.click()

    df = pd.DataFrame(datos)
    df["Categoría"] = "Ninos"
    df.to_csv("DataSet/productosninos.csv", index=False)

    time.sleep(10)
    navegador.close()

if __name__ == "__main__":
    extraer_datos_producto()
