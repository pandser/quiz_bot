from bot import bot


async def get_name(user_id: int) -> str:
    '''Получение имени пользователя.'''
    user = await bot.get_chat(user_id)
    return user.first_name
