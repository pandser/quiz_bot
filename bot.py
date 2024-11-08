import asyncio
import logging

from aiogram import Bot, Dispatcher

from config import config
from db.db_helper import create_table
from handlers import callbacks, commands


# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

# Объект бота
bot = Bot(token=config.api_token.get_secret_value())

# Диспетчер
dp = Dispatcher()

async def main():
    # Подключаем роутеры к диспетчеру
    dp.include_routers(
        callbacks.router,
        commands.router,
    )

    # Запускаем создание таблицы базы данных
    await create_table()

    # Запуск процесса поллинга новых апдейтов
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
