from src.database import DatabaseController, TelegramAccounts, MangaAccounts

from sqlalchemy import select
from sqlalchemy.orm import Session


def having_manga_account(account_id: int) -> bool | str:
    engine = DatabaseController().get_engine()

    with Session(engine) as session:
        query = select(TelegramAccounts, MangaAccounts).join(MangaAccounts).where(
            TelegramAccounts.account_id == account_id)
        result = session.execute(query).scalar_one_or_none()

    return result.username if result else False
