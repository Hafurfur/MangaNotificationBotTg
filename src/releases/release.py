from __future__ import annotations
from typing import TYPE_CHECKING
from .chapter import Chapter

if TYPE_CHECKING:
    from bs4 import Tag


class Release:
    def __init__(self, manga_name: str, manga_slug: str, chapters: list[Chapter]):
        self.manga_name = manga_name
        self.manga_slug = manga_slug
        self.chapters = chapters

    @classmethod
    def soup_builder(cls, release_data: Tag):
        manga_name: str = release_data.find(class_='link-default').text
        manga_slug: str = release_data.find(class_='link-default').attrs.get('href').split('/')[-1]
        chapters: list[Chapter] = [Chapter.soup_builder(chapter) for chapter in
                                   release_data.find_all(class_='updates__chapter')]
        chapters.reverse()

        return cls(manga_name, manga_slug, chapters)

    def __eq__(self, other: Release):
        if other is None:
            return False

        print(other)
        if (self.manga_name, self.manga_slug) == (other.manga_name, other.manga_slug) \
                and len(self.chapters) == len(other.chapters):
            for index, _ in enumerate(self.chapters):
                if self.chapters[index] != other.chapters[index]:
                    return False

        return True

    def __str__(self):
        return f'Release(manga_name={self.manga_name}, manga_slug=({self.manga_slug}, chapters={self.chapters})'
