from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str
    admin: int


@dataclass
class Database:
    host: str
    port: int
    user: str
    password: str
    db_name: str


@dataclass
class RedisBase:
    host: str
    port: int


@dataclass
class Config:
    tg_bot: TgBot
    bd: Database
    rd: RedisBase


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(tg_bot=TgBot(token=env('BOT_TOKEN'), admin=env('ADMIN')),
                  bd=Database(host=env("DB_HOST"), port=env("DB_PORT"), user=env("DB_USER"),
                              password=env("DB_PASSWORD"), db_name=env("DB_NAME")),
                  rd=RedisBase(host=env("REDIS_HOST"), port=env("REDIS_PORT"))
                  )
