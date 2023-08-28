from loader import scheduler, Session_db
from src.database.models import MangaAccounts, TrackedManga, MgAccountTrackedMgAssociationTable
from src.tele_bot.bot_back.site_data import get_readable_mg_acc
from src.logger.base_logger import log

from sqlalchemy import select, delete, insert
from sqlalchemy.exc import SQLAlchemyError, DBAPIError


@scheduler.scheduled_job('interval', hours=1)
def udp_readable_mg() -> None:
    log.info('Старт джобы обновления читаемой манги у манга аккаунтов')
    mg_accounts = _get_mg_acc_db()

    for mg_acc in mg_accounts:
        readable_mg_acc_site, readable_mg_id_site, status_code = get_readable_mg_acc(mg_acc)

        if status_code != 200:
            log.debug(f'Ошибка при получении списка манги с сайта | status_code={status_code}')
            continue

        all_tracked_mg = _get_tracked_mg_db()
        readable_mg_acc_db = _get_readable_mg_acc_db(mg_acc)

        new_tracked_mg = [_create_tracked_mg(manga) for manga in readable_mg_acc_site
                          if manga.get('manga_id') not in all_tracked_mg]
        del_readable_mg = readable_mg_acc_db.difference(readable_mg_id_site)
        new_readable_mg = readable_mg_id_site.difference(readable_mg_acc_db)

        _save_mew_tracked_mg(new_tracked_mg)
        _del_readable_mg(del_readable_mg, mg_acc)
        _sav_new_readable_mg(new_readable_mg, mg_acc)


def _save_mew_tracked_mg(manga: list) -> None:
    log.debug(f'Сохранение новой отслеживаемой манги в БД | manga={manga}')
    if not manga:
        log.debug('Список новой манги пуст')
        return

    with Session_db() as session:
        try:
            session.add_all(manga)
            session.commit()
        except (SQLAlchemyError, DBAPIError) as error:
            log.error('Ошибка при сохранении новой отслеживаемой манги в БД (SQLAlchemy)', exc_info=error)
            raise
        except Exception as error:
            log.error('Ошибка при сохранении новой отслеживаемой манги в БД', exc_info=error)
            raise


def _del_readable_mg(del_manga: set, mg_acc_id: int) -> None:
    log.debug(f'Удаление читаемой манги у манга аккаунта из БД | del_manga={del_manga}, mg_acc_id={mg_acc_id}')

    if not del_manga:
        log.debug('Список удаляемой читаемой манги у аккаунта пуст')
        return

    with Session_db() as session:
        try:
            stmt = delete(MgAccountTrackedMgAssociationTable).where(
                MgAccountTrackedMgAssociationTable.mg_acc_id == mg_acc_id).where(
                MgAccountTrackedMgAssociationTable.tracked_mg_id.in_(del_manga))

            log.debug(f'Запрос = {stmt}')
            session.execute(stmt)
            session.commit()
        except (SQLAlchemyError, DBAPIError) as error:
            log.error('Ошибка при удаление читаемой манги у манга аккаунта из ДБ (SQLAlchemy)', exc_info=error)
            raise
        except Exception as error:
            log.error('Ошибка при удаление читаемой манги у манга аккаунта из ДБ', exc_info=error)
            raise


def _sav_new_readable_mg(new_readable_mg: set, mg_acc_id: int) -> None:
    log.debug(f'Сохранении новой читаемой манги у манга аккаунта в БД | '
              f'new_readable_mg={new_readable_mg}, mg_acc_id={mg_acc_id}')

    if not new_readable_mg:
        log.debug('Список новой читаемой манги у аккаунта пуст')
        return

    list_rd_mg = [{'mg_acc_id': mg_acc_id, 'tracked_mg_id': mg_id} for mg_id in new_readable_mg]

    with Session_db() as session:
        try:
            stmt = insert(MgAccountTrackedMgAssociationTable).values(list_rd_mg)
            log.debug(f'Запрос = {stmt}')
            session.execute(stmt)
            session.commit()
        except (SQLAlchemyError, DBAPIError) as error:
            log.error('Ошибка при сохранении новой читаемой манги у манга аккаунта в ДБ (SQLAlchemy)', exc_info=error)
            raise
        except Exception as error:
            log.error('Ошибка при сохранении новой читаемой манги у манга аккаунта в ДБ', exc_info=error)
            raise


def _create_tracked_mg(data: dict) -> TrackedManga:
    log.debug(f'Создание объектов отслеживаемой манги | data={data}')

    last_chapter = data.get('last_chapter') if data.get('last_chapter') else {}

    return TrackedManga(manga_id=data.get('manga_id'), slug=data.get('slug'), name_rus=data.get('rus_name'),
                        cover_id=data.get('cover'), last_volume=last_chapter.get('volume'),
                        last_chapter=last_chapter.get('number'))


def _get_mg_acc_db() -> set:
    log.debug(f'Получение всех манга аккаунтов из ДБ')
    with Session_db() as session:
        try:
            stmt = select(MangaAccounts.account_id)
            log.debug(f'Запрос = {stmt}')
            result = session.scalars(stmt).all()
        except (SQLAlchemyError, DBAPIError) as error:
            log.error('Ошибка при всех манга аккаунтов из ДБ (SQLAlchemy)', exc_info=error)
            raise
        except Exception as error:
            log.error('Ошибка при всех манга аккаунтов из ДБ', exc_info=error)
            raise

    return set(result)


def _get_tracked_mg_db() -> set:
    log.debug(f'Получение всей отслеживаемой манги из ДБ')
    with Session_db() as session:
        stmt = select(TrackedManga.manga_id)
        result = session.scalars(stmt).all()

        try:
            stmt = select(TrackedManga.manga_id)
            log.debug(f'Запрос = {stmt}')
            result = session.scalars(stmt).all()
        except (SQLAlchemyError, DBAPIError) as error:
            log.error('Ошибка при получение всей отслеживаемой манги из ДБ (SQLAlchemy)', exc_info=error)
            raise
        except Exception as error:
            log.error('Ошибка при получение всей отслеживаемой манги из ДБ', exc_info=error)
            raise

    return set(result)


def _get_readable_mg_acc_db(mg_acc_id: int) -> set:
    log.debug(f'Получение всей читаемой манги у манга аккаунта из ДБ | mg_acc_id={mg_acc_id}')
    with Session_db() as session:
        try:
            stmt = select(TrackedManga.manga_id).join(MangaAccounts.readable_manga).where(
                MangaAccounts.account_id == mg_acc_id)
            log.debug(f'Запрос = {stmt}')
            result = session.scalars(stmt).all()
        except (SQLAlchemyError, DBAPIError) as error:
            log.error('Ошибка при получение всей читаемой манги у манга аккаунта из ДБ (SQLAlchemy)', exc_info=error)
            raise
        except Exception as error:
            log.error('Ошибка при получение всей читаемой манги у манга аккаунта из ДБ', exc_info=error)
            raise

    return set(result)
