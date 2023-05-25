from src.database.model_db import Base, TelegramAccounts
from src.database.database_controller import DatabaseController

from sqlalchemy.orm import Session


class BotDB(DatabaseController):

    def _exists_account(self, account_id: int):
        with Session(self._engine) as session:
            query = session.query(TelegramAccounts).filter(TelegramAccounts.account_id == account_id)
            res = session.query(query.exists()).scalar()

        return res

    def new_account(self, account_id: int, username: str, tg_first_name: str, tg_second_name):
        if not self._exists_account(account_id):
            with Session(self._engine) as session:
                account = TelegramAccounts(account_id=account_id, username=username, tg_first_name=tg_first_name,
                                           tg_second_name=tg_second_name, active=True)
                session.add(account)
                session.commit()


if __name__ == '__main__':
    pass
