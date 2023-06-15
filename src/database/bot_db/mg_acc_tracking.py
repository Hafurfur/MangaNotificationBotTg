from src.database import MangaAccounts, DatabaseController, TelegramAccounts, TrackedManga
from src.database.bot_db._sup_func import _exists_account
from src.site_data.search_manga import get_readable_mg_acc

from sqlalchemy import select, update
from sqlalchemy.orm import Session


def add_account_tracking(tg_acc_id: int, mg_acc_id: int, username: str) -> None:
    readable_mg, set_mg_id = get_readable_mg_acc(mg_acc_id)
    _save_manga_account(tg_acc_id, mg_acc_id, username)
    _save_new_manga(readable_mg)
    _link_mg_whit_acc(mg_acc_id, set_mg_id)


def _save_manga_account(tg_account_id: int, mg_account_id: int, username: str) -> None:
    if not _exists_account(mg_account_id, MangaAccounts):
        engine = DatabaseController().get_engine()

        with Session(engine) as session:
            manga_account = MangaAccounts(account_id=mg_account_id, username=username, active=True)
            session.add(manga_account)
            session.commit()

    _update_tg_account(tg_account_id, mg_account_id)


def _update_tg_account(tg_account_id: int, mg_account_id: int) -> None:
    engine = DatabaseController().get_engine()

    with Session(engine) as session:
        update_tg_account_query = update(TelegramAccounts).where(
            TelegramAccounts.account_id == tg_account_id).values(manga_account_id=mg_account_id)

        session.execute(update_tg_account_query)
        session.commit()


def _save_new_manga(readable_mg: list[dict]) -> None:
    engine = DatabaseController().get_engine()
    mg_id_in_db = _get_mg_id_in_db()

    with Session(engine) as session:
        for manga in readable_mg:
            if manga['manga_id'] not in mg_id_in_db:
                session.add(TrackedManga(manga_id=manga['manga_id'], slug=manga['slug'], name_rus=manga['rus_name'],
                                         cover_id=manga['cover']))
        session.commit()


def _get_mg_already_exist(set_mg_id: set) -> list[TrackedManga]:
    engine = DatabaseController().get_engine()

    with Session(engine) as session:
        query = select(TrackedManga).where(TrackedManga.manga_id.in_(set_mg_id))
        result = list(session.scalars(query).all())

    return result


def _get_mg_id_in_db() -> set:
    engine = DatabaseController().get_engine()

    with Session(engine) as session:
        query = select(TrackedManga.manga_id)
        result = set(session.scalars(query).all())

    return result


def _link_mg_whit_acc(mg_account_id: int, set_mg_id: set) -> None:
    engine = DatabaseController().get_engine()
    mg_in_db = _get_mg_already_exist(set_mg_id)

    with Session(engine) as session:
        mg_acc: MangaAccounts = session.scalar(
            select(MangaAccounts).where(MangaAccounts.account_id == mg_account_id))

        mg_acc.readable_manga.extend(mg_in_db)

        session.commit()
