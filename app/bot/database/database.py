from app.bot.database.models import Users, Offers
from app.bot.database.session import get_session, Session
from sqlalchemy import select


class Database:
    def __init__(self) -> None:
        self.session: Session = next(get_session())

    def create_user(self, user_id: int, username: str, chat_id: int) -> None:
        """Функция создание пользователя"""
        user = Users(user_id=user_id, username=username, chat_id=chat_id)
        self.session.add(user)
        self.session.commit()

    def get_user(self, user_id: int) -> int | None:
        """Функция получение пользователя"""
        result = self.session.query(Users.id).where(Users.user_id == user_id)
        return result.scalar()

    def get_offer(self, offer_id: int, user_id: int, price_list: list[int]) -> int | None:
        """Функция получение оффера у пользователя"""
        price_min, price_max = price_list
        stmt = select(Offers.id).join(Users).filter(
            Users.user_id == user_id,
            Offers.price.between(price_min, price_max),
            Offers.offer_id == offer_id)
        result = self.session.execute(stmt)
        return result.scalar()

    def create_offer(self, offer_id: int, title: str, price: int,
                     address: str, url: str, date: str, users_id: int) -> None:
        """Функция создание оффера"""
        offer = Offers(
            offer_id=offer_id,
            title=title,
            price=price,
            address=address,
            url=url,
            date=date,
            users_id=users_id
        )
        self.session.add(offer)
        self.session.commit()


