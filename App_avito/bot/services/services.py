from parser.start_parser import get_json
from parser.parser import StartBrowser
from bot.lexicon import CITY_EN, PRICE




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

