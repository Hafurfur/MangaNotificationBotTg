from settings import TOKEN
from src.database.bot_db import BotDB
from src.parser.search_manga_account import SearchMangaAccount
from src.tele_bot.inline_buttons import search_manga_acc_inline

from telebot import TeleBot
from telebot.types import Message, CallbackQuery
from telebot.storage import StateContext

bot = TeleBot(token=TOKEN, skip_pending=True)


@bot.message_handler(commands=['start'])
def start(message: Message):
    db = BotDB()
    db.save_telegram_account(message.from_user.id, message.from_user.username,
                             message.from_user.first_name, message.from_user.last_name)
    bot.send_message(message.chat.id, f'Добро пожаловать {message.from_user.first_name}!\nС этого момента бот сможет '
                                      f'присылать уведомления о выходе новых главах манги с сайта mangalib.\nЧто бы '
                                      f'получать уведомления нужно через команду /add_mangalib_account "имя аккаунта" '
                                      f'добавить аккаунт с сайта mangalib или через команду /add_manga "название '
                                      f'манги на русском" добавить интересующую мангу.\nПри добавлении аккаунта '
                                      f'будут приходить уведомления для манги из вкладки "Читаю".\nКак выйдет новая '
                                      f'глава бот вам её пришлет.')


@bot.message_handler(commands=['add_mangalib_account'])
def new_manga_account(message: Message):
    result_search = SearchMangaAccount().search_account(message.text)
    bot.set_state(message.from_user.id, 'add_mangalib_account', message.chat.id)

    if result_search is None:
        bot.send_message(message.chat.id, 'Аккаунт не найден\nПопробуйте еще раз, возможно была '
                                          'допущена ошибка в имени аккаунта')
        bot.delete_state(message.from_user.id, message.chat.id)
    else:
        bot.add_data(message.from_user.id, message.chat.id, accounts=result_search, account_index=0)
        bot.send_photo(message.chat.id, photo=result_search[0]['avatar'],
                       caption=f'[1 из {len(result_search)}] Имя аккаунта: {result_search[0]["value"]}',
                       reply_markup=search_manga_acc_inline)


@bot.callback_query_handler(func=lambda call: call.data.endswith('manga_acc'))
def manga_account_choice(callback_query: CallbackQuery):
    result_search: StateContext = bot.retrieve_data(callback_query.from_user.id, callback_query.message.chat.id)

    if result_search.data is None:
        bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
        bot.send_message(callback_query.message.chat.id, 'Пожалуйста повторите поиск аккаунта')
        return

    accounts: list = result_search.data['accounts']
    account_index: int = result_search.data['account_index']

    if callback_query.data == 'prev_manga_acc' and account_index > 0:
        account_index -= 1
        _send_manga_account(callback_query, len(accounts), accounts[account_index]["value"], account_index,
                            accounts[account_index]['avatar'])

    elif callback_query.data == 'next_manga_acc' and (account_index < len(accounts) - 1):
        account_index += 1
        _send_manga_account(callback_query, len(accounts), accounts[account_index]["value"], account_index,
                            accounts[account_index]['avatar'])

    elif callback_query.data == 'add_manga_acc':
        bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
        bot.delete_state(callback_query.from_user.id, callback_query.message.chat.id)
        BotDB().save_manga_account(accounts[account_index]['id'], accounts[account_index]['value'])
        bot.send_message(callback_query.message.chat.id,
                         f'Аккаунт {accounts[account_index]["value"]} был добавлен в отслеживание')

    elif callback_query.data == 'cancel_search_manga_acc':
        bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
        bot.delete_state(callback_query.from_user.id, callback_query.message.chat.id)
    else:
        bot.answer_callback_query(callback_query.id)


def _send_manga_account(callback_query: CallbackQuery, len_list_acc: int, name: str, index: int, photo: bytes):
    bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    bot.send_photo(callback_query.message.chat.id, photo=photo,
                   caption=f'[{index + 1} из {len_list_acc}] Имя аккаунта: {name}',
                   reply_markup=search_manga_acc_inline)
    bot.add_data(callback_query.from_user.id, callback_query.message.chat.id, account_index=index)

    pass


bot.infinity_polling()

if __name__ == '__main__':
    # mess('334496904')
    pass
