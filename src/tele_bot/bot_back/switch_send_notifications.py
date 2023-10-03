from datetime import datetime
from src.database import telegram_accounts
from loader import db
from src.logger.base_logger import log

from sqlalchemy import update


def switch_notification(status: str, tg_acc_id: int) -> None:
    log.info('Включение/выключение отправки уведомлений')
    log.debug(f'status={status}, tg_acc_id={tg_acc_id}')

    upd_date = {'active': True if status == 'ON' else False,
                'update_date': datetime.utcnow()}

    stmt = update(telegram_accounts).where(telegram_accounts.c.id == tg_acc_id)
    db.update(stmt, upd_date)
