from bs4 import BeautifulSoup
import requests
import pandas as pd
 
tipo=["empresas","mercados","economia_y_politica","internacional"]
titular = []
link = []
extracto=[]
df_final=[]

for n in tipo:
    pagina="https://www.df.cl/"+n
    r=requests.get(pagina)
    res=BeautifulSoup(r.text,"lxml")
    contenedor_notebook=res.find_all("article", {"class":"col-md-12"})

    for elem in contenedor_notebook:
        try:
            titular.append(elem.find("h2").text)
            enlace=str("https://www.df.cl")+str(elem.find("a")["href"])
            link.append(enlace)

            r2=requests.get(enlace)
            res2=BeautifulSoup(r2.text,"lxml")
            contenedor_link=res2.find_all("article", {"class":"auxi_articulo"})
            data_extracto=contenedor_link[0]["data-extracto"]
            extracto.append(data_extracto)

        except:
            continue
    
    noticia=pd.DataFrame({'titular': titular, 'link': link, 'extracto': extracto})
    noticia['titular'] = noticia['titular'].map(lambda x: x.lstrip("\n\n                                          ").rstrip('\n'))

    if len(df_final)>0:
        df_final=pd.concat([df_final, noticia], ignore_index=True)
    else: 
        df_final=noticia.copy()