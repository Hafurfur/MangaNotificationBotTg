from src.tele_bot.bot_back.save_tg_acc import save_telegram_account
from loader import bot
from src.logger.base_logger import log

from telebot.apihelper import ApiException
from telebot.types import Message


@bot.message_handler(commands=['start'])
def start_bot_on_client(message: Message):
    log.info('Старт обработчика команды "start"')
    log.debug(f'message.from_user.id={message.from_user.id}, message.chat.id={message.chat.id}')

    save_telegram_account(message.from_user.id, message.from_user.username,
                          message.from_user.first_name, message.from_user.last_name)

    star_message = (f'Добро пожаловать {message.from_user.first_name}!\nС этого момента бот сможет '
                    f'присылать уведомления о выходе новых главах манги с сайта mangalib.\nЧто бы '
                    f'получать уведомления нужно через команду /add_mangalib_account "имя аккаунта" '
                    f'добавить аккаунт с сайта mangalib.\nПри добавлении аккаунта '
                    f'будут приходить уведомления для манги из вкладки "Читаю".\nКак выйдет новая '
                    f'глава бот вам её пришлет.')

    try:
        bot.send_message(message.chat.id, text=star_message)
    except ApiException as error:
        log.error('Ошибка при отправке сообщения (Telebot)', exc_info=error)
    except Exception as error:
        log.error('Ошибка при отправке сообщения', exc_info=error)


@bot.message_handler(commands=['help'])
def help_client_mes(message: Message):
    log.info('Старт обработки команды "help"')
    log.debug(f'message.from_user.id={message.from_user.id}, message.chat.id={message.chat.id}')

    help_message = (f'Список доступных команд:'
                    f'  /add_mangalib_account ИМЯ АККАУНТА - добавляет манга аккаунт'
                    f'  /notification_on - включить получение уведомления'
                    f'  /notification_off - отключение получение уведомления')

    try:
        bot.send_message(message.chat.id, text=help_message)
    except ApiException as error:
        log.error('Ошибка при отправке сообщения (Telebot)', exc_info=error)
    except Exception as error:
        log.error('Ошибка при отправке сообщения', exc_info=error)
