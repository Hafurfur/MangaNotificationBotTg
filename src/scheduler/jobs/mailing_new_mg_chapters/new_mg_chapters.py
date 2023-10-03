from __future__ import annotations
from os import getenv
from dataclasses import dataclass
from loader import db
from src.database import tracked_manga
from src.logger.base_logger import log

import requests
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException
from bs4 import BeautifulSoup
from sqlalchemy import select


@dataclass
class Manga:
    id: int
    name: str
    slug: str
    chapters: list[Chapter]


@dataclass
class Chapter:
    url: str
    volume: int
    number: float


def get_new_manga_chapters(address_site: str) -> list[Manga]:
    log.info(f'Получение новых глав манги c сайта {address_site}')

    soup_site_data = _get_soup_data(address_site)
    if not soup_site_data:
        log.debug('Нет данных с сайта')
        return []

    tracked_manga_db = _get_tracked_manga_db()
    if not tracked_manga_db:
        log.debug('Нет данных из ДБ')
        return []

    new_releases = []
    all_new_releases_soup = soup_site_data.find_all(class_='updates__item')
    for release in all_new_releases_soup:
        new_release_slug = release.find(class_='link-default').attrs.get('href').split('/')[-1]

        if new_release_slug in tracked_manga_db and _check_new_chapters(release, tracked_manga_db):
            new_releases.append(_create_mg_obj(release, tracked_manga_db))

    log.debug(f'Список новой манги с главами={new_releases}')
    return new_releases


def _get_soup_data(address_site: str) -> BeautifulSoup | None:
    log.debug(f'Получение супа с {address_site}')

    try:
        cookies = {
            getenv("REMEMBER_WEB"): getenv("REMEMBER_WEB_VALUE"),
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/114.0.0.0 YaBrowser/23.7.5.704 Yowser/2.5 Safari/537.36',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept': '*/*',
            'Connection': 'keep-alive'}

        response = requests.get(address_site, cookies=cookies)
        response.raise_for_status()
    except (HTTPError, ConnectionError, Timeout, RequestException) as error:
        log.error('Ошибка при получении супа (requests)', exc_info=error)
        return
    except Exception as error:
        log.error('Ошибка при получении супа', exc_info=error)
        return

    result = BeautifulSoup(response.text, 'lxml')

    return result


def _get_tracked_manga_db() -> dict:
    log.debug(f'Получение отслеживаемой манги из БД')

    stmt = select(tracked_manga.c.id, tracked_manga.c.slug, tracked_manga.c.last_volume,
                  tracked_manga.c.last_chapter)
    result = db.select(stmt)

    tracked_manga_db: dict = {}
    for item in result:
        tracked_manga_db[item.slug] = {'id': item.id, 'last_volume': item.last_volume,
                                       'last_chapter': item.last_chapter}
    return tracked_manga_db


def _check_new_chapters(release, tracked_manga_db) -> bool:
    slug = release.find(class_='link-default').attrs.get('href').split('/')[-1]
    last_chapter = release.find(class_='updates__chapter')
    chapter_number = last_chapter.find(class_='updates__chapter-vol').text.split(' ')
    result = True if float(chapter_number[3]) > tracked_manga_db[slug].get('last_chapter') else False

    return result


def _create_mg_obj(release, tracked_manga_db) -> Manga:
    log.debug('Создание манги c новыми главами')

    name = release.find(class_='link-default').text
    slug = release.find(class_='link-default').attrs.get('href').split('/')[-1]
    all_new_chapters_soup = release.find_all(class_='updates__chapter')
    chapters: list[Chapter] = []

    for chapter in all_new_chapters_soup:
        chapter_number = chapter.find(class_='updates__chapter-vol').text.split(' ')
        volume = int(chapter_number[1])
        number = float(chapter_number[3])
        url = chapter.attrs.get('href').split('&ui')[0].split('?ui')[0]

        if number > tracked_manga_db[slug].get('last_chapter') and volume >= tracked_manga_db[slug].get('last_volume'):
            chapters.append(Chapter(url=url, volume=volume, number=number))

    result = Manga(id=tracked_manga_db[slug].get('id'), name=name, slug=slug, chapters=chapters)

    return result
