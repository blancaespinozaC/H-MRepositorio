# airbnb
#PROYECTO airbnb
#CODIGO DE EXTRACCION DE DATOS DE airbnb    
import requests
import pandas as pd
from bs4 import BeautifulSoup



def start_webscraping():
    response = requests.get("https://www.airbnb.mx")


    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html5lib")
        titulos=soup.findAll("div", attrs={"class":"t1jojoys"})
        extraInfo=soup.findAll("div",attrs={"class":"g1qv1ctd"})

        all_info={"tittle":[],"info":[],"fecha":[],"precio":[],"calificacion":[]}

        for item in titulos:
            all_info["tittle"].append(item.text)

        for item in extraInfo:
            info=item.find("div",attrs={"class":"fb4nyux atm_da_cbdd7d s1cjsi4j atm_g3_1kw7nm4 atm_ks_15vqwwr atm_sq_1l2sidv atm_9s_cj1kg8 atm_6w_1e54zos atm_fy_kb7nvz atm_7l_1he744i atm_ks_zryt35__1rgatj2 dir dir-ltr"})
            fecha=item.find("span",attrs={"class":" dir dir-ltr"})
            precio=item.find("div",attrs={"class":"pquyp1l atm_da_cbdd7d pi11895 atm_h3_lh1qj6 dir dir-ltr"})
            calificacion=item.find("span",attrs={"class":"ru0q88m atm_cp_1ts48j8 dir dir-ltr"})

            if info is not None:
                all_info["info"].append(info.text)
            else:
                all_info["info"].append("N/A")

            if fecha is not None:
                all_info["fecha"].append(fecha.text)
            else:
                all_info["fecha"].append("N/A")

            if precio is not None:
                all_info["precio"].append(precio.text)
            else:
                all_info["precio"].append("N/A")

            if calificacion is not None:
                all_info["calificacion"].append(calificacion.text)
            else:
                all_info["calificacion"].append("0.0")

        df=pd.DataFrame(all_info)
        print(df.shape)
        df.to_csv("DataSet/airbnb2.csv", index=False)

    else:
        raise Exception("Ocurrio un error!")




if __name__ == "__main__" :
    start_webscraping()
