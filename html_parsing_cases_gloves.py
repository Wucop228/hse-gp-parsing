import requests
import time
from bs4 import BeautifulSoup
itog=[]
url = 'https://csmarketcap.com/weapons/all/gloves'
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html')
urls = []
for link in soup.find_all('a'):
    if ('gloves' in link.get('href') or 'hand-wraps' in link.get('href')) and '/item/' in link.get('href'):
        if link.get('href').count("/") == 2:
            urls.append(link.get('href'))
urls=list(set(urls))
for i in range(len(urls)):
    urli='https://csmarketcap.com'+urls[i]
    pagei = requests.get(urli)
    soupi = BeautifulSoup(pagei.text, 'html')
    case = []
    temp = soupi.find_all("p", {"class": "light"})
    for ii in range(len(temp)):
        case.append(temp[ii].text)
    case = list(set(case))
    name = soupi.find_all("h1", {"class": "skin-main--title f28"})[0].text
    itog.append((name, case))
    print(i, len(urls))
    time.sleep(0.3)
url = 'https://csmarketcap.com/weapons/all/gloves?page=2'
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html')
urls = []
for link in soup.find_all('a'):
    if ('gloves' in link.get('href') or 'hand-wraps' in link.get('href')) and '/item/' in link.get('href'):
        if link.get('href').count("/") == 2:
            urls.append(link.get('href'))
urls=list(set(urls))
for i in range(len(urls)):
    urli='https://csmarketcap.com'+urls[i]
    pagei = requests.get(urli)
    soupi = BeautifulSoup(pagei.text, 'html')
    case = []
    temp = soupi.find_all("p", {"class": "light"})
    for ii in range(len(temp)):
        case.append(temp[ii].text)
    case = list(set(case))
    name = soupi.find_all("h1", {"class": "skin-main--title f28"})[0].text
    itog.append((name, case))
    print(i, len(urls))
    time.sleep(0.3)
with open("output_gloves.txt", "a",encoding="utf-8") as f:
    for el in itog:
        f.write(f"{el[0]}{";"}{el[1]}\n")