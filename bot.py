import openai
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.utils import executor
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import BOT_TOKEN, OPENAI_TOKEN


openai.api_key = OPENAI_TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


BOT_MESSAGE = """Ребят, пожалуйста, не задавайте <a href='https://nometa.xyz/ru.html'>мета-вопросы</a> в чате!
– вопросы, которые подразумевают другие вопросы.

Примеры мета-вопросов:
- Можно задать вопрос про X?
- Здесь есть, кто проходил курс Y?
- Ребят, а кто работал с Z?

Они тратят время! И ваше, и других людей, которые пытаются вам помочь :)

Оцените корректность работы кнопкой ниже
"""


def is_meta_question(text: str) -> bool:
    """Функция проверяет с помощью запроса к ChatGPT, является ли сообщение пользователя мета-вопросом.

    Parameters
    ----------
    text : str
        Сообщение пользователя

    Returns
    -------
    bool
        True, если сообщение - мета-вопрос
        False иначе
    """
    prompt = f"""Мета-вопрос — это вопрос, который подразумевает другие вопросы.
    Некоторые примеры мета-вопросов 1) Можно ли задать вопрос? 2) Кто разбирается в ...? 3) Кто работал с ...? 
    Является ли вопрос '{text}' мета-вопросом? Напиши да или нет. Говори да, если сильно уверена."""
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        max_tokens=1500,
        temperature=0.1,
        n=1
    )
    ans = response.choices[0].text.strip().lower()
    if 'да' in ans:
        return True
    return False


@dp.message_handler()
async def find_meta_questions(message: types.Message):
    if is_meta_question(message.text):
        await message.reply(
            BOT_MESSAGE,
            parse_mode='HTML',
            reply_markup=InlineKeyboardMarkup(row_width=2).add(
                InlineKeyboardButton(text='👍',
                                     callback_data=f'feedback_like_{message.chat.id}_{message.message_id}'),
                InlineKeyboardButton(text='👎',
                                     callback_data=f'feedback_dislike_{message.chat.id}_{message.message_id}')
            ))

votes = dict()


@dp.callback_query_handler(Text(startswith='feedback_'))
async def feedback_processing(callback: types.CallbackQuery):
    """Как бейзлайн оценки пользователей пишутся в консоль. Дальше можно сохранять в базу данных."""
    action, chat_id, message_id = callback.data.split('_')[1:]
    user_id = callback.from_user.id
    if user_id not in votes[message_id]:
        votes[message_id].append(user_id)
        if action == 'like':
            print(f'Пользователь {user_id} сказал, что вопрос {message_id} с чата {chat_id} является метавопросом')
        elif action == 'dislike':
            print(f'Пользователь {user_id} сказал, что вопрос {message_id} с чата {chat_id} не является метавопросом')
        await callback.answer('Спасибо за голос!', show_alert=True)
    else:
        await callback.answer('Вы уже голосовали', show_alert=True)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
