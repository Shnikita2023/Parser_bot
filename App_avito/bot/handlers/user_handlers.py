from aiogram import Router, F
from aiogram.filters import Command, CommandStart, Text
from aiogram.types import Message, CallbackQuery
from bot.keyboards import city_kb, price_kb, start_kb, kategory_kb
from bot.lexicon import LEXICON_RU, CITY_EN, PRICE
from bot.services import get_data, translation_price
from bot.database.database import User, SqLiteClient

router: Router = Router()
list_city: list = []
list_category: list = []
PATH_BD = r"C:\Users\79991\PycharmProjects\App_avito\bot\database\Avito.db"
database = User(SqLiteClient(PATH_BD))


# Этот хэндлер срабатывает на команду /start
@router.message(CommandStart())
async def process_start_command(message: Message) -> None:
    user_id = message.from_user.id
    username = message.from_user.username
    chat_id = message.chat.id
    database.setup()
    user = database.get_user(user_id=user_id)
    if not user:
        database.create_user(user_id=user_id, username=username, chat_id=chat_id)
    if list_city:
        list_city.clear()
    database.shutdown()
    await message.answer(text=LEXICON_RU['/start'], reply_markup=start_kb)


# Этот хэндлер срабатывает на команду /help
@router.message(Command(commands=['help']))
async def process_help_command(message: Message) -> None:
    await message.answer(text=LEXICON_RU['/help'], reply_markup=city_kb)


@router.callback_query(Text(text=['parsing_button']))
async def process_buttons_command(callback: CallbackQuery):
    await callback.message.answer(text='Выберите категорию парсинга', reply_markup=kategory_kb)


@router.callback_query(Text(text=['flat_long_button']))
@router.callback_query(Text(text=['flat_short_button']))
@router.callback_query(Text(text=['buy_flat_button']))
@router.callback_query(Text(text=['buy_car']))
async def process_buttons_command(callback: CallbackQuery):
    await callback.message.answer(text='Выберите город', reply_markup=city_kb)


@router.message(Text(text=[CITY_EN['moskva'],
                           CITY_EN["sankt-peterburg"],
                           CITY_EN['perm'],
                           CITY_EN['ufa'],
                           CITY_EN['sochi'],
                           CITY_EN['ekaterinburg']]))
async def city_button(message: Message) -> None:
    await message.answer(text="Выберите ваш бюджет для снятие квартиры", reply_markup=price_kb)
    data_city = message.text
    list_city.append(data_city)


@router.message(Text(text=[PRICE["0-10000"],
                           PRICE["10000-20000"],
                           PRICE["20000-50000"],
                           PRICE["50000-500000"]]))
async def price_button(message: Message) -> None:
    await message.answer(text="Ожидайте, пожалуйста...", reply_markup=price_kb)
    user_id = message.from_user.id
    price_user = message.text
    price_min, price_max = translation_price(price=price_user)
    dict_offer = get_data(city=list_city[0], user_id=user_id)
    count = 0
    for key, value in dict_offer.items():
        title, price, address, url, date = value
        title = title.split(",")
        if price_min <= price <= price_max:
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
                              "или нажмите /start для смены города")
    dict_offer.clear()
