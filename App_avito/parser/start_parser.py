from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from fake_useragent import UserAgent
from datetime import datetime
from selectolax.parser import HTMLParser
from urllib.parse import unquote
from bd import id_llist
from bot.database.database import SqLiteClient, Offer

import json
import sqlite3 as sq

dict_offer = {}
SITE = "https://www.avito.ru"
URL = "https://www.avito.ru/moskva/kvartiry/sdam/na_dlitelnyy_srok-ASgBAgICAkSSA8gQ8AeQUg"
PATH_BD = r"C:\Users\79991\PycharmProjects\App_avito\bot\database\Avito.db"


def start_browser():
    """Запуск драйвера Селeниум"""
    useragent = UserAgent()
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-agent={useragent.random}")
    options.add_argument("--disable-blink-features=AutomationControlled")  # Отключение режима веб-драйвера
    # options.add_argument('headless')  # Отключение фонового режима
    s = Service(r"C:\Users\79991\PycharmProjects\App_avito\parser_avito\driver\chromedriver.exe")
    browser = webdriver.Chrome(service=s, options=options)
    browser.implicitly_wait(1200)
    browser.maximize_window()
    return browser


def get_json(city: str, user_id: int):
    """Получение Json данных"""
    URL = f"https://www.avito.ru/{city}/kvartiry/sdam/na_dlitelnyy_srok-ASgBAgICAkSSA8gQ8AeQUg"
    try:
        with start_browser() as browser:
            print(f"###[INFO]### Запись")
            browser.get(url=URL)
            html = browser.page_source
            tree = HTMLParser(html)
            scripts = tree.css("script")
            for script in scripts:
                if "window.__initialData__" in script.text():
                    json_text = script.text().split(";")[0].split("=")[-1].strip()
                    json_text = unquote(json_text)
                    json_text = json_text[1:-1]
                    data = json.loads(json_text)
                    get_json_item(data, user_id)

        return dict_offer

    except Exception as Ex:
        print("Ошибка при получение страниц")
        print(Ex)


def append_data_dict(item: dict) -> None:
    """Добавление данных в словарь"""
    try:
        date = datetime.fromtimestamp(item["sortTimeStamp"] / 1000).strftime("%d.%m.%Y в %H:%M")
        title = item["title"]
        price = item["priceDetailed"]["value"]
        address = item['geo']["formattedAddress"]
        url = f'{SITE}{item["urlPath"]}'
        dict_offer[item["id"]] = [title, price, address, url, date]

    except Exception as Ex:
        print(Ex)
        print("Ошибка добавление данных")


def get_data(item: dict) -> tuple:
    """Получение из json данных ID, цены, url, заголовок, адрес и дату"""
    try:
        offer_id = item["id"]
        price = item["priceDetailed"]["value"]
        title = item["title"]
        url = f'{SITE}{item["urlPath"]}'
        address = item['geo']["formattedAddress"]
        date = datetime.fromtimestamp(item["sortTimeStamp"] / 1000).strftime("%d.%m.%Y в %H:%M")
        return (offer_id, title, price, address, url, date)

        # offer = {}
        # offer["offer_id"] = item["id"]
        # offer["price"] = item["priceDetailed"]["value"]
        # offer["title"] = item["title"]
        # offer["url"] = f'{SITE}{item["urlPath"]}'
        # offer["address"] = item['geo']["formattedAddress"]
        # offer["date"] = datetime.fromtimestamp(item["sortTimeStamp"] / 1000).strftime("%d.%m.%Y в %H:%M")
        # return offer

    except Exception as Ex:
        print(Ex)
        print("Ошибка получение данных")


def check_database(item: dict, user_id: int) -> None:
    """Проверка ID offer в БД и запись данных"""
    try:
        offer_id = item["id"]
        database = Offer(database_client=SqLiteClient(PATH_BD))
        database.setup()
        data_offer = database.check_id_offer(offer_id=offer_id, user_id=user_id)
        if isinstance(data_offer, tuple):
            offer = get_data(item) + data_offer
            database.insert_offer(offer=offer)
            append_data_dict(item=item)
            print(f"Запись {offer_id} у пользователя {user_id} добавлена в БД")

    except Exception as Ex:
        print(f"Ошибка при записи {offer_id} c пользователем {user_id} в БД ### {Ex}")

    finally:
        database.shutdown()


def get_json_item(data: dict, user_id: int) -> None:
    """Получение json словаря и item(ID)"""
    try:
        for key in data:
            if "single-page" in key:
                items = data[key]["data"]["catalog"]["items"]
                for item in items:
                    if item.get("id"):
                        check_database(item, user_id)

    except Exception as Ex:
        print("Ошибка при получение item")
        print(Ex)


def main():
    """Основной запуск программы"""
    start_time = datetime.now()
    get_json(city="moskva")
    print(f"####################### TOTAL {datetime.now() - start_time}")


if __name__ == '__main__':
    main()
