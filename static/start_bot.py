"""
START BOT

!!! don't forget to add the token to the environment variables !!!
"""

from src.app.bot import BotMetaMessageChecker

if __name__ == '__main__':
    bot = BotMetaMessageChecker()
    bot.start()
