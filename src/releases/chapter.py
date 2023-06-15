from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bs4 import Tag


class Chapter:
    def __init__(self, chapter_url: str, chapter_number: str):
        self.chapter_url = chapter_url
        self.chapter_number = chapter_number

    @classmethod
    def soup_builder(cls, chapter_data: Tag):
        chapter_url: str = chapter_data.attrs.get('href')
        chapter_number: str = chapter_data.find(class_='updates__chapter-vol').text

        return cls(chapter_url, chapter_number)

    def __ne__(self, other):
        if other is None:
            return False

        if (self.chapter_url, self.chapter_number) == (other.chapter_url, other.chapter_number):
            return False

        return True

    def __str__(self):
        return f'Chapter(chapter_url={self.chapter_url}, chapter_number{self.chapter_number})'
