#Blanca Espinoza 08/05/2024
#EXTRACCION - CATEGORIA : MUJER 
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
    time.sleep(2)

    btnCli = navegador.find_element(By.ID, "onetrust-accept-btn-handler")
    btnCli.click()
    time.sleep(3)

    CateCli = navegador.find_element(By.CSS_SELECTOR, "a.CGae.__9y2v.vEfo")
    CateCli.click()
    time.sleep(5)

    verTodo_button = navegador.find_element(By.CSS_SELECTOR,".CTA-module--action__1qN9s.CTA-module--medium__1uoRl.CTA-module--reset__1G6AO.ListItem-module--link__1MuqR")
    verTodo_button.click()
    time.sleep(4)

    datos = {"Nombre": [], "Precio": []}

    for _ in range(5):
        time.sleep(10)
        soup = BeautifulSoup(navegador.page_source, "html.parser")
        productos = soup.find_all("div", class_="eed2a5 ec329a d5728c")

        for producto in productos:
            nombre = producto.find("h2", class_="d1cd7b a09145 e07e0d a04ae4").text.strip()
            precio_element = producto.find("span", class_="aeecde ac3d9e b19650")
            precio = precio_element.text.strip() if precio_element else "Precio no disponible"

            datos["Nombre"].append(nombre)
            datos["Precio"].append(precio)

        siguiente_pagina = navegador.find_element(By.XPATH,"//button[contains(@class, 'f05bd4') and contains(@class, 'aaa2a2') and contains(@class, 'ab0e07') and contains(text(), 'Cargar siguiente página')]")
        siguiente_pagina.click()

    df = pd.DataFrame(datos)
    df.to_csv("DataSet/productos.csv")


    time.sleep(20)
    navegador.close()

if __name__ == "__main__":
    extraer_datos_producto()
