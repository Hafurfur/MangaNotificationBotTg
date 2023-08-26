from pathlib import Path

from src.scheduler.jobs.new_chapters.new_mg_chapters import get_new_manga_chapters
from src.database import TrackedManga, MangaAccounts, TelegramAccounts
from loader import Session_db, bot, scheduler
from src.logger.base_logger import log
from time import sleep

from requests import get
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError, DBAPIError
from telebot.apihelper import ApiException


@scheduler.scheduled_job('interval', minutes=5)
def send_notif_new_chapters() -> None:
    log.info('Старт джобы на отправку уведомлений о выходе новых глав')
    releases = get_new_manga_chapters()

    for release in releases:
        # Получение телеграмм аккаунта и id обложки манги
        send_data = _get_send_data(release.slug)
        cover = _get_cover_data(release.slug, send_data[0].get('cover_id'))
        for chapter in release.chapters[::-1]:
            sleep(1)
            for count, data in enumerate(send_data, start=1):
                if count % 30 == 0:
                    sleep(1)
                _send_release_in_tg(release.name, chapter.volume, chapter.number, chapter.url, cover,
                                    data.get('account_id'))


def _get_send_data(manga_slug: str) -> list[dict]:
    log.debug(f'Получение телеграмм аккаунтов и id обложки манги из ДБ | manga_slug={manga_slug}')
    with Session_db() as session:
        try:
            stmt = select(TelegramAccounts.account_id, TrackedManga.cover_id).join(
                MangaAccounts.readable_manga).join(MangaAccounts.telegram_accounts).where(
                TrackedManga.slug == manga_slug).where(TelegramAccounts.active.is_(True))
            log.debug(f'Запрос = {stmt}')
            result = session.execute(stmt).mappings().all()
        except (SQLAlchemyError, DBAPIError) as error:
            log.error('Ошибка при получении телеграмм аккаунтов и id обложки манги из ДБ (SQLAlchemy)', exc_info=error)
            raise
        except Exception as error:
            log.error('Ошибка при получении телеграмм аккаунтов и id обложки манги из ДБ', exc_info=error)
            raise

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
    placeholder_path = Path.joinpath(Path.cwd(), r'.\data\images\placeholder_cover.png')
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
