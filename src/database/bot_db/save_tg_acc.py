from src.database import TelegramAccounts, DatabaseController
from src.database.bot_db._sup_func import _exists_account

from sqlalchemy.orm import Session


def save_telegram_account(account_id: int, username: str, first_name: str, second_name) -> None:
    if not _exists_account(account_id, TelegramAccounts):
        engine = DatabaseController().get_engine()

        with Session(engine) as session:
            account = TelegramAccounts(account_id=account_id, username=username, first_name=first_name,
                                       second_name=second_name, active=True)
            session.add(account)
            session.commit()
