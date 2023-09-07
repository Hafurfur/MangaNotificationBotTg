from src.database import TrackedManga
from src.scheduler.jobs.new_chapters.manga import Manga
from loader import Session_db
from src.logger.base_logger import log
from os import getenv
from datetime import datetime

import requests
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException
from bs4 import BeautifulSoup
from sqlalchemy import select, update, bindparam
from sqlalchemy.exc import SQLAlchemyError, DBAPIError


def get_new_manga_chapters() -> list[Manga]:
    log.info('Старт получение новых глав манги')

    manga_data_db = _get_manga_data_db()
    soup_data = _get_soup_data()

    if not manga_data_db or not soup_data:
        log.debug('Нет данных манги из ДБ или не получен суп с сайта')
        return []

    soup_all_new_releases = soup_data.find_all(class_='updates__item')
    all_new_releases = []
    for release in soup_all_new_releases:
        new_release_slug = release.find(class_='link-default').attrs.get('href').split('/')[-1]

        if new_release_slug in manga_data_db:
            last_mg_chapter = manga_data_db.get(new_release_slug)
            new_release = Manga.maga_builder(release, last_mg_chapter)

            if new_release.chapters:
                all_new_releases.append(new_release)

    if all_new_releases:
        _update_last_mg_chapter_db(all_new_releases)

    log.debug(f'Список новой манги с главами={all_new_releases}')
    return all_new_releases


def _get_soup_data() -> BeautifulSoup | None:
    log.debug(f'Получение супа с https://mangalib.me')

    try:
        if not getenv("REMEMBER_WEB") or not getenv("REMEMBER_WEB_VALUE"):
            log.error('Не указаны данные куки')
            raise

        cookies = {
            getenv("REMEMBER_WEB"): getenv("REMEMBER_WEB_VALUE"),
            'User-Agent': 'python-requests/2.30.0',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept': '*/*',
            'Connection': 'keep-alive'}

        response = requests.get('https://mangalib.me', cookies=cookies)
        response.raise_for_status()
    except (HTTPError, ConnectionError, Timeout, RequestException) as error:
        log.error('Ошибка при получении супа для парсинга (requests)', exc_info=error)
        return
    except Exception as error:
        log.error('Ошибка при получении манга аккаунта', exc_info=error)
        return

    return BeautifulSoup(response.text, 'lxml')


def _get_manga_data_db() -> dict:
    log.debug(f'Получение манги отслеживаемой манги из БД в виде словаря')

    with Session_db() as session:
        try:
            stmt = select(TrackedManga.slug, TrackedManga.last_volume, TrackedManga.last_chapter)
            log.debug(f'Запрос = {stmt}')
            result = session.execute(stmt).mappings().all()
        except (SQLAlchemyError, DBAPIError) as error:
            log.error('Ошибка при получении списка манги из БД (SQLAlchemy)', exc_info=error)
            raise
        except Exception as error:
            log.error('Ошибка при получении списка манги', exc_info=error)
            raise

    manga_data_db: dict = {}

    for item in result:
        manga_data_db[item.get('slug')] = {'last_volume': item.get('last_volume') if item.get('last_volume') else 0,
                                           'last_chapter': item.get('last_chapter') if item.get('last_chapter') else 0}

    return manga_data_db


def _update_last_mg_chapter_db(all_new_releases: list[Manga]) -> None:
    log.debug(f'Обновление номеров последних глав манги в БД. all_new_releases={all_new_releases}')
    set_data: list = []

    for release in all_new_releases:
        data = {'col_slug': release.slug,
                'update_date': datetime.utcnow(),
                'last_volume': release.chapters[0].volume,
                'last_chapter': release.chapters[0].number}
        set_data.append(data)

    with Session_db() as session:
        try:
            stmt = update(TrackedManga).where(TrackedManga.slug == bindparam('col_slug'))

            log.debug(f'Запрос = {stmt}')
            session.connection().execute(stmt, set_data)
            session.commit()
        except (SQLAlchemyError, DBAPIError) as error:
            log.error('Ошибка при обновлении данных в БД (SQLAlchemy)', exc_info=error)
            raise
        except Exception as error:
            log.error('Ошибка при обновлении данных в БД', exc_info=error)
            raise
