import os
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from src.utils import pattern_checking, checking_tfidf_model
from src.app.constants import GROUP_MESSAGE

BOT_TOKEN = os.getenv("BOT_TOKEN")  # YOUR BOT_TOKEN FROM @BotFather
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# TODO: Temporary fix. Swap to select question definition type
message_check = checking_tfidf_model  # checking_tfidf_model, pattern_checking


class BotMetaMessageChecker:
    def start(self):
        executor.start_polling(dp, skip_updates=True)


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
        elif message_check(message.text):
            await message.reply('Это мета-вопрос.')
        else:
            await message.reply('Это обычный вопрос.')
    elif message.chat.type == 'group':
        if message_check(message.text):
            await message.reply(GROUP_MESSAGE, parse_mode='html')
