from aiogram.filters.callback_data import CallbackData


class AnswerCallbackFactory(CallbackData, prefix="answer"):
    action: str
    value: int