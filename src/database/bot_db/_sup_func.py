from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database import DatabaseController


def _exists_account(account_id: int, table) -> bool:
    engine = DatabaseController().get_engine()

    with Session(engine) as session:
        query = select(table).where(table.account_id == account_id)
        res_execute: table = session.scalar(query)

    return True if res_execute else False
