from aiogram import Router
from aiogram.filters import Command, CommandStart, Text, BaseFilter
from aiogram.types import Message
from bot.keyboards import admin_kb
from bot.lexicon import ADMIN_PANEL
from bot.config_data import Config, load_config
from bot.filters.filters import IsAdmin

router: Router = Router()
config: Config = load_config()
admin_id = int(config.tg_bot.admin)


# Этот хэндлер будет срабатывать, если апдейт от админа
@router.message(IsAdmin(admin_id), Text(startswith='/admin'))
async def answer_if_admins_update(message: Message) -> None:
    first_name = message.from_user.first_name
    await message.answer(text=f'Добро пожаловать босс {first_name}, что хочешь добавить или удалить?!',
                         reply_markup=admin_kb)


@router.message(Text(text=ADMIN_PANEL["add"]))
async def operatsiya_city(message: Message) -> None:
    await message.answer(text=f"Напиши город, который желаешь удалить")
    # Не реализована логика
    city_message = message.text


@router.message(Text(text=ADMIN_PANEL["delete"]))
async def operatsiya_city(message: Message) -> None:
    await message.answer(text=f"Напиши город, который желаешь добавить")
    # Не реализована логика
    city_message = message.text


# Этот хэндлер будет срабатывать, если апдейт не от админа
@router.message(Text(startswith='/admin'))
async def answer_if_not_admins_update(message: Message) -> None:
    await message.answer(text='Нет прав доступа')
