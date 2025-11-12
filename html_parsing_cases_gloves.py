import requests
import time
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO, filename="html_parsing_cases_gloves_log.log",
                    filemode="w", format="%(asctime)s %(levelname)s %(message)s")
logging.info("Running gloves scraper")
GlovesAndCases = []

complete_proc = 0
kol_inf = 0
processed_count = 0

pages_to_scrape = ['https://csmarketcap.com/weapons/all/gloves','https://csmarketcap.com/weapons/all/gloves?page=2']
logging.info(f"Total pages to process: {len(pages_to_scrape)}")

logging.info("Calculating total number of gloves to process")
for page_url in pages_to_scrape:
    logging.info(f"Loading page: {page_url}")
    try:
        page = requests.get(page_url, timeout=10)
        page.raise_for_status()
    except requests.RequestException as err:
        logging.error(f"Failed to load {page_url}: {err}")
        continue
    logging.info("Successfully loaded")
    soup = BeautifulSoup(page.text, 'html.parser')
    urls = []

    for link in soup.find_all('a'):
        href = link.get('href')
        if href and '/item/' in href and ('gloves' in href or 'hand-wraps' in href):
            if href.count("/") == 2:
                urls.append(href)
    urls = list(set(urls))
    kol_inf += len(urls)
    logging.info(f"Found {len(urls)} gloves on this page")
logging.info(f"Total gloves to process: {kol_inf}")

for page_index in range(len(pages_to_scrape)):
    page_number = page_index + 1
    page_url = pages_to_scrape[page_index]
    logging.info(f"Processing page {page_number}/{len(pages_to_scrape)}: {page_url}")

    try:
        page = requests.get(page_url, timeout=10)
        page.raise_for_status()
    except requests.RequestException as err:
        logging.error(f"Failed to load {page_url}: {err}")
        continue
    logging.info("Successfully loaded")
    soup = BeautifulSoup(page.text, 'html.parser')
    urls = []

    for link in soup.find_all('a'):
        href = link.get('href')
        if href and ('gloves' in href or 'hand-wraps' in href) and '/item/' in href:
            if href.count("/") == 2:
                urls.append(href)
    urls = list(set(urls))
    logging.info(f"Found {len(urls)} gloves on page {page_number}")

    for url_index in range(len(urls)):
        urli = 'https://csmarketcap.com' + urls[url_index]
        logging.info(f"Loading glove page: {urli}")
        try:
            pagei = requests.get(urli, timeout=10)
            pagei.raise_for_status()
        except requests.RequestException as err:
            logging.error(f"Failed to load glove {urli}: {err}")
            continue
        logging.info("Successfully loaded")
        soupi = BeautifulSoup(pagei.text, 'html.parser')

        case = []
        temp = soupi.find_all("p", {"class": "light"})
        for ii in range(len(temp)):
            case.append(temp[ii].text)
        case = list(set(case))
        name_element = soupi.find_all("h1", {"class": "skin-main--title f28"})
        if not name_element:
            logging.warning(f"No glove name found for {urli}")
            continue
        name = name_element[0].text
        GlovesAndCases.append((name, case))
        logging.debug(f"Processed: {name}")

        processed_count += 1
        progress = round(processed_count * 100 / kol_inf, 2)
        print(f"\r{progress} %", end="")
        time.sleep(0.3)

    complete_proc = round(processed_count * 100 / kol_inf, 2)
    logging.info(f"Progress: {complete_proc}%")

logging.info(f"Saving {len(GlovesAndCases)} items to file")
try:
    with open("output_gloves.txt", "w", encoding="utf-8") as f:
        for el in GlovesAndCases:
            f.write(f"{el[0]};{el[1]}\n")
    logging.info("File saved successfully")
except Exception as err:
    logging.error(f"Error saving to file: {err}")
logging.info("Script finished")