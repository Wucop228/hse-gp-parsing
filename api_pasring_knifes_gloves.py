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
)
log = logging.getLogger("cs2_market")

url = f"https://www.steamwebapi.com/steam/api/items?key={API_KEY}&game=cs2&format=json"

safe_url = url.replace(API_KEY, "***") if API_KEY else url
log.info("GET %s", safe_url)

r = requests.get(url)

log.info("HTTP %s", r.status_code)

print("Статус:", r.status_code)
data = r.json()
print("Всего предметов:", len(data))
df = pd.DataFrame(data)

filtered = df[df["itemgroup"].isin(["knife", "gloves"])].copy()
print("Ножей и перчаток найдено:", len(filtered))
filtered = df[(df["itemgroup"].isin(["knife", "gloves"])) &(df["pricelatest"].notna()) &(df["pricelatest"] > 0)].copy()

print(filtered.columns.tolist())
cstable = filtered.to_csv('cstable.csv')

cols_keep = ["id","marketname","markethashname","itemgroup","itemtype","groupname","wear","isstattrak", "issouvenir","rarity","pricelatest","pricemedian24h","pricemedian7d","pricemedian30d","pricemedian90d","sold24h","sold7d","sold30d","sold90d","tag7"]
cols_present = [c for c in cols_keep if c in filtered.columns]
filtered_clean = filtered[cols_present].copy()
print("Столбцов осталось:", len(filtered_clean.columns))
filtered_clean.to_csv("cs2_knives_gloves_clean.csv", index=False)

log.info("Saved: cstable.csv, cs2_knives_gloves_clean.csv")
