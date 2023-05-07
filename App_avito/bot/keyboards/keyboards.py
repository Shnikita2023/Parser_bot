from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from bot.lexicon import CITY_EN, PRICE
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

# ------- Создаем клавиатуру через ReplyKeyboardBuilder -------

# Создаем кнопки с выбором городов
button_mockva: KeyboardButton = KeyboardButton(text=CITY_EN['moskva'])
button_ufa: KeyboardButton = KeyboardButton(text=CITY_EN['ufa'])
button_spb: KeyboardButton = KeyboardButton(text=CITY_EN['sankt-peterburg'])
button_perm: KeyboardButton = KeyboardButton(text=CITY_EN['perm'])
button_sochi: KeyboardButton = KeyboardButton(text=CITY_EN['sochi'])
button_ekaterinburg: KeyboardButton = KeyboardButton(text=CITY_EN['ekaterinburg'])


# Инициализируем билдер для клавиатуры с кнопками "Городов"
city_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()

# Добавляем кнопки в билдер с параметром width=3
city_builder.row(button_ufa, button_spb, button_perm, button_mockva,
                 button_sochi, button_ekaterinburg, width=3)

# Создаем клавиатуру с кнопками "Городов"
city_kb = city_builder.as_markup(
                                one_time_keyboard=True,
                                resize_keyboard=True)

# Создаем кнопки с ценами квартир
button_ten: KeyboardButton = KeyboardButton(text=PRICE["0-10000"])
button_twenty: KeyboardButton = KeyboardButton(text=PRICE["10000-20000"])
button_thirty: KeyboardButton = KeyboardButton(text=PRICE["20000-50000"])
button_more: KeyboardButton = KeyboardButton(text=PRICE["50000-500000"])

# Инициализируем билдер для клавиатуры с кнопками "Цен"
price_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()

# Добавляем кнопки в билдер с параметром width=2
price_builder.row(button_ten, button_twenty, button_thirty, button_more, width=2)

# Создаем клавиатуру с кнопками "Цен"
price_kb = price_builder.as_markup(
                                one_time_keyboard=True,
                                resize_keyboard=True)

# Создаем объекты инлайн-кнопок
parsing_button: InlineKeyboardButton = InlineKeyboardButton(
    text='🔍Парсинг',
    callback_data='parsing_button')

write_admin_button: InlineKeyboardButton = InlineKeyboardButton(
    text='👨‍💻Написать администратору',
    url='https://t.me/shveitcer')

additionally_button: InlineKeyboardButton = InlineKeyboardButton(
    text='❓Дополнительно',
    callback_data='additionally_button')

start_bilder: InlineKeyboardBuilder = InlineKeyboardBuilder()
start_bilder.row(parsing_button, write_admin_button, additionally_button, width=2)
start_kb = start_bilder.as_markup()


# Создаем объекты инлайн-кнопок(категории парсинга)
flat_long_button: InlineKeyboardButton = InlineKeyboardButton(
    text='Сдачи квартир на длительный срок',
    callback_data='flat_long_button')

flat_short_button: InlineKeyboardButton = InlineKeyboardButton(
    text='Сдачи квартир посуточно',
    callback_data='flat_short_button')

buy_flat_button: InlineKeyboardButton = InlineKeyboardButton(
    text='Покупка квартир',
    callback_data='buy_flat_button')

buy_car: InlineKeyboardButton = InlineKeyboardButton(
    text='Покупка автомобилей',
    callback_data='buy_car')

kategory_bilder: InlineKeyboardBuilder = InlineKeyboardBuilder()
kategory_bilder.row(flat_long_button, flat_short_button, buy_flat_button, buy_car, width=1)
kategory_kb = kategory_bilder.as_markup()



# # Создаем кнопки с админ панелью
# button_add: KeyboardButton = KeyboardButton(text=CHANGE_CITY["add"])
# button_delete: KeyboardButton = KeyboardButton(text=CHANGE_CITY["delete"])
#
# # Инициализируем билдер для клавиатуры с кнопками "admin панели"
# admin_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()
#
# # Добавляем кнопки в билдер с параметром width=2
# admin_builder.row(button_add, button_delete, width=2)
#
# # Создаем клавиатуру с кнопками
# admin_kb = admin_builder.as_markup(
#                                 one_time_keyboard=True,
#                                 resize_keyboard=True)