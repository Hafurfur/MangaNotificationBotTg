from __future__ import annotations
from src.database import DatabaseController
from src.database.models import TrackedManga
from src.releases import Release

import requests
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session
from sqlalchemy import select

_last_release: Release = None


def _get_soup_from_page() -> BeautifulSoup:
    try:
        response = requests.get('https://mangalib.me')
    except requests.exceptions as error:
        print(error)

    return BeautifulSoup(response.text, 'lxml')


def _get_all_manga_slug_db() -> set:
    db_engine = DatabaseController().get_engine()
    with Session(db_engine) as session:
        query = select(TrackedManga.slug)

    return set(session.scalars(query).all())


def get_releases() -> list[Release]:
    slugs_in_db = _get_all_manga_slug_db()
    releases = []
    global _last_release

    for release in _get_soup_from_page().find_all(class_='updates__item'):
        if release.find(class_='link-default').attrs.get('href').split('/')[-1] in slugs_in_db:
            new_release = Release.soup_builder(release)

            if new_release == _last_release:
                break

            releases.append(new_release)

    if releases:
        _last_release = releases[0]

    return releases
