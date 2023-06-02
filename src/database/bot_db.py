from src.database.model_db import TelegramAccounts, MangaAccounts
from src.database.database_controller import DatabaseController

from sqlalchemy.orm import Session, DeclarativeBase
from sqlalchemy import select


class BotDB(DatabaseController):

    def _exists_account(self, account_id: int, table):
        with Session(self._engine) as session:
            query = select(table).where(table.account_id == account_id)
            res_execute = session.scalar(query)
            if res_execute is not None:
                return True

        return False

    def save_telegram_account(self, account_id: int, username: str, first_name: str, second_name):
        if not self._exists_account(account_id, TelegramAccounts):
            with Session(self._engine) as session:
                account = TelegramAccounts(account_id=account_id, username=username, first_name=first_name,
                                           second_name=second_name, active=True)
                session.add(account)
                session.commit()

    def save_manga_account(self, account_id: int, username: str):
        if not self._exists_account(account_id, MangaAccounts):
            with Session(self._engine) as session:
                account = MangaAccounts(account_id=account_id, username=username, active=True)
                session.add(account)
                session.commit()


if __name__ == '__main__':
    pass
