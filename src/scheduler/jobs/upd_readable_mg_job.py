from loader import scheduler, db
from src.configs.settings import UPD_READABLE_MB_JOB_INTERVAL
from src.database.models import manga_accounts, tracked_manga, readable_manga
from src.tele_bot.bot_back.site_data import get_readable_mg_acc
from src.logger.base_logger import log

from sqlalchemy import select, delete, insert


@scheduler.scheduled_job('interval', hours=UPD_READABLE_MB_JOB_INTERVAL)
def udp_readable_mg() -> None:
    log.info('Старт задания обновления читаемой манги у манга аккаунтов')
    mg_accounts = _get_mg_acc_db()

    for mg_acc in mg_accounts:
        readable_mg_acc_site, readable_mg_id_site, status_code = get_readable_mg_acc(mg_acc)

        if status_code != 200:
            log.debug(f'Ошибка при получении списка манги с сайта | status_code={status_code}')
            continue

        if not readable_mg_acc_site:
            continue

        all_tracked_id_mg_db = _get_tracked_id_mg_db()
        readable_mg_acc_db = _get_readable_mg_acc_db(mg_acc)

        new_tracked_mg = _create_tracked_mg_list(readable_mg_acc_site, all_tracked_id_mg_db)
        del_readable_mg = readable_mg_acc_db.difference(readable_mg_id_site)
        new_readable_mg = readable_mg_id_site.difference(readable_mg_acc_db)

        _save_mew_tracked_mg(new_tracked_mg)
        _del_readable_mg(del_readable_mg, mg_acc)
        _sav_new_readable_mg(new_readable_mg, mg_acc)


def _save_mew_tracked_mg(manga: list[dict]) -> None:
    log.debug(f'Сохранение новой отслеживаемой манги в БД | manga={manga}')
    if not manga:
        log.debug('Список новой манги пуст')
        return

    stmt = insert(tracked_manga)
    db.insert(stmt, manga)


def _del_readable_mg(del_manga: set, mg_acc_id: int) -> None:
    log.debug(f'Удаление читаемой манги у манга аккаунта из БД | del_manga={del_manga}, mg_acc_id={mg_acc_id}')

    if not del_manga:
        log.debug('Список удаляемой читаемой манги у аккаунта пуст')
        return

    stmt = delete(readable_manga).where(
        readable_manga.c.mg_acc_id == mg_acc_id).where(
        readable_manga.c.tracked_mg_id.in_(del_manga))

    db.delete(stmt)


def _sav_new_readable_mg(new_readable_mg: set, mg_acc_id: int) -> None:
    log.debug(f'Сохранении новой читаемой манги у манга аккаунта в БД | '
              f'new_readable_mg={new_readable_mg}, mg_acc_id={mg_acc_id}')

    if not new_readable_mg:
        log.debug('Список новой читаемой манги у аккаунта пуст')
        return

    list_rd_mg = [{'mg_acc_id': mg_acc_id, 'tracked_mg_id': mg_id} for mg_id in new_readable_mg]
    stmt = insert(readable_manga)
    db.insert(stmt, list_rd_mg)


def _create_tracked_mg_list(readable_mg_acc_site: list[dict], all_tracked_mg_db: set) -> list[dict]:
    log.debug(f'Создание списка отслеживаемой манги')

    result = []

    for site_manga in readable_mg_acc_site:
        if site_manga.get('manga_id') not in all_tracked_mg_db:
            last_chapter = site_manga.get('last_chapter') if site_manga.get('last_chapter') else {}

            data = {'id': site_manga.get('manga_id'), 'slug': site_manga.get('slug'),
                    'name_rus': site_manga.get('rus_name'), 'cover_id': site_manga.get('cover'),
                    'last_volume': last_chapter.get('volume'), 'last_chapter': last_chapter.get('number')}

            result.append(data)

    return result


def _get_mg_acc_db() -> set:
    log.debug(f'Получение всех манга аккаунтов из ДБ')

    stmt = select(manga_accounts.c.id)
    result = set(db.select(stmt).scalars().all())
    return result


def _get_tracked_id_mg_db() -> set:
    log.debug(f'Получение всех id отслеживаемой манги из ДБ')

    stmt = select(tracked_manga.c.id)
    result = set(db.select(stmt).scalars().all())
    return result


def _get_readable_mg_acc_db(mg_acc_id: int) -> set:
    log.debug(f'Получение всей читаемой манги у манга аккаунта из ДБ | mg_acc_id={mg_acc_id}')

    stmt = select(readable_manga.c.tracked_mg_id).join(manga_accounts).where(
        manga_accounts.c.id == mg_acc_id)

    result = set(db.select(stmt).scalars().all())
    return result
