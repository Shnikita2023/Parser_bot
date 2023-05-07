from parser.start_parser import get_json
from bot.lexicon import CITY_EN, PRICE




def get_data(city: str, user_id: int) -> dict:
    list_value = list(CITY_EN.values())
    list_key = list(CITY_EN.keys())
    position = list_value.index(city)
    city = list_key[position]
    offer = get_json(city=city, user_id=user_id)
    return offer


def translation_price(price: str) -> list[int, int]:
    for key, value in PRICE.items():
        if value == price:
            return list(map(int, key.split("-")))

