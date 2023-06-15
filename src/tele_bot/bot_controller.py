from settings import TOKEN

from telebot import TeleBot

bot = TeleBot(token=TOKEN, skip_pending=True)


def star_bot() -> None:
    import src.tele_bot.handlers
    bot.infinity_polling()


def stop_bot() -> None:
    bot.stop_bot()
