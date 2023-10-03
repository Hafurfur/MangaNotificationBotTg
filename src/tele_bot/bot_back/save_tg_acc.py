from datetime import datetime

from src.database import telegram_accounts
from loader import db
from src.logger.base_logger import log


def save_telegram_account(account_id: int, username: str, first_name: str, second_name: str) -> None:
    log.info('Сохранение телеграмм аккаунта в БД')
    log.debug(f'id={account_id}, username={username}, first_name={first_name}, second_name={second_name}')

    data = {'insert_data': {'id': account_id, 'username': username, 'first_name': first_name,
                            'second_name': second_name, 'active': True},
            'update_data': {'update_date': datetime.utcnow(), 'username': username, 'first_name': first_name,
                            'second_name': second_name, 'active': True}}

    db.insert_on_conflict_do_update(telegram_accounts, telegram_accounts.c.id, data)
