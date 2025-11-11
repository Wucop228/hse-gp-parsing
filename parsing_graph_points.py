import time
import json
import logging

import requests
from fake_useragent import UserAgent

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s: %(message)s",
    datefmt="%H:%M:%S",
    filename="graph_points.log",
    encoding="utf-8"
)

ua = UserAgent()
logger = logging.getLogger(__name__)

proxies = [None]
logger.debug("Достаю все proxy из файла .proxies")
try:
    with open(".proxies") as f:
        for line in f:
            proxies.append(line)
except Exception as e:
    logger.error("Ошибка при извлечении данных файла .proxies: error=%s", e)
else:
    logger.info("Успешно достал все proxy из файла .proxies")

items = []
logger.debug("Достаю из файла cstable.csv все данные")
try:
    with open("cstable.csv") as f:
        keys = f.readline().strip().split(',')
        for line in f:
            arr = line.strip().split(',')
            item = {}
            for i in range(len(keys)):
                item[keys[i]] = arr[i]
            items.append(item)
except Exception as e:
    logger.error("Ошибка при извлечении данных файла cstable.csv: error=%s", e)
else:
    logger.info("Успешно достал все данные из файла cstable.csv")

def get_graph_points(url, proxy, headers, ip):
    logger.debug("Пытаюсь запарсить ссылку: url=%s, proxy=%s", url, ip)
    try:
        if proxy != None:
            res = requests.get(url, proxies={"http": proxy, "https": proxy}, headers=headers)
        else:
            res = requests.get(url, headers=headers)
    except Exception as e:
        logger.error("Ошибка при парсинге: error=%s", e)
        return
    else:
        logger.info("Успешно запарсил ссылку: url=%s, proxy=%s", url, ip)

    logger.debug("Проверяю запрос на ошибки: url=%s, proxy=%s", url, ip)
    try:
        res.raise_for_status()
    except requests.exceptions.HTTPError as e:
        logger.exception("Ответ вернулся с ошибкой: error=%s", e)
        return
    else:
        logger.info("Запрос успешно выполнен: url=%s, proxy=%s", url, ip)

    start = res.text.find("var line1")
    arr_str = res.text[start + len("var line1"):]

    end = arr_str.find("g_timePriceHistoryEarliest")
    arr_str = arr_str[:end]

    while arr_str[-1] != ']':
        arr_str = arr_str[:len(arr_str) - 1]
    while arr_str[0] != '[':
        arr_str = arr_str[1:]

    logger.debug("Пытаюсь преобразовать строку в массив: arr_str_len=%s", len(arr_str))
    try:
        arr = json.loads(arr_str.strip().rstrip(","))
    except Exception as e:
        logger.error("Ошибка при преобразовании строки в массив: error=%s", e)
        return
    else:
        logger.info("Успешно строчка преобразована в массив: arr_len=%s", len(arr))

    return arr

curr = 0
while True:
    fake_ua = ua.random
    start = time.time()
    lst = []
    success = 0
    failed = 0
    for proxy in proxies:
        if proxy != None:proxy = proxy.strip()
        ip = "-"
        if proxy != None:
            ip = proxy.split("@")[1]
        for i in range(25):
            url = f"https://steamcommunity.com/market/listings/730/{items[curr]['normalizedname']}"
            try:
                arr = get_graph_points(url, proxy=proxy, headers={"User-Agent": fake_ua}, ip=ip)
                if arr == []: break
                arr = [x for x in arr if "2025" in x[0] and ("Oct" in x[0] or "Nov" in x[0])]
                lst.append(f"{items[curr]['id']};{items[curr]['normalizedname']};{arr}" + "\n")
                success += 1
            except Exception as e:
                logger.error("Ошибка при обработке запроса: curr=%s, url=%s, proxy=%s, item_id=%s, error=%s",
                             curr, url, ip, items[curr]['id'], e)
                failed += 1
                break
            else:
                logger.info("Успешно обработан запрос: curr=%s, url=%s, proxy=%s, item_id=%s, arr_len=%s",
                            curr, url, ip, items[curr]['id'], len(arr))
            curr += 1
            if curr >= len(items): exit()

    logger.debug("Записываю в файл output.txt данные: lst_len=%s", len(lst))
    try:
        with open("output.txt", "a") as f:
            for x in lst:
                f.write(x)
    except Exception as e:
        logger.error("Ошибка при записи в файл output.txt данные: lst_len=%s, error=%s",len(lst), e)
    else:
        logger.info("Успешно записано в файл output.txt данные: lst_len=%s", len(lst))

    end = time.time()
    diff = int(end - start)
    logger.info("Предметы обработаны: diff=%s, success=%s, failed=%s", diff, success, failed)
    time.sleep(300)