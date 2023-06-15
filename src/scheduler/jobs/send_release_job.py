from typing import Sequence
from time import sleep
from src.releases import get_releases
from src.scheduler.cheduler_controller import scheduler
from src.database import TrackedManga, MangaAccounts, TelegramAccounts, DatabaseController
from src.tele_bot.bot_controller import bot

from requests import get
from sqlalchemy.orm import Session
from sqlalchemy import select, Row


@scheduler.scheduled_job('interval', minutes=1)
def job_check_new_release():
    releases = get_releases()

    for release in releases:
        send_data = _get_send_data(release.manga_slug)
        cover = _get_cover_data(release.manga_slug, send_data)
        for data in send_data:
            for chap in release.chapters:
                sleep(1)
                _send_release_in_tg(release.manga_name, chap.chapter_number, chap.chapter_url, cover, data[0])


def _get_send_data(manga_slug: str) -> Sequence[Row[tuple]]:
    engine = DatabaseController().get_engine()

    with Session(engine) as session:
        query = select(TelegramAccounts.account_id, TrackedManga.cover_id).join(
            MangaAccounts.readable_manga).join(MangaAccounts.telegram_accounts).where(
            TrackedManga.slug == manga_slug)
        result_sql = session.execute(query).all()

    return result_sql


def _get_cover_data(manga_slug: str, send_data: Sequence[Row[tuple]]) -> bytes:
    response = get(f'https://cover.imglib.info/uploads/cover/{manga_slug}/cover/{send_data[0][1]}_250x350.jpg')
    return response.content


def _send_release_in_tg(manga_name: str, chap_num: str, chap_url: str, cover: bytes, tg_id: int):
    bot.send_photo(tg_id, photo=cover, caption=f'{manga_name}\n{chap_num}\n\n{chap_url}')
