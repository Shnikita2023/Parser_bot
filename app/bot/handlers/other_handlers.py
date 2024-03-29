from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state
from aiogram.types import Message

from ..lexicon.lexicon import LEXICON_RU

other_router: Router = Router()


# Хэндлер для сообщений, которые не попали в другие хэндлеры
@other_router.message(StateFilter(default_state))
async def send_echo(message: Message):
    await message.reply(text=LEXICON_RU['other_answer'])
