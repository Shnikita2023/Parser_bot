from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message

from ..lexicon.lexicon import PRICE


class TrottlingMiddleware(BaseMiddleware):
    # Миддлевари на анти флуд
    def __init__(self, storage: RedisStorage) -> None:
        self.storage = storage

    async def __call__(self,
                       handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
                       event: Message,
                       data: Dict[str, Any]
                       ) -> Any:
        list_allowed_command = ["/start", "/help", "/cancel", "/pars", "/admin"] + list(PRICE.values())  # Разрешенные команды
        if event.text.lower() in list_allowed_command:
            return await handler(event, data)

        user = f'user{event.from_user.id}'
        check_user = await self.storage.redis.get(name=user)

        if check_user:
            if int(check_user.decode()) == 1:
                await self.storage.redis.set(name=user, value=0, ex=5)
                return await event.answer(text="Слишком частые запросы, не надо флудить\n"
                                               "Ожидайте, 5 секунд")
            return
        await self.storage.redis.set(name=user, value=1, ex=5)

        return await handler(event, data)

