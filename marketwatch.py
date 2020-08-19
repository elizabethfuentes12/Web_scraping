
from bs4 import BeautifulSoup
import requests
import pandas as pd



ticker=[]
ticker_change=[]
titular = []
link = []
extract=[]
r=requests.get("https://www.marketwatch.com/markets?mod=top_nav")
res=BeautifulSoup(r.text,"lxml")
contenedor=res.find_all("div",{"class":"article__content"})

for elem in contenedor:
    
    titular.append(elem.find("a").text)
    link.append(elem.find("a")["href"])
    if (len(elem.find("a")["href"]))>1:
        r2=requests.get(elem.find("a")["href"])
        res2=BeautifulSoup(r2.text,"lxml") 
        contenedor2=res2.find_all("div",{"id":"js-article__body"})
        if (len(contenedor2))>0:
            extract.append(contenedor2[0].find_all({"p"})[0].text)
        else:
            if (len(contenedor2))<1:
                extract.append("0")
            else:
                contenedor2=res2.find_all("div",{"id":"video-hole"})
                extract.append(contenedor2[0].find_all("article",{"id":"article"})[0].text)
    else: 
        extract.append("0")

    try:
        ticker.append(elem.find("span",{"class":"ticker__symbol"}).text)
        ticker_change.append(elem.find("bg-quote",{"class":"ticker__change"}).text)
    except:
        ticker.append("0")
        ticker_change.append("0")
        continue

noticia=pd.DataFrame({'titular': titular,"extract":extract,"ticker_change":ticker_change,"ticker":ticker,'link': link})#
noticia['titular'] = noticia['titular'].map(lambda x: x.lstrip("\r\n                            \r\n                            ").rstrip('\r\n'))
noticia=noticia.drop_duplicates()



# %%
