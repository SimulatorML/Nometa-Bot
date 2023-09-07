import os
import random
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from src.app.utils import (check_question_with_rubert_clf,
                           check_question_pattern,
                           check_question_with_tfidf_model)
from src.app.constants import GROUP_MESSAGES
from src.app.constants import PRIVATE_MESSAGES_POS
from src.app.constants import PRIVATE_MESSAGES_NEG

# Load your Bot Token and Channel ID from environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")  # YOUR BOT_TOKEN FROM @BotFather
CHANNEL_ID = os.getenv("CHANNEL_ID")  # CHANNEL_ID FOR COLLECTING DATA

# Create a Bot instance and a Dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# TODO: Temporary fix. Swap to select question definition type
# checking_tfidf_model, pattern_checking
message_check = check_question_with_rubert_clf


class BotMetaMessageChecker:
    """
    A class to manage message checking and handling for the bot.
    """

    def start(self):
        """
        Start polling for new messages using the Dispatcher.
        """
        executor.start_polling(dp, skip_updates=True)


@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
    """
    Handle the /start command.
    """
    if message.chat.type == "private":
        await message.answer("Привет! Для того чтобы начать, просто напиши мне какой-нибудь вопрос или сообщение.")


@dp.message_handler()
async def check_message(message: types.Message):
    """
    Process user messages and respond accordingly.

    In a private chat, respond based on the type of question:
        - Non-question message
        - Meta-question
        - Regular question

    In a group chat, only respond to meta-questions.
    Responds to help questions

    Parameters
    ----------
    message : types.Message
        The incoming message to process.
    """

    prediction, info = message_check(message.text)

    if message.chat.type == 'private':
        if prediction:
            await message.reply(
                random.choice(PRIVATE_MESSAGES_POS), parse_mode='html'
            )
        else:
            await message.reply(
                random.choice(PRIVATE_MESSAGES_NEG), parse_mode='html'
            )
    else:
        if message.photo:
            prediction = 0
        if prediction:
            await message.reply(
                random.choice(GROUP_MESSAGES), parse_mode='html'
            )

    await bot.send_message(chat_id=CHANNEL_ID, text=f"Message from user @{message.from_user.username}\n {info}")

# Instantiate the BotMetaMessageChecker class and start polling
if __name__ == '__main__':
    bot_meta_checker = BotMetaMessageChecker()
    bot_meta_checker.start()
