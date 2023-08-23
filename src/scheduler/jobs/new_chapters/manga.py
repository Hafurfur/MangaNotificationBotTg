from __future__ import annotations
from typing import TYPE_CHECKING
from src.scheduler.jobs.new_chapters.chapter import Chapter

if TYPE_CHECKING:
    from bs4 import Tag


class Manga:
    def __init__(self, manga_name: str, manga_slug: str, chapters: list[Chapter]):
        self.name = manga_name
        self.slug = manga_slug
        self.chapters = chapters

    @classmethod
    def maga_builder(cls, release_data: Tag, last_mg_chapter: dict):
        name: str = release_data.find(class_='link-default').text
        slug: str = release_data.find(class_='link-default').attrs.get('href').split('/')[-1]
        chapters: list[Chapter] = []

        soup_all_new_chapters = release_data.find_all(class_='updates__chapter')

        for chapter in soup_all_new_chapters:
            new_chapter = Chapter.chapter_builder(chapter)
            if new_chapter.volume >= last_mg_chapter.get('last_volume') and \
                    new_chapter.number > last_mg_chapter.get('last_chapter'):
                chapters.append(new_chapter)

        return cls(name, slug, chapters)

    def __repr__(self):
        return f'Release(manga_name={self.name}, manga_slug=({self.slug}, chapters={self.chapters})'
