import os
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from utils import GROUP_MESSAGE, is_meta_question


BOT_TOKEN = os.getenv("BOT_TOKEN") #YOUR BOT_TOKEN FROM @BotFather
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


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
            await message.reply(GROUP_MESSAGE, parse_mode='html')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
