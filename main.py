import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage, Redis

from app.bot.handlers.admin_handlers import admin_router
from app.bot.handlers.other_handlers import other_router
from app.bot.handlers.user_handlers import user_router
from app.bot.middlewares.middlewares import TrottlingMiddleware
from app.config import load_config, Config


# Инициализируем логгер
logger = logging.getLogger(__name__)

# Функция конфигурирования и запуска бота
async def main():
    # Конфигурируем логирование
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s '
               u'[%(asctime)s] - %(name)s - %(message)s', filename=f"{__name__}.log", filemode="w")

    # Выводим в консоль информацию о начале запуска бота
    logger.info('Starting bot')

    # Загружаем конфиг в переменную config
    config: Config = load_config()

    # Инициализируем Redis
    redis: Redis = Redis(host=config.rd.host, port=config.rd.port)
    storage: RedisStorage = RedisStorage(redis=redis)

    # Инициализируем бот и диспетчер
    bot: Bot = Bot(token=config.tg_bot.token,
                   parse_mode='HTML')
    dp: Dispatcher = Dispatcher(storage=storage)

    # Регистрируем миделварри
    dp.message.middleware.register(TrottlingMiddleware(storage=storage))

    # Регистриуем роутеры в диспетчере
    dp.include_router(user_router)
    dp.include_router(admin_router)
    dp.include_router(other_router)

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        # Запускаем функцию main в асинхронном режиме
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        # Выводим в консоль сообщение об ошибке,
        # если получены исключения KeyboardInterrupt или SystemExit
        logger.error('Bot stopped!')
