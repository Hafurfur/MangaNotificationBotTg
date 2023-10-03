from datetime import datetime

from src.database import manga_accounts, telegram_accounts, tracked_manga, readable_manga
from src.tele_bot.bot_back.site_data import get_readable_mg_acc
from loader import db
from src.logger.base_logger import log

from sqlalchemy import select, update, func, insert

def save_new_mg_acc(tg_acc_id: int, mg_acc_id: int, username: str) -> bool:
    log.info('Сохранение нового манга аккаунта')
    log.debug(f'tg_acc_id={tg_acc_id}, mg_acc_id={mg_acc_id}, username={username}')

    res_save_mg_acc = _save_mg_acc(tg_acc_id, mg_acc_id, username)

    if not res_save_mg_acc:
        return False

    readable_mg_acc_site, readable_mg_id_site, status_code = get_readable_mg_acc(mg_acc_id)
    if status_code != 200:
        log.debug(f'Ошибка при получении списка манги с сайта | status_code={status_code}')
        return False

    _save_new_tracked_manga(readable_mg_acc_site)
    _link_mg_whit_acc(mg_acc_id, readable_mg_id_site)

    return True


def _save_mg_acc(tg_acc_id: int, mg_acc_id: int, username: str) -> bool:
    log.debug(f'Сохранение манга аккаунта | tg_acc_id={tg_acc_id}, mg_acc_id={mg_acc_id}, username={username}')

    data = {'insert_data': {'id': mg_acc_id, 'username': username, 'active': True},
            'update_data': {'update_date': func.now(), 'username': username, 'active': True}}

    db.insert_on_conflict_do_update(manga_accounts, manga_accounts.c.id, data)

    result_update_tg_acc = _update_tg_account(tg_acc_id, mg_acc_id)
    return True if result_update_tg_acc else False


def _update_tg_account(tg_acc_id: int, mg_acc_id: int) -> bool:
    log.debug(f'Обновление манга аккаунта у телеграмм аккаунта в БД | tg_acc_id={tg_acc_id}, mg_acc_id={mg_acc_id}')

    upd_data = {'manga_account_id': mg_acc_id, 'update_date': datetime.utcnow()}
    stmt = update(telegram_accounts).where(telegram_accounts.c.id == tg_acc_id)
    db.update(stmt, upd_data)
    return True


def _save_new_tracked_manga(readable_mg_acc_site: list[dict]) -> None:
    log.debug(f'Сохранение читаемой манги нового манга аккаунта')

    if not readable_mg_acc_site:
        log.debug('Список новой отслеживаемой манги пуст')
        return

    all_tracked_id_mg_db = _get_tracked_mg_db()
    insert_data = []

    for site_manga in readable_mg_acc_site:
        if site_manga.get('manga_id') not in all_tracked_id_mg_db:
            last_chapter = site_manga.get('last_chapter') if site_manga.get('last_chapter') else {}

            data = {'id': site_manga.get('manga_id'), 'slug': site_manga.get('slug'),
                    'name_rus': site_manga.get('rus_name'), 'cover_id': site_manga.get('cover'),
                    'last_volume': last_chapter.get('volume'), 'last_chapter': last_chapter.get('number')}

            insert_data.append(data)

    stmt = insert(tracked_manga)
    db.insert(stmt, insert_data)


def _get_tracked_mg_db() -> set:
    log.debug(f'Получение всех id отслеживаемой манги из ДБ')

    stmt = select(tracked_manga.c.id)
    result = set(db.select(stmt).scalars().all())
    return result


def _link_mg_whit_acc(mg_acc_id: int, list_mg_id: set) -> None:
    log.debug(f'Связывание манга аккаунта с отслеживаемой мангой | mg_acc_id={mg_acc_id}, list_mg_id={list_mg_id}')

    if not list_mg_id:
        log.debug('Список читаемой манги у аккаунта пуст')
        return
    list_rd_mg = [{'mg_acc_id': mg_acc_id, 'tracked_mg_id': mg_id} for mg_id in list_mg_id]

    stmt = insert(readable_manga)
    db.insert(stmt, list_rd_mg)
