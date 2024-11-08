from aiogram.utils.keyboard import InlineKeyboardBuilder

from db.db_helper import get_quiz_index, update_record
from content.question import quiz_data
from utils.callback_factory import AnswerCallbackFactory


async def new_quiz(message):
    # получаем id пользователя, отправившего сообщение
    user_id = message.from_user.id

    # сбрасываем значение текущего индекса вопроса квиза и количество правильных ответов в 0
    current_question_index = 0
    current_result_right_answer = 0
    await update_record(user_id, current_question_index, current_result_right_answer)

    # запрашиваем новый вопрос для квиза
    await get_question(message, user_id)


async def get_question(message, user_id):
    # Запрашиваем из базы текущий индекс для вопроса
    current_question_index = await get_quiz_index(user_id)

    # Получаем индекс правильного ответа для текущего вопроса
    correct_index = quiz_data[current_question_index]['correct_option']

    # Получаем список вариантов ответа для текущего вопроса
    opts = quiz_data[current_question_index]['options']

    # Функция генерации кнопок для текущего вопроса квиза
    # В качестве аргументов передаем варианты ответов и значение правильного ответа (не индекс!)
    kb = generate_options_keyboard(opts, opts[correct_index])

    # Отправляем в чат сообщение с вопросом, прикрепляем сгенерированные кнопки
    await message.answer(
        f"{quiz_data[current_question_index]['question']}",
        reply_markup=kb,
    )


def generate_options_keyboard(answer_options, right_answer):
  # Создаем сборщика клавиатур типа Inline
    builder = InlineKeyboardBuilder()
    btn_idx = 0

    # В цикле создаем 4 Inline кнопки, а точнее Callback-кнопки
    for option in answer_options:
        builder.button(
            # Текст на кнопках соответствует вариантам ответов
            text=option,
            # Присваиваем данные для колбэк запроса.
            # Если ответ верный сформируется колбэк-запрос с данными 'right'
            # Если ответ неверный сформируется колбэк-запрос с данными 'wrong'
            # Так же передается индекс выбранного ответа
            callback_data=AnswerCallbackFactory(
                action="right" if option == right_answer else "wrong",
                value=btn_idx,
            ),
        )
        btn_idx += 1

    # Выводим по одной кнопке в столбик
    builder.adjust(1)
    return builder.as_markup()
