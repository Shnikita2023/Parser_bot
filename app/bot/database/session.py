from typing import Generator, Any

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import Config, load_config

config: Config = load_config()
HOST = config.bd.host
PORT = config.bd.port
USER = config.bd.user
PASSWORD = config.bd.password
DB_NAME = config.bd.db_name

DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}"


class Base(DeclarativeBase):
    pass


engine = create_engine(DATABASE_URL)
session_maker = sessionmaker(bind=engine, expire_on_commit=False)


def get_session() -> Generator[Session, Any, None]:
    with session_maker() as session:
        yield session
