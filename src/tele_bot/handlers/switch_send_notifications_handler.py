from loader import bot
from src.logger.base_logger import log
from src.tele_bot.bot_back.switch_send_notifications import switch_notification

from telebot.apihelper import ApiException
from telebot.types import Message


@bot.message_handler(commands=['notification_on', 'notification_off'])
def notification_on(message: Message):
    log.info('Старт обработчика команды "notification_on / notification_off"')
    log.debug(f'message.from_user.id={message.from_user.id}, message.chat.id={message.chat.id}, '
              f'message.text={message.text}')

    command_part = message.text.split(' ')[0].lstrip('/')
    status = 'ON' if command_part == 'notification_on' else 'OFF'
    switch_notification(status, message.from_user.id)

    feedback_mes = f'Получение уведомлений было {"включено" if command_part == "notification_on" else "выключено"}'

    try:
        bot.send_message(message.chat.id, text=feedback_mes)
    except ApiException as error:
        log.error('Ошибка при отправке сообщения (Telebot)', exc_info=error)
    except Exception as error:
        log.error('Ошибка при отправке сообщения', exc_info=error)





