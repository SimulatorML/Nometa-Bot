import os
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor


GROUP_MESSAGE = """
Ребят, пожалуйста, не задавайте <a href='https://nometa.xyz/ru.html'>мета-вопросы</a> в чате!
– вопросы, которые подразумевают другие вопросы.

Примеры мета-вопросов:
- Можно задать вопрос про X?
- Здесь есть, кто проходил курс Y?
- Ребят, а кто работал с Z?

Они тратят время! И ваше, и других людей, которые пытаются вам помочь :)
"""

patterns_meta_questions = [
    'здесь кто-нибудь работал с',
    'кто-нибудь разбирается в',
    'можно задать вопрос про',
    'кто проходил курс',
    'кто шарит за',
    'кто юзал',
    'можно задать вопрос',
]


BOT_TOKEN = os.getenv("BOT_TOKEN") #YOUR BOT_TOKEN FROM @BotFather
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


def is_meta_question(message: str) -> bool:
    """
    Функция проверяет, является ли сообщение мета-вопросом.

    Parameters
    ----------
    message : str
        Сообщенние от пользователя.

    Returns
    -------
    bool
        True, если сообщение - мета вопрос.
        False, если сообщение - обычный вопрос.
    """
    message = message.lower()
    for meta_question in patterns_meta_questions:
        if message in meta_question:
            return True
    return False


@dp.message_handler()
async def check_message(message: types.Message):
    """
    Функция обрабатывает сообщения пользователей.
    В личном чате на каждое сообщение отвечает классом, к которому оно относится:
        - Сообщение без вопроса
        - Мета-вопрос
        - Обычный вопрос
    В групповом чате отвечает только на мета-вопросы.
    """
    if message.chat.type == 'private':
        if '?' not in message.text:
            await message.reply('Это не вопрос.')
        elif is_meta_question(message.text):
            await message.reply('Это мета-вопрос.')
        else:
            await message.reply('Это обычный вопрос.')
    elif message.chat.type == 'group':
        if is_meta_question(message.text):
            await message.reply(GROUP_MESSAGE)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
