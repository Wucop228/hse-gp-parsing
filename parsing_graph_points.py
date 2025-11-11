import time
import json

import requests
from fake_useragent import UserAgent

ua = UserAgent()

with open(".proxies") as f:
    proxies = [None]
    for line in f:
        proxies.append(line)

with open("cstable.csv") as f:
    keys = f.readline().strip().split(',')
    items = []
    for line in f:
        arr = line.strip().split(',')
        item = {}
        for i in range(len(keys)):
            item[keys[i]] = arr[i]
        items.append(item)

def get_graph_points(url, proxy, headers):
    if proxy != None:
        res = requests.get(url, proxies={"http": proxy, "https": proxy}, headers=headers)
    else:
        res = requests.get(url, headers=headers)

    try:
        res.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"HTTP ошибка: {e}")
    print("ok")

    start = res.text.find("var line1")
    arr_str = res.text[start + len("var line1"):]

    end = arr_str.find("g_timePriceHistoryEarliest")
    arr_str = arr_str[:end]

    while arr_str[-1] != ']':
        arr_str = arr_str[:len(arr_str) - 1]
    while arr_str[0] != '[':
        arr_str = arr_str[1:]

    try:
        arr = json.loads(arr_str.strip().rstrip(","))
    except Exception as e:
        raise e


    return arr

curr = 0
while True:
    fake_ua = ua.random
    start = time.time()
    lst = []
    success = 0
    fail = 0
    for proxy in proxies:
        for i in range(25):
            url = f"https://steamcommunity.com/market/listings/730/{items[curr]['normalizedname']}"
            try:
                arr = get_graph_points(url, proxy=proxy, headers={"User-Agent": fake_ua})
                arr = [x for x in arr if "2025" in x[0] and ("Oct" in x[0] or "Nov" in x[0])]
                print(f"{curr}___{items[curr]['id']}___{len(arr)}")
                lst.append(f"{items[curr]['id']};{items[curr]['normalizedname']};{arr}" + "\n")
                success += 1
            except Exception as e:
                print(f"{curr}___{items[curr]['id']}___error:{e}")
                fail += 1
                break
            curr += 1
            if curr >= len(items): exit()
    with open("output_test.txt", "a") as f:
        for x in lst:
            f.write(x)
    end = time.time()
    diff = int(end - start)
    print(f"diff: {diff}, success: {success}, fail: {fail}")
    time.sleep(300)