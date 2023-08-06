import os
import random
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from src.app.utils import (check_question_with_rubert_clf,
                           check_question_pattern,
                           check_question_with_tfidf_model)
from src.app.constants import GROUP_MESSAGES


BOT_TOKEN = os.getenv("BOT_TOKEN")  # YOUR BOT_TOKEN FROM @BotFather
CHANNEL_ID = os.getenv("DATASET_CHANNEL") #CHANNEL_ID FOR COLLECTING DATA
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# TODO: Temporary fix. Swap to select question definition type
# checking_tfidf_model, pattern_checking
message_check = check_question_with_rubert_clf


class BotMetaMessageChecker:
    """
    TODO: add descriptions
    """
    def start(self):
        executor.start_polling(dp, skip_updates=True)


@dp.message_handler()
async def check_message(message: types.Message):
    """
    Функция обрабатывает сообщения пользователей.
    В личном чате на каждое сообщение отвечает классом,
    к которому оно относится:
        - Сообщение без вопроса
        - Мета-вопрос
        - Обычный вопрос
    В групповом чате отвечает только на мета-вопросы.
    """
    prediction, info = message_check(message.text)
    if message.chat.type == 'private':
        if prediction:
            await message.reply(f'Это мета-вопрос.\n{info}')
        else:
            await message.reply(f'Это обычный вопрос/обычное сообщение.\n{info}')
    else:
        if prediction:
            await message.reply(
                random.choice(GROUP_MESSAGES), parse_mode='html'
            )

    await bot.send_message(chat_id=CHANNEL_ID, text=f"Message from user @{message.from_user.username}\n {info}")
