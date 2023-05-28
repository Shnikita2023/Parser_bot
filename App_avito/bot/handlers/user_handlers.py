from aiogram import Router, F
from aiogram.filters import Command, CommandStart, Text, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery
from bot.fsm.states import FSMParserForm
from bot.keyboards import city_kb, start_kb, kategory_kb, flat_long_button, price_panel
from bot.lexicon import LEXICON_RU, CITY_EN, PRICE
from bot.services import get_data, translation_price, transfer_text_telegram
from bot.database.database import User, Database


router: Router = Router()
database = User(Database())


# Этот хэндлер срабатывает на команду /start
@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message) -> None:
    user_id = message.from_user.id
    username = message.from_user.username
    chat_id = message.chat.id
    database.setup()
    user = database.get_user(user_id=user_id)
    if not user:
        database.create_user(user_id=user_id, username=username, chat_id=chat_id)
    database.shutdown()
    await message.answer(text=LEXICON_RU['/start'], reply_markup=start_kb)


# Этот хэндлер будет срабатывать на команду "/cancel" в любых состояниях,
# кроме состояния по умолчанию, и отключать машину состояний
@router.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext) -> None:
    await message.answer(text='Чтобы снова начать парсинг, нажмите /pars')
    # Сбрасываем состояние
    await state.clear()


# Этот хэндлер будет срабатывать на команду "/cancel" в состоянии
# по умолчанию и сообщать, что эта команда доступна в машине состояний
@router.message(Command(commands='cancel'), StateFilter(default_state))
async def process_cancel_command(message: Message) -> None:
    await message.answer(text='Отменять нечего. Чтобы начать парсинг, нажмите /pars')


# Этот хэндлер срабатывает на команду /help
@router.message(Command(commands=['help']), StateFilter(default_state))
async def process_help_command(message: Message) -> None:
    await message.answer(text=LEXICON_RU['/help'])


# Этот хэндлер для смены города
@router.message(Command(commands=['gorod']), StateFilter(default_state))
async def process_help_command(message: Message, state: FSMContext) -> None:
    await state.set_state(FSMParserForm.name_city)
    await message.answer(text='Выберите город', reply_markup=city_kb)


# Этот хэндлер для выбора категории
@router.callback_query(Text(text=['parsing_button']), StateFilter(default_state))
async def category_command(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.answer(text='Выберите категорию парсинга', reply_markup=kategory_kb)
    await state.set_state(FSMParserForm.category_pars)

@router.message(Command(commands=['pars']), StateFilter(default_state))
async def category_pars(message: Message, state: FSMContext) -> None:
    await message.answer(text='Выберите категорию парсинга', reply_markup=kategory_kb)
    await state.set_state(FSMParserForm.category_pars)

@router.message(StateFilter(FSMParserForm.category_pars))
async def warning_not_pars(message: Message) -> None:
    await message.answer(text='Выберите одну из категории объявление\n'
                              'Отправьте команду /cancel для завершение парсинга')

@router.callback_query(Text(text=['flat_long_button',
                                  'flat_short_button',
                                  'buy_flat_button']), StateFilter(FSMParserForm.category_pars))
async def city_selection(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(category_pars=callback.data)
    await callback.message.answer(text='Выберите город', reply_markup=city_kb)
    await state.set_state(FSMParserForm.name_city)

@router.message(Text(text=list(CITY_EN.values())), StateFilter(FSMParserForm.name_city))
async def price_button(message: Message, state: FSMContext) -> None:
    category = await state.get_data()
    price_category = price_panel(category["category_pars"])
    await state.update_data(name_city=message.text)
    await message.answer(text="Выберите ваш бюджет для снятие квартиры", reply_markup=price_category)
    await state.set_state(FSMParserForm.price)

@router.message(StateFilter(FSMParserForm.name_city))
async def warning_not_city(message: Message) -> None:
    await message.answer(text='Выберите из списка город и нажмите на него!\n'
                              'Отправьте команду /cancel для завершение парсинга')

@router.message(Text(text=list(PRICE.values())), StateFilter(FSMParserForm.price))
async def process_parsing(message: Message, state: FSMContext) -> None:
    await state.update_data(price=message.text)
    await message.answer(text="Ожидайте, пожалуйста...")
    user_id = message.from_user.id
    data_state = await state.get_data()
    category_adit = data_state["category_pars"]
    name_city = data_state["name_city"]
    price_user = data_state["price"]
    range_price_list = translation_price(price=price_user)
    dict_offer = get_data(city=name_city, category=category_adit, user_id=user_id, price=range_price_list)
    count = 0
    for value in dict_offer.values():
        text = transfer_text_telegram(value)
        count += 1
        await message.answer(text=text)
    if not count:
        text = "Объявлений нету!"
        await message.answer(text=text)

    await state.clear()
    await message.answer(text="Готово, чтоб начать заново, нажмите /pars\n"
                              "Можно вернуться в меню /start")

@router.message(StateFilter(FSMParserForm.price))
async def warning_not_price(message: Message) -> None:
    await message.answer(text='Некорректно выбрана цена, нажмите кнопку из списка\n'
                              'Отправьте команду /cancel для завершение парсинга')

