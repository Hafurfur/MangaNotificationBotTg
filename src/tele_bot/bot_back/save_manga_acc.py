from src.database import MangaAccounts, TelegramAccounts, TrackedManga, MgAccountTrackedMgAssociationTable
from src.tele_bot.bot_back.site_data import get_readable_mg_acc
from loader import Session_db
from src.logger.base_logger import log

from sqlalchemy import select, update, func
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.exc import SQLAlchemyError, DBAPIError


def save_new_mg_acc(tg_acc_id: int, mg_acc_id: int, username: str) -> bool:
    log.info('Сохранение нового манга аккаунта')
    log.debug(f'tg_acc_id={tg_acc_id}, mg_acc_id={mg_acc_id}, username={username}')

    res_save_mg_acc = _save_mg_acc(tg_acc_id, mg_acc_id, username)

    if not res_save_mg_acc:
        return False

    readable_mg, list_mg_id, status_code = get_readable_mg_acc(mg_acc_id)
    if status_code != 200:
        log.debug(f'Ошибка при получении списка манги с сайта | status_code={status_code}')
        return False

    _save_new_tracked_manga(readable_mg)
    _link_mg_whit_acc(mg_acc_id, list_mg_id)

    return True


def _save_mg_acc(tg_acc_id: int, mg_acc_id: int, username: str) -> bool:
    log.debug(f'Сохранение манга аккаунта | tg_acc_id={tg_acc_id}, mg_acc_id={mg_acc_id}, username={username}')

    with Session_db() as session:
        try:
            stmt = insert(MangaAccounts).values(account_id=mg_acc_id, username=username, active=True)
            stmt = stmt.on_conflict_do_update(index_elements=[MangaAccounts.account_id],
                                              set_=dict(username=username, update_date=func.now()))

            log.debug(f'Запрос = {stmt}')
            session.execute(stmt)
            session.commit()
        except (SQLAlchemyError, DBAPIError) as error:
            log.error('Ошибка при сохранении манга аккаунта аккаунта в БД (SQLAlchemy)', exc_info=error)
            return False
        except Exception as error:
            log.error('Ошибка при сохранении манга аккаунта в БД', exc_info=error)
            return False

    result_update_tg_acc = _update_tg_account(tg_acc_id, mg_acc_id)
    return True if result_update_tg_acc else False


def _update_tg_account(tg_acc_id: int, mg_acc_id: int) -> bool:
    log.debug(f'Обновление манга аккаунта у телеграмм аккаунта в БД | tg_acc_id={tg_acc_id}, mg_acc_id={mg_acc_id}')

    with Session_db() as session:
        try:
            stmt = update(TelegramAccounts).where(TelegramAccounts.account_id == tg_acc_id).values(
                manga_account_id=mg_acc_id,
                update_date=func.now())

            log.debug(f'Запрос = {stmt}')
            session.execute(stmt)
            session.commit()
        except (SQLAlchemyError, DBAPIError) as error:
            log.error('Ошибка при обновлении данных телеграм аккаунта в БД (SQLAlchemy)', exc_info=error)
            return False
        except Exception as error:
            log.error('Ошибка при обновлении данных телеграм аккаунта в БД', exc_info=error)
            return False
    return True


def _save_new_tracked_manga(readable_mg: list[dict]) -> None:
    log.debug(f'Сохранение читаемой манги нового манга аккаунта')

    if not readable_mg:
        log.debug('Список новой отслеживаемой манги пуст')
        return

    mg_id_in_db = _get_mg_id_db()

    new_mg_list = []
    for manga in readable_mg:
        last_chapter = manga.get('last_chapter') if manga.get('last_chapter') else {}
        if manga.get('manga_id') not in mg_id_in_db:
            new_mg_list.append(dict(manga_id=manga.get('manga_id'), slug=manga.get('slug'),
                                    name_rus=manga.get('rus_name'), cover_id=manga.get('cover'),
                                    last_volume=last_chapter.get('volume'),
                                    last_chapter=last_chapter.get('number')))

    with Session_db() as session:
        try:
            stmt = insert(TrackedManga).values(new_mg_list)
            log.debug(f'Запрос = {stmt}')
            session.execute(stmt)
            session.commit()
        except (SQLAlchemyError, DBAPIError) as error:
            log.error('Ошибка при добавлении новой манги в БД (SQLAlchemy)', exc_info=error)
        except Exception as error:
            log.error('Ошибка при добавлении новой манги в БД', exc_info=error)


def _get_mg_id_db() -> set:
    log.debug(f'Получение всех slug отслеживаемой манги из ДБ')

    with Session_db() as session:
        try:
            stmt = select(TrackedManga.manga_id)
            log.debug(f'Запрос = {stmt}')
            result = set(session.scalars(stmt).all())
        except (SQLAlchemyError, DBAPIError) as error:
            log.error('Ошибка при получении списка новой отслеживаемой манги в БД (SQLAlchemy)', exc_info=error)
        except Exception as error:
            log.error('Ошибка при получении списка новой отслеживаемой манги в БД', exc_info=error)

    return result


def _link_mg_whit_acc(mg_acc_id: int, list_mg_id: set) -> None:
    log.debug(f'Связывание манга аккаунта с отслеживаемой мангой | mg_acc_id={mg_acc_id}, list_mg_id={list_mg_id}')

    if not list_mg_id:
        log.debug('Список читаемой манги у аккаунта пуст')
        return

    list_rd_mg = [{'mg_acc_id': mg_acc_id, 'tracked_mg_id': mg_id} for mg_id in list_mg_id]

    with Session_db() as session:
        try:
            stmt = insert(MgAccountTrackedMgAssociationTable).values(list_rd_mg)
            log.debug(f'Запрос = {stmt}')
            session.execute(stmt)
            session.commit()
        except (SQLAlchemyError, DBAPIError) as error:
            log.error('Ошибка при связывании манга аккаунта с читаемой мангой в БД (SQLAlchemy)', exc_info=error)
        except Exception as error:
            log.error('Ошибка при связывании манга аккаунта с читаемой мангой в БД', exc_info=error)
