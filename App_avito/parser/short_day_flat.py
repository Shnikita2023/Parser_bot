from fake_useragent import UserAgent
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
from datetime import datetime
from bs4 import BeautifulSoup
from selectolax.parser import HTMLParser
from urllib.parse import unquote
from bd import id_llist
import json


dict_offer = {}
SITE = "https://www.avito.ru"


def start_browser():
    """Запуск драйвера Селeниум"""
    useragent = UserAgent()
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-agent={useragent.random}")
    options.add_argument("--disable-blink-features=AutomationControlled")  # Отключение режима веб-драйвера
    # options.add_argument('headless')  # Отключение фонового режима
    s = Service(r"C:\Users\79991\PycharmProjects\App_avito\parser_avito\driver\chromedriver.exe")
    browser = webdriver.Chrome(service=s, options=options)
    browser.implicitly_wait(60)
    browser.maximize_window()
    return browser


def get_url_car():
    try:
        URL = "https://www.avito.ru/moskva/kvartiry/sdam/posutochno/-ASgBAgICAkSSA8gQ8AeSUg?cd=1&s=104"
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
                    get_json_item(data)
                    break

    except Exception:
        print("Ошибка")

def get_json_item(data: dict) -> None:
    """Получение json словаря и item(ID)"""
    try:
        for key in data:
            if "single-page" in key:
                items = data[key]["data"]["catalog"]["items"]
                for item in items:
                    if item.get("id"):
                        append_data_dict(item)


    except Exception as Ex:
        print("Ошибка при получение item")
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


def main():
    """Основной запуск программы"""
    start_time = datetime.now()
    get_url_car()
    with open("2.json", "w", encoding="utf-8") as file:
        json.dump(dict_offer, file, ensure_ascii=False, indent=4)
    print(f"####################### TOTAL {datetime.now() - start_time}")


if __name__ == '__main__':
    main()
