import requests
import logging
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format="%(asctime)s | %(levelname)s | %(message)s",
    filename="api_parsing.log",
    encoding="utf-8",
)
log = logging.getLogger("cs2_market")

url = f"https://www.steamwebapi.com/steam/api/items?key={API_KEY}&game=cs2&format=json"

safe_url = url.replace(API_KEY, "***") if API_KEY else url
log.info("GET %s", safe_url)

try:
    r = requests.get(url, timeout=60)
    log.info("HTTP %s", r.status_code)
    r.raise_for_status()
except requests.RequestException:
    log.exception("Сетевая ошибка при запросе /steam/api/items")
    raise

try:
    data = r.json()
except ValueError:
    log.exception("Ошибка парсинга JSON")
    raise

log.info("Всего предметов: %d", len(data))
df = pd.DataFrame(data)

filtered = df[df["itemgroup"].isin(["knife", "gloves"])].copy()
log.info("Ножей и перчаток найдено (вкл. с нулевой ценой): %d", len(filtered))

filtered = df[(df["itemgroup"].isin(["knife", "gloves"])) &(df["pricelatest"].notna()) &(df["pricelatest"] > 0)].copy()
log.info("Ножей/перчаток с ценой > 0: %d", len(filtered))
log.debug("Колонки filtered: %s", filtered.columns.tolist())

filtered.to_csv('cstable.csv', index=False)

cols_keep = ["id","marketname","markethashname","itemgroup","itemtype","groupname","wear","isstattrak","issouvenir","rarity","pricelatest","pricemedian24h","pricemedian7d","pricemedian30d","pricemedian90d","sold24h","sold7d","sold30d","sold90d","tag7"]
cols_present = [c for c in cols_keep if c in filtered.columns]
filtered_clean = filtered[cols_present].copy()
log.info("Столбцов осталось: %d", len(filtered_clean.columns))

filtered_clean.to_csv("cs2_knives_gloves_clean.csv", index=False)
log.info("Saved: cstable.csv, cs2_knives_gloves_clean.csv")
