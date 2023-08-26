from src.database import TelegramAccounts
from loader import Session_db
from src.logger.base_logger import log

from sqlalchemy import update, func
from sqlalchemy.exc import SQLAlchemyError, DBAPIError


def switch_notification(status: str, tg_acc_id: int) -> None:
    log.info('Включение/выключение отправки уведомлений')
    log.debug(f'status={status}, tg_acc_id={tg_acc_id}')

    with Session_db() as session:
        try:
            stmt = update(TelegramAccounts).values(active=True if status == 'ON' else False,
                                                   update_date=func.now()).where(
                TelegramAccounts.account_id == tg_acc_id)
            log.debug(f'Запрос={stmt}')
            session.execute(stmt)
            session.commit()
        except (SQLAlchemyError, DBAPIError) as error:
            log.error('Ошибка при включение/выключение отправки уведомлений в БД (SQLAlchemy)', exc_info=error)
        except Exception as error:
            log.error('Ошибка при включение/выключение отправки уведомлений в БД', exc_info=error)
