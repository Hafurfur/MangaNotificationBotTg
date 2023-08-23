from src.tele_bot.bot_back.save_manga_acc import save_new_mg_acc
from src.tele_bot.bot_back.site_data import search_account, get_photo_account
from loader import bot
from src.tele_bot.bot_back.inline_buttons import search_manga_acc_inline
from src.logger.base_logger import log

from telebot.storage import StateContext
from telebot.types import Message, CallbackQuery
from telebot.apihelper import ApiException


@bot.message_handler(commands=['add_manga_account'])
def set_mg_acc(message: Message) -> None:
    log.info('Старт обработчика команды "add_manga_account"')
    log.debug(f'{__name__}(message.from_user.id={message.from_user.id})')

    bot.delete_state(message.chat.id)
    bot.set_state(message.chat.id, 'add_new_mg_acc')

    manga_accounts = search_account(message.text)

    if not manga_accounts:
        bot.send_message(message.chat.id, 'Аккаунт не найден\nПопробуйте еще раз, возможно была '
                                          'допущена ошибка в имени аккаунта')
        log.debug(f'Манга аккаунт не найден')
        return

    bot.add_data(message.chat.id, accounts=manga_accounts, account_index=0, cur_message_id=message.message_id)
    photo_acc = get_photo_account(manga_accounts[0].get("id"), manga_accounts[0].get('avatar'))

    try:
        bot.send_photo(message.chat.id, photo=photo_acc,
                       caption=f'[1 из {len(manga_accounts)}] Имя аккаунта: {manga_accounts[0].get("value")}',
                       reply_markup=search_manga_acc_inline)
    except ApiException as error:
        log.error('Ошибка при отправке фотографии через telebot', exc_info=error)
    except Exception as error:
        log.error('Ошибка при отправке фотографии', exc_info=error)


@bot.callback_query_handler(func=lambda call: call.data == 'prev_manga_acc')
def prev_manga_acc(callback_query: CallbackQuery) -> None:
    log.info('Старт обработчика команды "prev_manga_acc"')
    log.debug(f'{__name__}(callback_query.from_user.id={callback_query.from_user.id})')

    state: StateContext = bot.retrieve_data(callback_query.message.chat.id)

    if _check_expired_mess(state, callback_query):
        accounts: list = state.data['accounts']
        account_index: int = state.data['account_index']

        if account_index > 0:
            account_index -= 1
            _send_manga_account(callback_query, len(accounts), accounts[account_index]["id"],
                                accounts[account_index]["value"], accounts[account_index]['avatar'], account_index)

        bot.answer_callback_query(callback_query.id)


@bot.callback_query_handler(func=lambda call: call.data == 'next_manga_acc')
def next_manga_acc(callback_query: CallbackQuery) -> None:
    log.info('Старт обработчика команды "next_manga_acc"')
    log.debug(f'{__name__}(callback_query.from_user.id={callback_query.from_user.id})')

    state: StateContext = bot.retrieve_data(callback_query.message.chat.id)

    if _check_expired_mess(state, callback_query):
        accounts: list = state.data['accounts']
        account_index: int = state.data['account_index']

        if account_index < len(accounts) - 1:
            account_index += 1
            _send_manga_account(callback_query, len(accounts), accounts[account_index]["id"],
                                accounts[account_index]["value"], accounts[account_index]['avatar'], account_index)
        bot.answer_callback_query(callback_query.id)


@bot.callback_query_handler(func=lambda call: call.data == 'add_manga_acc')
def add_manga_acc(callback_query: CallbackQuery) -> None:
    log.info('Старт обработчика команды "add_manga_acc"')
    log.debug(f'{__name__}(callback_query.from_user.id={callback_query.from_user.id})')
    state: StateContext = bot.retrieve_data(callback_query.message.chat.id)

    if _check_expired_mess(state, callback_query):
        accounts: list = state.data['accounts']
        account_index: int = state.data['account_index']

        try:
            bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
            log.debug(f'Сообщение chat={callback_query.message.chat.id}, '
                      f'message_id={callback_query.message.message_id} было удалено')

        except ApiException as error:
            log.error('Ошибка при удалении сообщения через telebot', exc_info=error)
        except Exception as error:
            log.error('Ошибка при удалении сообщения', exc_info=error)

        bot.delete_state(callback_query.message.chat.id)
        result_save_mg_acc = save_new_mg_acc(callback_query.from_user.id, accounts[account_index]['id'],
                                             accounts[account_index]['value'])

        try:
            if result_save_mg_acc:
                bot.send_message(callback_query.message.chat.id,
                                 f'Аккаунт {accounts[account_index]["value"]} был добавлен')
            else:
                bot.send_message(callback_query.message.chat.id,
                                 f'Во время добавления аккаунта {accounts[account_index]["value"]} произошла ошибка. '
                                 f'Попробуйте повторить попытку.')

        except ApiException as error:
            log.error('Ошибка при отправке сообщения через telebot', exc_info=error)
        except Exception as error:
            log.error('Ошибка при отправке сообщения', exc_info=error)


@bot.callback_query_handler(func=lambda call: call.data == 'cancel_search_manga_acc')
def cancel_search_manga_acc(callback_query: CallbackQuery) -> None:
    log.info('Старт обработчика команды "cancel_search_manga_acc"')
    log.debug(f'{__name__}(callback_query.from_user.id={callback_query.from_user.id})')

    state: StateContext = bot.retrieve_data(callback_query.message.chat.id)

    if _check_expired_mess(state, callback_query):

        try:
            bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
            log.debug(f'Сообщение chat={callback_query.message.chat.id}, '
                      f'message_id={callback_query.message.message_id} было удалено')

        except ApiException as error:
            log.error('Ошибка при удалении сообщения через telebot', exc_info=error)
        except Exception as error:
            log.error('Ошибка при удалении сообщения', exc_info=error)
        bot.delete_state(callback_query.message.chat.id)


def _check_expired_mess(state: StateContext, callback_query: CallbackQuery) -> bool:
    log.debug(f'{__name__}(state={state.data}, callback_query.message.message_id={callback_query.message.message_id})')

    if state.data is None or callback_query.message.message_id < state.data['cur_message_id']:

        try:
            bot.answer_callback_query(callback_query.id, text='Сообщение устарело')
        except ApiException as error:
            log.error('Ошибка при отправке сообщения через telebot', exc_info=error)
        except Exception as error:
            log.error('Ошибка при отправке сообщения', exc_info=error)

        return False
    return True


def _send_manga_account(callback_query: CallbackQuery, len_list_acc: int, acc_id: str, acc_name: str, photo_id: str,
                        index: int) -> None:
    log.debug(f'{__name__}(callback_query, len_list_acc={len_list_acc}, acc_id={acc_id}, acc_name={acc_name}, '
              f'photo_id={photo_id}, index={index})')

    photo_acc = get_photo_account(acc_id, photo_id)
    bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)

    try:
        bot.send_photo(callback_query.message.chat.id, photo=photo_acc,
                       caption=f'[{index + 1} из {len_list_acc}] Имя аккаунта: {acc_name}',
                       reply_markup=search_manga_acc_inline)
    except ApiException as error:
        log.error('Ошибка при отправке фотографии через telebot', exc_info=error)
    except Exception as error:
        log.error('Ошибка при отправке фотографии', exc_info=error)

    bot.add_data(callback_query.message.chat.id, account_index=index)
