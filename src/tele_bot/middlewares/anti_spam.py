from loader import bot
from time import time

from telebot.handler_backends import BaseMiddleware
from telebot.handler_backends import CancelUpdate

from telebot.types import Message, CallbackQuery


class AntiSpam(BaseMiddleware):
    def __init__(self, message_limit: float, callback_limit: float) -> None:
        super().__init__()
        self.update_sensitive = True
        self.last_messages = {}
        self.mes_limit = message_limit
        self.cb_limit = callback_limit
        self.update_types = ['message', 'callback_query']

    def pre_process_message(self, message: Message, data):
        if message.from_user.id not in self.last_messages:
            self.last_messages[message.from_user.id] = time()
            return
        if time() - self.last_messages[message.from_user.id] < self.mes_limit:
            bot.send_message(message.chat.id, 'Слишком много запросов')
            return CancelUpdate()
        self.last_messages[message.from_user.id] = time()

    def post_process_message(self, message, data, exception):
        pass

    def pre_process_callback_query(self, callback_query: CallbackQuery, data):
        if callback_query.from_user.id not in self.last_messages:
            self.last_messages[callback_query.from_user.id] = time()
            return

        if time() - self.last_messages[callback_query.from_user.id] < self.cb_limit:
            bot.answer_callback_query(callback_query.id, 'Слишком много запросов')
            return CancelUpdate()
        self.last_messages[callback_query.from_user.id] = time()

    def post_process_callback_query(self, callback_query, data, exception):
        pass
