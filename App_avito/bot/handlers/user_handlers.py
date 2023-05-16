from aiogram import Router, F
from aiogram.filters import Command, CommandStart, Text
from aiogram.types import Message, CallbackQuery
from bot.keyboards import city_kb, start_kb, kategory_kb, flat_long_button, price_panel
from bot.lexicon import LEXICON_RU, CITY_EN, PRICE
from bot.services import get_data, translation_price
from bot.database.database import User, SqLiteClient

router: Router = Router()
list_city: list = []
list_category: list = []
PATH_BD = "/home/nikita/PycharmProjects/Parser_bot/App_avito/bot/database/Avito.db"
database = User(SqLiteClient(PATH_BD))


# Этот хэндлер срабатывает на команду /start
@router.message(CommandStart())
async def process_start_command(message: Message) -> None:
    user_id = message.from_user.id
    username = message.from_user.username
    chat_id = message.chat.id
    database.setup()
    user = database.get_user(user_id=user_id)
    list_city.clear()
    if not user:
        database.create_user(user_id=user_id, username=username, chat_id=chat_id)
    database.shutdown()
    await message.answer(text=LEXICON_RU['/start'], reply_markup=start_kb)




# Этот хэндлер срабатывает на команду /help
@router.message(Command(commands=['help']))
@router.message(Text(text=['help_button']))
async def process_help_command(message: Message) -> None:
    await message.answer(text=LEXICON_RU['/help'])


# Этот хэндлер для смены города
@router.message(Command(commands=['gorod']))
async def process_help_command(message: Message) -> None:
    list_city.clear()
    await message.answer(text='Выберите город', reply_markup=city_kb)

# Этот хэндлер для выбора категории
@router.callback_query(Text(text=['parsing_button']))
async def category_command(callback: CallbackQuery) -> None:
    await callback.message.answer(text='Выберите категорию парсинга', reply_markup=kategory_kb)



@router.callback_query(Text(text=['flat_long_button',
                                  'flat_short_button',
                                  'buy_flat_button']))
async def city_selection(callback: CallbackQuery) -> None:
    category = callback.data
    list_category.append(category)
    await callback.message.answer(text='Выберите город', reply_markup=city_kb)


@router.message(Text(text=[CITY_EN['moskva'],
                           CITY_EN["sankt-peterburg"],
                           CITY_EN['perm'],
                           CITY_EN['ufa'],
                           CITY_EN['sochi'],
                           CITY_EN['ekaterinburg']]))
async def price_button(message: Message) -> None:
    price_category = price_panel(list_category[-1])
    await message.answer(text="Выберите ваш бюджет для снятие квартиры", reply_markup=price_category)
    data_city = message.text
    list_city.append(data_city)


@router.message(Text(text=[PRICE["0-2000"], PRICE["2000-5000"], PRICE["5000-100000"],
                           PRICE["0-10000"], PRICE["10000-20000"], PRICE["20000-50000"],
                           PRICE["50000-500000"], PRICE["1000000-3000000"], PRICE["3000000-10000000"],
                           PRICE["10000000-500000000"], PRICE["500000000-1000000000"]]))
async def process_parsing(message: Message) -> None:
    await message.answer(text="Ожидайте, пожалуйста...")
    user_id = message.from_user.id
    price_user = message.text
    range_price_list = translation_price(price=price_user)
    dict_offer = get_data(city=list_city[-1], category=list_category[-1], user_id=user_id, price=range_price_list)
    count = 0
    for key, value in dict_offer.items():
        title, price, address, url, date = value
        title = title.split(",")
        text = (f"<b>Количество комнат:</b> {title[0]}\n"
                f"<b>Площадь:</b> {title[1]}\n"
                f"<b>Этаж:</b> {title[2]}\n"
                f"<b>Цена:</b> {price} руб\n"
                f"<b>Ссылка:</b> <a href='{url}'>{' '.join(title)}</a>\n"
                f"<b>Адрес:</b> {address}\n"
                f"<b>Дата публикации:</b> {date}")
        count += 1
        await message.answer(text=text)

    if not count:
        text = "Объявлений нету!"
        await message.answer(text=text)

    await message.answer(text="Готово, чтоб продолжить, выбери другую цену "
                              "или нажмите /gorod для смены города")

