from aiogram.filters import BaseFilter
from aiogram.types import Message


class IsAdmin(BaseFilter):
    """Проверка пользователя на права доступа(admin)"""
    def __init__(self, admins_ids: int) -> None:
        self.admin_ids = admins_ids

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id == self.admin_ids
