# hse-gp-parsing

Небольшой набор скриптов для парсинга данных по кейсам **CS2** (ножи и перчатки) и подготовки данных для последующего анализа/визуализации.

## Что здесь есть
- `html_parsing_cases_knifes.py` — HTML парсер кейсов с **ножами**.
- `html_parsing_cases_gloves.py` — HTML парсер кейсов с **перчатками**.
- `api_pasring_knifes_gloves.py` — сбор данных по ножам/перчаткам через Steam Web API.
- `parsing_graph_points.py` — сбор данных о цене и количества продаж у всех ножей/перчаток для анализа графика.

# `parsing_graph_points.py`
Делаю запрос к каждому скину и получаю html страничку. Там данные о всех точках графика находится в js скрипте. Достаю из строчки нужный массив и загружаю его в python массив
## Использовал
- requests
- fake_useragent
- logging
- json
- time

# `api_pasring_knifes_gloves.py`
Задача: собрать данные по ножам и перчаткам через Steam Web API и очистить для анализа.

Алгоритм:
 1. Получаю API-токен из .env.
 2. Формирую запрос к Steam Web API (CS2 items).
 3. Делаю GET-запрос → получаю JSON.
 4. Преобразую в pandas.DataFrame.
 5. Фильтрую только ножи и перчатки.
 6. Убираю пустые и нулевые цены.
 7. Выбираю ключевые признаки.
 8. Сохраняю результат в cs2_knives_gloves_clean.csv.
 9. Логирую все шаги в api_parsing.log

Признаки:

marketname - название
itemgroup - группа (нож/перчатки)
wear - износ
isstattrak, issouvenir - тип предмета
pricelatest, pricemedian* - цены
sold* - объёмы продаж
rarity, itemtype, groupname- редкость и тип

Использовал:

requests, pandas, dotenv, logging, json

#Ссылки на графики
- https://colab.research.google.com/drive/1YrPk3OLkztesWGe18-co5CdTmVJ7nkdH?usp=sharing