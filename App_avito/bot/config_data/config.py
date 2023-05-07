from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str            # Токен для доступа к телеграм-боту
    admin: int

@dataclass
class Database:
    host: str
    user: str
    password: str
    db_name: str

@dataclass
class Config:
    tg_bot: TgBot
    bd: Database


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(tg_bot=TgBot(token=env('BOT_TOKEN'), admin=env('ADMIN')),
                  bd=Database(host=env("HOST"), user=env("USER"),
                              password=env("PASSWORD"), db_name=env("DB_NAME")))




