from app.bot.database.models import Users, Offers
from app.bot.database.session import get_session
from sqlalchemy import select


class Database:
    def __init__(self) -> None:
        self.session = next(get_session())

    def create_user(self, user_id: int, username: str, chat_id: int) -> None:
        """Функция создание пользователя"""
        user = Users(user_id=user_id, username=username, chat_id=chat_id)
        self.session.add(user)
        self.session.commit()

    def get_user(self, user_id: int) -> tuple | None:
        """Функция получение пользователя"""
        result = self.session.query(Users.id).where(Users.user_id == user_id)
        return tuple(result.one())


    def get_offer(self, offer_id: int, user_id: int, price_list: list[int]) -> tuple:
        """Функция получение оффера у пользователя"""
        price_min, price_max = price_list
        stmt = select(Users.id).join(Offers).filter(
            Users.user_id == user_id,
            Offers.price.between(price_min, price_max),
            Offers.offer_id == offer_id)
        result = self.session.execute(stmt)
        return result.first()

    def create_offer(self, offer_id: int, title: str, price: int,
                     address: str, url: str, date: str, users_id: int) -> None:
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

#
# d = Database()
# print(d.get_user(user_id=1668957907))
# d.create_offer(offer=(21311321221, 'Квартира', 4000, 'Шмидта', 'яндексю.ру', '1997.01.01', 1))
