import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from bs4 import BeautifulSoup

def bot_login():
    # Configuración del servicio y las opciones del navegador
    s = Service(ChromeDriverManager().install())
    options = Options()
    options.add_argument("--window-size=1020,1200")

    navegador = webdriver.Chrome(service=s, options=options)
    navegador.get("https://www2.hm.com/es_mx/index.html")
    time.sleep(7)

    # Aceptar cookies
    cookies = navegador.find_element(By.ID, "onetrust-accept-btn-handler")
    cookies.click()
    time.sleep(5)

    home = navegador.find_element(By.XPATH, "//a[@href='/es_mx/home.html']")
    home.click()
    time.sleep(15)

    ver_todo_link = navegador.find_element(By.LINK_TEXT, "Ver todo")
    ver_todo_link.click()
    time.sleep(10)

    # Reemplaza el bucle for pagina in range(5) con el siguiente código
    while True:
        try:
            siguiente_pagina = navegador.find_element(By.XPATH,"//button[contains(@class, 'f05bd4') and contains(@class, 'aaa2a2') and contains(@class, 'ab0e07') and contains(text(), 'Cargar siguiente página')]")
            siguiente_pagina.click()
            time.sleep(10)  # Aumentar el tiempo de espera después de hacer clic en el enlace
        except Exception as e:
            print("Error al cambiar de página:", e)
            break

    # Nombre de producto, rating, precio, fecha de entrega
    Nombres = navegador.find_elements(By.CSS_SELECTOR, "h2.d1cd7b.a09145.e07e0d.a04ae4")
    Precios = navegador.find_elements(By.CSS_SELECTOR, "p.d3254e.a1b659 > span.aeecde.ac3d9e.b19650")

    datos = {
        "Nombre del producto": [],
        "Precio": []
    }

    for extraccion in range(len(Nombres)):
        if extraccion < len(Nombres):
            nombre = Nombres[extraccion].text
        else:
            nombre = "sin nombre"
        if extraccion < len(Precios):
            precio = Precios[extraccion].text  # Corregido aquí
        else:
            precio = "no contiene precio"

        datos["Nombre del producto"].append(nombre)
        datos["Precio"].append(precio)

    df = pd.DataFrame(datos)
    df.to_csv("Datasets/DATOS.csv")
    time.sleep(7)
    navegador.close()

if __name__ == "__main__":
    bot_login()