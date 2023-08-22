from aiogram import Router
from aiogram.types import Message

from ..filters.filters import IsAdmin
from ..keyboards.keyboards import admin_kb
from ..lexicon.lexicon import ADMIN_PANEL
from app.config import load_config, Config

admin_router: Router = Router()
config: Config = load_config()
admin_id = int(config.tg_bot.admin)


# Этот хэндлер будет срабатывать, если апдейт от админа
@admin_router.message(IsAdmin(admin_id), lambda message: message.text == '/admin')
async def answer_if_admins_update(message: Message) -> None:
    first_name = message.from_user.first_name
    await message.answer(text=f'Добро пожаловать босс {first_name}, что хочешь добавить или удалить?!',
                         reply_markup=admin_kb)


@admin_router.message(lambda message: message == ADMIN_PANEL["add"])
# Добавление города
async def operatsiya_city(message: Message) -> None: pass


@admin_router.message(lambda message: message == ADMIN_PANEL["delete"])
# Удаление города
async def operatsiya_city(message: Message) -> None: pass


# Этот хэндлер будет срабатывать, если апдейт не от админа
@admin_router.message(lambda message: message.text == '/admin')
async def answer_if_not_admins_update(message: Message) -> None:
    await message.answer(text='Нет прав доступа')
