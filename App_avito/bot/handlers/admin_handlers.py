from aiogram import Router, F
from aiogram.filters import Command, CommandStart, Text, BaseFilter
from aiogram.types import Message
from bot.lexicon import CITY_EN, LEXICON_RU, PRICE
from bot.config_data import Config, load_config
from bot.filters.filters import IsAdmin

router: Router = Router()
config: Config = load_config()
admin_id = int(config.tg_bot.admin)


# Этот хэндлер будет срабатывать, если апдейт от админа
@router.message(IsAdmin(admin_id), Text(startswith='/admin'))
async def answer_if_admins_update(message: Message):
    first_name = message.from_user.first_name
    await message.answer(text=f'Добро пожаловать босс {first_name}')


# Этот хэндлер будет срабатывать, если апдейт не от админа
@router.message(Text(startswith='/admin'))
async def answer_if_not_admins_update(message: Message):
    await message.answer(text='Нет прав доступа')