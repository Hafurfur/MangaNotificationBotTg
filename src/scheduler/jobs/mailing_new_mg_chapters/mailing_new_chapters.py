from datetime import datetime
from pathlib import Path
from src.configs.settings import MAILING_JOB_INTERVAL
from src.scheduler.jobs.mailing_new_mg_chapters.new_mg_chapters import get_new_manga_chapters, Manga
from src.database.models import tracked_manga, manga_accounts, telegram_accounts, readable_manga
from src.logger.base_logger import log
from loader import bot, scheduler, db
from time import sleep

from requests import get
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException
from sqlalchemy import select, update, bindparam
from telebot.apihelper import ApiException


@scheduler.scheduled_job('interval', minutes=MAILING_JOB_INTERVAL)
def mailing_new_chapters_job() -> None:
    log.info('Начало задания на отправку уведомлений о выходе новых глав')

    releases = get_new_manga_chapters('https://mangalib.me')

    if not releases:
        return
    _update_last_mg_chapter_db(releases)

    for release in releases:
        # Получение телеграмм аккаунтов и id обложки манги
        send_data = _get_send_data(release.slug)
        cover = _get_cover_data(release.slug, send_data[0].get('cover_id'))
        for chapter in release.chapters[::-1]:
            for count, data in enumerate(send_data, start=1):
                if count % 30 == 0:
                    sleep(1)
                _send_release_in_tg(release.name, chapter.volume, chapter.number, chapter.url, cover,
                                    data.get('id'))
            sleep(1)


def _get_send_data(manga_slug: str) -> list[dict]:
    log.debug(f'Получение телеграмм аккаунтов и id обложки манги из ДБ | manga_slug={manga_slug}')

    stmt = select(telegram_accounts.c.id, tracked_manga.c.cover_id).join_from(tracked_manga, readable_manga).join_from(
        readable_manga, manga_accounts).join_from(manga_accounts, telegram_accounts).where(
        tracked_manga.c.slug == manga_slug).where(telegram_accounts.c.active.is_(True))
    result = db.select(stmt).mappings().all()

    return result


def _get_cover_data(manga_slug: str, cover_id: str) -> bytes:
    log.debug(f'Получение обложки манги | manga_slug={manga_slug}, send_data={cover_id}')

    try:
        response = get(f'https://cover.imglib.info/uploads/cover/{manga_slug}/cover/{cover_id}_250x350.jpg')
        response.raise_for_status()
    except (HTTPError, ConnectionError, Timeout, RequestException) as error:
        log.error('Ошибка при получении обложки манги (requests)', exc_info=error)
        return _get_placeholder_cover()
    except Exception as error:
        log.error('Ошибка при получении обложки манги', exc_info=error)
        return _get_placeholder_cover()

    result = response.content
    return result


def _get_placeholder_cover() -> bytes:
    log.debug(f'Получение заглушки обложки манга')
    placeholder_path = Path.joinpath(Path.cwd(), r'.\pr_data\images\placeholder_cover.png')
    with open(placeholder_path, 'rb') as fr:
        return fr.read()


def _send_release_in_tg(manga_name: str, chap_vol: int, chap_num: float, chap_url: str, cover: bytes,
                        tg_id: int) -> None:
    log.debug(f'Отправка сообщения с новой главой | manga_name={manga_name}, chap_vol={chap_vol}, '
              f'chap_num={chap_num}, chap_url={chap_url}, tg_id={tg_id}')
    try:
        bot.send_photo(tg_id, photo=cover, caption=f'{manga_name}\nТом {chap_vol} глава '
                                                   f'{int(chap_num) if chap_num % 1 == 0 else chap_num}\n\n{chap_url}')
    except ApiException as error:
        log.error('Ошибка при отправке фотографии (telebot)', exc_info=error)
    except Exception as error:
        log.error('Ошибка при отправке фотографии', exc_info=error)


def _update_last_mg_chapter_db(all_new_releases: list[Manga]) -> None:
    log.debug(f'Обновление номеров последних глав манги в БД. all_new_releases={all_new_releases}')
    update_data: list = []

    for release in all_new_releases:
        data = {'_id': release.id,
                'slug': release.slug,
                'update_date': datetime.utcnow(),
                'last_volume': release.chapters[0].volume,
                'last_chapter': release.chapters[0].number}
        update_data.append(data)

    stmt = update(tracked_manga).where(tracked_manga.c.id == bindparam('_id'))
    db.update(stmt, update_data)
