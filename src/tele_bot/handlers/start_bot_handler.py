from src.tele_bot.bot_back.save_tg_acc import save_telegram_account
from loader import bot
from src.logger.base_logger import log

from telebot.types import Message


@bot.message_handler(commands=['start'])
def start_bot_on_client(message: Message):
    log.info('Старт обработчика команды "start"')
    log.debug(f'message.from_user.id={message.from_user.id}')

    save_telegram_account(message.from_user.id, message.from_user.username,
                          message.from_user.first_name, message.from_user.last_name)
    bot.send_message(message.chat.id, f'Добро пожаловать {message.from_user.first_name}!\nС этого момента бот сможет '
                                      f'присылать уведомления о выходе новых главах манги с сайта mangalib.\nЧто бы '
                                      f'получать уведомления нужно через команду /add_mangalib_account "имя аккаунта" '
                                      f'добавить аккаунт с сайта mangalib.\nПри добавлении аккаунта '
                                      f'будут приходить уведомления для манги из вкладки "Читаю".\nКак выйдет новая '
                                      f'глава бот вам её пришлет.')
