from src.database import having_manga_account, add_account_tracking
from src.site_data import search_account, get_photo_account
from src.tele_bot.bot_controller import bot
from src.tele_bot.inline_buttons import checking_manga_account_inline, search_manga_acc_inline

from telebot.storage import StateContext
from telebot.types import Message, CallbackQuery


@bot.message_handler(commands=['add_mangalib_account'])
def set_mg_acc(message: Message) -> None:
    state = bot.get_state(message.from_user.id)

    if state is None:
        mg_acc_res: str | bool = having_manga_account(message.from_user.id)

        if mg_acc_res:
            bot.set_state(message.chat.id, 'add_mangalib_account')
            bot.add_data(message.chat.id, name_search_acc=message.text)
            bot.send_message(message.chat.id, f'Уже отслеживается аккаунт {mg_acc_res}\nХотите заменить?',
                             reply_markup=checking_manga_account_inline)
            return

    bot.set_state(message.chat.id, 'add_mangalib_account')
    bot.add_data(message.chat.id, name_search_acc=message.text)
    _search_mg_acc(message)


def _search_mg_acc(message: Message) -> None:
    state_data: StateContext = bot.retrieve_data(message.chat.id)

    if _state_data_exist(state_data, message):
        result_search = search_account(state_data.data['name_search_acc'])

        if result_search is None:
            bot.send_message(message.chat.id, 'Аккаунт не найден\nПопробуйте еще раз, возможно была '
                                              'допущена ошибка в имени аккаунта')
        else:
            photo_acc = get_photo_account(result_search[0]["id"], result_search[0]['avatar'])
            bot.add_data(message.chat.id, accounts=result_search, account_index=0)
            bot.send_photo(message.chat.id, photo=photo_acc,
                           caption=f'[1 из {len(result_search)}] Имя аккаунта: {result_search[0]["value"]}',
                           reply_markup=search_manga_acc_inline)


@bot.callback_query_handler(func=lambda call: call.data.endswith('checking_manga_acc'))
def checking_manga_account(callback_query: CallbackQuery) -> None:
    if callback_query.data == 'accept_checking_manga_acc':
        bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
        _search_mg_acc(callback_query.message)

    elif callback_query.data == 'cancel_checking_manga_acc':
        bot.delete_state(callback_query.message.chat.id)
        bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)


@bot.callback_query_handler(func=lambda call: call.data == 'prev_manga_acc')
def prev_manga_acc(callback_query: CallbackQuery) -> None:
    state_data: StateContext = bot.retrieve_data(callback_query.message.chat.id)

    if _state_data_exist(state_data, callback_query.message):
        accounts: list = state_data.data['accounts']
        account_index: int = state_data.data['account_index']

        if account_index > 0:
            account_index -= 1
            _send_manga_account(callback_query, len(accounts), accounts[account_index]["id"],
                                accounts[account_index]["value"], accounts[account_index]['avatar'], account_index)

        bot.answer_callback_query(callback_query.id)


@bot.callback_query_handler(func=lambda call: call.data == 'next_manga_acc')
def next_manga_acc(callback_query: CallbackQuery) -> None:
    state_data: StateContext = bot.retrieve_data(callback_query.message.chat.id)

    if _state_data_exist(state_data, callback_query.message):
        accounts: list = state_data.data['accounts']
        account_index: int = state_data.data['account_index']

        if account_index < len(accounts) - 1:
            account_index += 1
            _send_manga_account(callback_query, len(accounts), accounts[account_index]["id"],
                                accounts[account_index]["value"], accounts[account_index]['avatar'], account_index)
        bot.answer_callback_query(callback_query.id)


@bot.callback_query_handler(func=lambda call: call.data == 'add_manga_acc')
def add_manga_acc(callback_query: CallbackQuery) -> None:
    state_data: StateContext = bot.retrieve_data(callback_query.message.chat.id)

    if _state_data_exist(state_data, callback_query.message):
        accounts: list = state_data.data['accounts']
        account_index: int = state_data.data['account_index']

        bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
        bot.delete_state(callback_query.message.chat.id)
        add_account_tracking(callback_query.from_user.id, accounts[account_index]['id'],
                             accounts[account_index]['value'])
        bot.send_message(callback_query.message.chat.id,
                         f'Аккаунт {accounts[account_index]["value"]} был добавлен')


@bot.callback_query_handler(func=lambda call: call.data == 'cancel_search_manga_acc')
def cancel_search_manga_acc(callback_query: CallbackQuery) -> None:
    bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    bot.delete_state(callback_query.message.chat.id)


def _state_data_exist(state_data: StateContext, message: Message) -> bool:
    if state_data.data is None:
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, 'Пожалуйста повторите поиск аккаунта')
        return False
    return True


def _send_manga_account(callback_query: CallbackQuery, len_list_acc: int, acc_id: str, acc_name: str, photo_id: str,
                        index: int) -> None:
    photo_acc = get_photo_account(acc_id, photo_id)
    bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    bot.send_photo(callback_query.message.chat.id, photo=photo_acc,
                   caption=f'[{index + 1} из {len_list_acc}] Имя аккаунта: {acc_name}',
                   reply_markup=search_manga_acc_inline)
    bot.add_data(callback_query.message.chat.id, account_index=index)
