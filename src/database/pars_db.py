from src.database.database_controller import DatabaseController
from src.database.models.tracked_manga import TrackedManga

from sqlalchemy.orm import Session
from sqlalchemy import select

class ParsBD(DatabaseController):


    def _exists_account(self, account_id: int, table):
        with Session(self._engine) as session:
            query = select(table).where(table.account_id == account_id)
            res_execute = session.scalar(query)
            if res_execute is not None:
                return True

        return False

    def save_manga(self, manga_id: str, slug: str, name_rus: str, cover_url:str):

        print()


if __name__ == '__main__':
    pass
