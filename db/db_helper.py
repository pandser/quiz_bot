import aiosqlite
from typing import Sequence

DB_NAME: str = 'quiz_bot.sqlite3'


async def create_table() -> None:
    # Создаем соединение с базой данных (если она не существует, то она будет создана)
    async with aiosqlite.connect(DB_NAME) as db:
        # Выполняем SQL-запрос к базе данных
        await db.execute(
            '''CREATE TABLE IF NOT EXISTS quiz_state (user_id INTEGER PRIMARY KEY, question_index INTEGER, right_answer INTEGER)'''
        )
        # Сохраняем изменения
        await db.commit()


async def update_record(user_id: int, index: int, right_answer: int) -> None:
    # Создаем соединение с базой данных (если она не существует, она будет создана)
    async with aiosqlite.connect(DB_NAME) as db:
        # Вставляем новую запись или заменяем ее, если с данным user_id уже существует
        await db.execute(
            'INSERT OR REPLACE INTO quiz_state (user_id, question_index, right_answer) VALUES (?, ?, ?)',
            (user_id, index, right_answer),
        )
        # Сохраняем изменения
        await db.commit()


async def get_quiz_index(user_id: int) -> int:
     # Подключаемся к базе данных
     async with aiosqlite.connect(DB_NAME) as db:
        # Получаем запись для заданного пользователя
        async with db.execute(
            'SELECT question_index FROM quiz_state WHERE user_id = (?)',
            (user_id, )
        ) as cursor:
            # Возвращаем результат
            results = await cursor.fetchone()
            if results is not None:
                return results[0]
            else:
                return 0


async def get_right_answer(user_id: int) -> int:
     # Подключаемся к базе данных
     async with aiosqlite.connect(DB_NAME) as db:
        # Получаем запись для заданного пользователя
        async with db.execute(
            'SELECT right_answer FROM quiz_state WHERE user_id = (?)',
            (user_id, )
        ) as cursor:
            # Возвращаем результат
            results = await cursor.fetchone()
            if results is not None:
                return results[0]
            else:
                return 0
            

async def get_top_ten() -> Sequence | None:
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute(
            'SELECT user_id, right_answer FROM quiz_state ORDER BY right_answer DESC LIMIT 10',
        ) as cursor:
            results = await cursor.fetchall()
            if results is not None:
                return results
            else:
                return None
