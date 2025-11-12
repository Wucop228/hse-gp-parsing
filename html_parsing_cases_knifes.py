# Import libraries
import requests
import time
from bs4 import BeautifulSoup
import logging
# Logging to file
logging.basicConfig(level=logging.INFO, filename="html_parsing_cases_knifes_log.log",
                    filemode="w",format="%(asctime)s %(levelname)s %(message)s")

logging.info("running knife scraper")
# We create an array that will contain the final result
KnifesAndCases=[]
# Search and save links to all types of knives """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
url_main_website = 'https://csmarketcap.com'
logging.info(f"Loading the main website: {url_main_website}")
try:
    page_main_website = requests.get(url_main_website, timeout=10)
    page_main_website.raise_for_status()
except requests.RequestException as err:
    logging.error(f"Failed to fetch main page: {err}")
    exit(1)
logging.info("successfully")
soup_main_website = BeautifulSoup(page_main_website.text, 'html.parser')
urlS_main_website = []
for link in soup_main_website.find_all('a'):
    if 'weapons' in link.get('href') and ('knife' in link.get('href') or 'knife' in link.get('href')
                                          or 'bayonet' in link.get('href') or 'karambit' in link.get('href')
                                          or 'm9-bayonet' in link.get('href')
                                          or 'shadow-daggers' in link.get('href')):
        urlS_main_website.append(link.get('href'))
urlS_main_website=list(set(urlS_main_website))
logging.info(f"Found {len(urlS_main_website)} knife types: {urlS_main_website}")
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Variables for displaying percentages ---------------------------------------------------------------------------------
complete_proc=0
tec_kol_inf=0
kol_inf=0
# To display percentages. Calculate the amount of information
logging.info("Calculating total number of skins to process")
for LinkNumber_urlS_main_website in range(len(urlS_main_website)):
    url_subsite_main_website = "https://csmarketcap.com"+urlS_main_website[LinkNumber_urlS_main_website]
    logging.info(f"Loading the subsite main website: {url_subsite_main_website}")
    try:
        page_subsite_main_website = requests.get(url_subsite_main_website, timeout=10)
        page_subsite_main_website.raise_for_status()
    except requests.RequestException as err:
        logging.error(f"Failed to load {url_subsite_main_website}: {err}")
        continue
    logging.info("successfully")
    soup_subsite_main_website = BeautifulSoup(page_subsite_main_website.text, 'html.parser')
    urlS_subsite_main_website=[]
    for link0 in soup_subsite_main_website.find_all('a'):
        if "item/"+str(urlS_main_website[LinkNumber_urlS_main_website].split("/")[2]) in link0.get('href'):
            if link0.get('href').count("/")==2:
                urlS_subsite_main_website.append(link0.get('href'))
    urlS_subsite_main_website = list(set(urlS_subsite_main_website))
    kol_inf=kol_inf+len(urlS_subsite_main_website)
logging.info(f"Total skins to process: {kol_inf}")
# ----------------------------------------------------------------------------------------------------------------------
# Go to the website for a specific knife and save links to all types of skins """"""""""""""""""""""""""""""""""""""""""
for LinkNumber_urlS_main_website in range(len(urlS_main_website)):
    logging.info(f"Processing knife {LinkNumber_urlS_main_website + 1}/{len(urlS_main_website)}: {urlS_main_website[LinkNumber_urlS_main_website]}")
    url_subsite_main_website = "https://csmarketcap.com"+urlS_main_website[LinkNumber_urlS_main_website]
    logging.info(f"Loading the subsite main website: {url_subsite_main_website}")
    try:
        page_subsite_main_website = requests.get(url_subsite_main_website, timeout=10)
        page_subsite_main_website.raise_for_status()
    except requests.RequestException as err:
        logging.error(f"Failed to load {url_subsite_main_website}: {err}")
        continue
    logging.info("successfully")
    soup_subsite_main_website = BeautifulSoup(page_subsite_main_website.text, 'html.parser')
    urlS_subsite_main_website=[]
    for link0 in soup_subsite_main_website.find_all('a'):
        if "item/"+str(urlS_main_website[LinkNumber_urlS_main_website].split("/")[2]) in link0.get('href'):
            if link0.get('href').count("/")==2:
                urlS_subsite_main_website.append(link0.get('href'))
    urlS_subsite_main_website=list(set(urlS_subsite_main_website))
    logging.info(f"Found {len(urlS_subsite_main_website)} skins for this knife")
# Go to the website for a specific knife and a specific skin, read the name of the skin and the cases it is in.
    for LinkNumber_urlS_subsite_main_website in range(len(urlS_subsite_main_website)):
        tec_kol_inf=LinkNumber_urlS_subsite_main_website
        urlS_SubSubsite_main_website = "https://csmarketcap.com"+urlS_subsite_main_website[LinkNumber_urlS_subsite_main_website]
        logging.info(f"Loading the subsubsite main website: {urlS_SubSubsite_main_website}")
        try:
            page_SubSubsite_main_website = requests.get(urlS_SubSubsite_main_website, timeout=10)
            page_SubSubsite_main_website.raise_for_status()
        except requests.RequestException as err:
            logging.error(f"Failed to load skin {urlS_SubSubsite_main_website}: {err}")
            continue
        logging.info("successfully")
        soup_SubSubsite_main_website = BeautifulSoup(page_SubSubsite_main_website.text, 'html.parser')
        cases_skin=[]
        all_cases=soup_SubSubsite_main_website.find_all("p",{"class" : "light"})
        for number_all_cases in range(len(all_cases)):
            cases_skin.append(all_cases[number_all_cases].text)
        cases_skin=list(set(cases_skin))
        name_skin=soup_SubSubsite_main_website.find_all("h1",{"class" : "skin-main--title f28"})[0].text
        KnifesAndCases.append((name_skin, cases_skin))
        logging.debug(f"Processed: {name_skin}")
        time.sleep(0.3)
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#Output of interest and preservation of previous interest---------------------------------------------------------------
        print(f"\r{round(complete_proc + (tec_kol_inf + 1) * (100 / kol_inf), 2)} %", end="")
    complete_proc= complete_proc + (tec_kol_inf + 1) * (100 / kol_inf)
    logging.info(f"Progress: {round(complete_proc, 2)}%")
#-----------------------------------------------------------------------------------------------------------------------
#Adding the obtained result to the file'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
logging.info(f"Saving {len(KnifesAndCases)} items to file")
with open("output_knife.txt", "w",encoding="utf-8") as f:
    for el in KnifesAndCases:
        f.write(f"{el[0]};{el[1]}\n")
logging.info("File saved successfully")
logging.info("Script finished")
#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''