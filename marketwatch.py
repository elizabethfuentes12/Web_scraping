from bs4 import BeautifulSoup
import requests
import pandas as pd

ticker=[]
ticker_change=[]
titular = []
link = []
r=requests.get("https://www.marketwatch.com/markets?mod=top_nav")
res=BeautifulSoup(r.text,"lxml")
contenedor=res.find_all("div",{"class":"article__content"})

for elem in contenedor:
    try:
        titular.append(elem.find("a").text)
        link.append(elem.find("a")["href"])
        ticker.append(elem.find("span",{"class":"ticker__symbol"}).text)
        ticker_change.append(elem.find("bg-quote",{"class":"ticker__change"}).text)

    except:
        ticker.append("0")
        ticker_change.append("0")
        continue

noticia=pd.DataFrame({'titular': titular,"ticker_change":ticker_change,"ticker":ticker,'link': link})#
noticia['titular'] = noticia['titular'].map(lambda x: x.lstrip("\r\n                            \r\n                            ").rstrip('\r\n'))
noticia=noticia.drop_duplicates()