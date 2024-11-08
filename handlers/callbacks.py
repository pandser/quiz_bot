from aiogram import F, Router, types

from content.question import quiz_data
from db.db_helper import get_right_answer, update_record
from utils.quiz_helper import get_question, get_quiz_index
from utils.callback_factory import AnswerCallbackFactory


router = Router()


@router.callback_query(AnswerCallbackFactory.filter())
async def answer(
    callback: types.CallbackQuery, 
    callback_data: AnswerCallbackFactory,
    ):
    # редактируем текущее сообщение с целью убрать кнопки (reply_markup=None)
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )
    # Получение текущего вопроса для данного пользователя
    current_question_index = await get_quiz_index(callback.from_user.id)
    current_result_right_answer = await get_right_answer(callback.from_user.id)
    usr_answer = quiz_data[current_question_index]['options'][callback_data.value]
    if callback_data.action == 'right':
        # Отправляем в чат сообщение, что ответ верный
        await callback.message.answer(f"Верно! {usr_answer}")
        current_result_right_answer += 1
    else:
        correct_option = quiz_data[current_question_index]['correct_option']
        await callback.message.answer(
            f"{usr_answer} - неверный ответ. "
            f"Правильный ответ: {quiz_data[current_question_index]['options'][correct_option]}"
        )

    # Обновление номера текущего вопроса в базе данных
    current_question_index += 1
    await update_record(
        callback.from_user.id,
        current_question_index,
        current_result_right_answer,
    )

    # Проверяем достигнут ли конец квиза
    if current_question_index < len(quiz_data):
        # Следующий вопрос
        await get_question(callback.message, callback.from_user.id)
    else:
        # Уведомление об окончании квиза
        await callback.message.answer(
            f'Это был последний вопрос. Квиз завершен! '
            f'{callback.from_user.first_name} Ваш результат '
            f'{current_result_right_answer} правильных ответов из 10.'
        )
