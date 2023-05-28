from settings import TOKEN
from src.database.bot_db import BotDB

import telebot
from telebot.types import Message

bot = telebot.TeleBot(token=TOKEN, skip_pending=True)


@bot.message_handler(commands=['start'])
def mess(message: Message):
    res = bot.send_message(message.chat.id, f'ggg')
    db = BotDB()
    db.new_account(message.from_user.id, message.from_user.username,
                   message.from_user.first_name, message.from_user.last_name)

    print(message)
    print(res)


bot.infinity_polling()

if __name__ == '__main__':
    # mess('334496904')
    pass
