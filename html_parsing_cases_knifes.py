import requests
import time
from bs4 import BeautifulSoup
itog=[]
url = 'https://csmarketcap.com'
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html')
urls = []
for link in soup.find_all('a'):
    if 'weapons' in link.get('href') and ('knife' in link.get('href') or 'knife' in link.get('href')
                                          or 'bayonet' in link.get('href') or 'karambit' in link.get('href')
                                          or 'm9-bayonet' in link.get('href')
                                          or 'shadow-daggers' in link.get('href')):
        urls.append(link.get('href'))
urls=list(set(urls))
for i in range(len(urls)):
    print("--------", i+1, len(urls))
    urli = "https://csmarketcap.com"+urls[i]
    pagei = requests.get(urli)
    soupi = BeautifulSoup(pagei.text, 'html')
    urlsi=[]
    for link0 in soupi.find_all('a'):
        if "item/"+str(urls[i].split("/")[2]) in link0.get('href'):
            if link0.get('href').count("/")==2:
                urlsi.append(link0.get('href'))
    urlsi=list(set(urlsi))
    for ii in range(len(urlsi)):
        urlii = "https://csmarketcap.com"+urlsi[ii]
        pageii = requests.get(urlii)
        soupii = BeautifulSoup(pageii.text, 'html')
        case=[]
        temp=soupii.find_all("p",{"class" : "light"})
        for iii in range(len(temp)):
            case.append(temp[iii].text)
        case=list(set(case))
        name=soupii.find_all("h1",{"class" : "skin-main--title f28"})[0].text
        itog.append((name, case))
        time.sleep(0.3)
        print('\r\033[k',end="")
        print(ii+1,len(urlsi),end='')
    print('\033c', end="")
with open("output_knife.txt", "a",encoding="utf-8") as f:
    for el in itog:
        f.write(f"{el[0]}{";"}{el[1]}\n")