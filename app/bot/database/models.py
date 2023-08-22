from sqlalchemy import String, ForeignKey, BigInteger
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship

from app.bot.database.session import Base


class Users(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False, unique=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False)
    chat_id: Mapped[int] = mapped_column(BigInteger, nullable=False)

    offers: Mapped["Offers"] = relationship('Offers', back_populates='users')


class Offers(Base):
    __tablename__ = 'offers'

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    offer_id: Mapped[int] = mapped_column(BigInteger, nullable=False, unique=True)
    title: Mapped[str] = mapped_column(String(100))
    price: Mapped[int] = mapped_column()
    address: Mapped[str] = mapped_column(String(100))
    url: Mapped[str] = mapped_column(String(200))
    date: Mapped[str] = mapped_column(String(50))

    users_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    users: Mapped["Users"] = relationship('Users', back_populates='offers')



