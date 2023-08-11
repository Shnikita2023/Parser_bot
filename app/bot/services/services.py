from ..lexicon.lexicon_ru import CITY_EN, PRICE
from app.parser.parser import StartBrowser


def get_data(city: str, category: str, user_id: int, price: list[int]) -> dict:
    list_value = list(CITY_EN.values())
    list_key = list(CITY_EN.keys())
    position = list_value.index(city)
    city = list_key[position]
    offer = StartBrowser(city=city, user_id=user_id, range_price_list=price, category=category).get_json()
    return offer


def translation_price(price: str) -> list[int]:
    for key, value in PRICE.items():
        if value == price:
            return list(map(int, key.split("-")))


def transfer_text_telegram(value: str) -> str:
    title, price, address, url, date = value
    title = title.split(",")
    text = (f"<b>Количество комнат:</b> {title[0]}\n"
            f"<b>Площадь:</b> {title[1]}\n"
            f"<b>Этаж:</b> {title[2]}\n"
            f"<b>Цена:</b> {price} руб\n"
            f"<b>Ссылка:</b> <a href='{url}'>{' '.join(title)}</a>\n"
            f"<b>Адрес:</b> {address}\n"
            f"<b>Дата публикации:</b> {date}")
    return text
