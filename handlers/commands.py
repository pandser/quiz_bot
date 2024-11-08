from aiogram import F, Router, types
from aiogram.filters.command import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from db.db_helper import get_top_ten
from utils.quiz_helper import new_quiz
from utils.tg_user import get_name


router = Router()


# Хэндлер на команду /start
@router.message(Command("start"))
async def cmd_start(message: types.Message):
    # Создаем сборщика клавиатур типа Reply
    builder = ReplyKeyboardBuilder()

    # Добавляем в сборщик кнопки
    builder.add(types.KeyboardButton(text="Начать игру"))
    builder.add(types.KeyboardButton(text="Топ 10"))
    
    builder.adjust(1)
    # Прикрепляем кнопки к сообщению
    await message.answer(
        "Добро пожаловать в квиз!",
        reply_markup=builder.as_markup(resize_keyboard=True),
    )


# Хэндлер на команду /quiz
@router.message(F.text=="Начать игру")
@router.message(Command("quiz"))
async def cmd_quiz(message: types.Message):
    # Отправляем новое сообщение без кнопок
    await message.answer(f"Давайте начнем квиз!")

    # Запускаем новый квиз
    await new_quiz(message)


# Хэндлер на команду /top10
@router.message(F.text=="Топ 10")
@router.message(Command('top10'))
async def cmd_top_ten(message: types.Message):
    top10 = await get_top_ten()
    text = ''
    for i in top10:
        text += f'{await get_name(i[0])} {i[1]}\n'
    await message.answer(text)
