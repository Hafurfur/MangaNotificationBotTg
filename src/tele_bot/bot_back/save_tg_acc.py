from src.database import TelegramAccounts
from loader import Session_db
from src.logger.base_logger import log

from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError, DBAPIError
from sqlalchemy.dialects.sqlite import insert


def save_telegram_account(account_id: int, username: str, first_name: str, second_name: str) -> None:
    log.debug(f'{__name__}(account_id={account_id}, username={username}, first_name={first_name}, '
              f'second_name={second_name})')
    with Session_db() as session:
        try:
            stmt = insert(TelegramAccounts).values(account_id=account_id, username=username, first_name=first_name,
                                                   second_name=second_name, active=True)
            stmt = stmt.on_conflict_do_update(index_elements=[TelegramAccounts.account_id],
                                              set_=dict(username=username, first_name=first_name,
                                                        second_name=second_name, update_date=func.now()))
            log.debug(f'Запрос = {stmt}')

            session.execute(stmt)
            session.commit()
        except (SQLAlchemyError, DBAPIError) as error:
            log.error('Ошибка при сохранении телеграм аккаунта (SQLAlchemy)', exc_info=error)
            raise
        except Exception as error:
            log.error('Ошибка при сохранении телеграм аккаунта', exc_info=error)
            raise
