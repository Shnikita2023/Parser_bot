import json

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
from datetime import datetime
from selectolax.parser import HTMLParser
from urllib.parse import unquote
from app.bot.database.database import Offer, Database
from loguru import logger

from app.bot.lexicon.lexicon_ru import CATEGORY

LINK = "https://www.avito.ru"
logger.add(sink="parser.log", format="{time} {level} {message}", level="DEBUG", mode="w")


class StartBrowser:
    """Запуск драйвера Селeниум"""
    logger.info('Starting pars')
    useragent = UserAgent()
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-agent={useragent.random}")
    options.add_argument("--disable-blink-features=AutomationControlled")  # Отключение режима веб-драйвера
    options.add_argument('headless')  # Отключение фонового режима
    service = ChromeService(ChromeDriverManager().install())  # путь до драйвера

    def __init__(self, city: str, user_id: int, range_price_list: list[int], category: str) -> None:
        self.city = city
        self.user_id = user_id
        self.range_price_list = range_price_list
        self.category = category
        self.dict_offer = {}
        self.browser = webdriver.Chrome(service=self.service, options=self.options)
        self.browser.implicitly_wait(120)
        self.browser.maximize_window()

    def get_json(self) -> dict:
        """Получение Json данных"""
        category_offer = CATEGORY[self.category]
        URL = f"{LINK}/{self.city}{category_offer}"
        try:
            with self.browser as browser:
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
                        self.get_json_item(data, self.user_id)
                        break
            return self.dict_offer

        except Exception as Ex:
            logger.exception("Ошибка получение json данных")

    def get_json_item(self, data: dict, user_id: int) -> None:
        """Получение json словаря и item(ID)"""
        try:
            for key in data:
                if "single-page" in key:
                    items = data[key]["data"]["catalog"]["items"]
                    for item in items:
                        if item.get("id"):
                            self.check_database(item=item, user_id=user_id)

        except Exception as Ex:
            logger.exception("Ошибка получение item данных")

    def check_database(self, item: dict, user_id: int) -> None:
        """Проверка ID offer в БД и запись данных"""
        try:
            offer_id = item["id"]
            database = Offer(database_client=Database())
            database.setup()
            data_offer = database.check_id_offer(self.range_price_list, offer_id=offer_id, user_id=user_id)
            if isinstance(data_offer, tuple):
                offer = self.get_data(item)
                if offer:
                    offer += data_offer
                    logger.info(offer)
                    database.insert_offer(offer=offer)
                    logger.info(f"Запись {offer_id} у пользователя {user_id} добавлена в БД")

        except Exception as Ex:
            logger.exception(f"Ошибка при записи {offer_id} c пользователем {user_id} в БД ### {Ex}")

        finally:
            database.shutdown()

    def get_data(self, item: dict) -> tuple | None:
        """Получение из json данных ID, цены, url, заголовок, адрес и дату и добавление в словарь"""
        try:
            offer_id = item["id"]
            price = item["priceDetailed"]["value"]
            title = item["title"]
            url = f'{LINK}{item["urlPath"]}'
            address = item['geo']["formattedAddress"]
            date = datetime.fromtimestamp(item["sortTimeStamp"] / 1000).strftime("%d.%m.%Y в %H:%M")
            if self.check_price(price):
                self.dict_offer[item["id"]] = [title, price, address, url, date]
                return offer_id, title, price, address, url, date

        except Exception as Ex:
            logger.exception("Ошибка получение данных(id, url, цены и т.д)")

    def check_price(self, price: int) -> bool:
        """Проверка с ценой пользователя и объявлениeм"""
        price_min, price_max = self.range_price_list
        return price_min <= price <= price_max

