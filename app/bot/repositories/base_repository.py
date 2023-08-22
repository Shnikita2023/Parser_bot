from abc import ABC, abstractmethod
from typing import Any

from sqlalchemy import insert, select, delete, update
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.asyncio import AsyncSession


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one(self, data):
        raise NotImplementedError

    @abstractmethod
    async def find_all(self):
        raise NotImplementedError

    @abstractmethod
    async def find_one(self, data_id):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add_one(self, data: dict) -> int:
        try:
            stmt = insert(self.model).values(**data).returning(self.model.id)
            res = await self.session.execute(stmt)
            return res.scalar_one()

        except ConnectionError:
            raise Exception("Ошибка подключения к базе данных")

        except Exception as ex:
            raise f"Ошибка {ex}"

    async def find_all(self) -> list[model]:
        try:
            stmt = select(self.model)
            res = await self.session.execute(stmt)
            res = [row[0].to_read_model() for row in res.all()]
            return res

        except ConnectionError:
            raise Exception("Ошибка подключения к базе данных")

        except InvalidRequestError:
            raise Exception("Некорректный запрос, проверьте формат данных")

        except Exception as ex:
            raise f"Ошибка {ex}"

    async def find_one(self, data_id: int) -> model:
        try:
            stmt = select(self.model).where(self.model.id == data_id)
            res = await self.session.execute(stmt)
            res = [row[0].to_read_model() for row in res.all()]
            return res[0]

        except ConnectionError:
            raise Exception("Ошибка подключения к базе данных")

        except InvalidRequestError:
            raise Exception("Некорректный запрос, проверьте формат данных")

        except Exception as ex:
            raise f"Ошибка {ex}"



