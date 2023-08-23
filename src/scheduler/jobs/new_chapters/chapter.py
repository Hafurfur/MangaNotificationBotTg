from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bs4 import Tag


class Chapter:
    def __init__(self, chapter_url: str, chapter_volume: int, chapter_number: float):
        self.url = chapter_url
        self.volume = chapter_volume
        self.number = chapter_number

    @classmethod
    def chapter_builder(cls, chapter_data: Tag):
        url: str = chapter_data.attrs.get('href')
        chapter_number = chapter_data.find(class_='updates__chapter-vol').text.split(' ')
        volume: int = int(chapter_number[1])
        number: float = float(chapter_number[3])

        return cls(url, volume, number)

    def __repr__(self):
        return f'Chapter(chapter_url={self.url}, chapter_volume={self.volume}, ' \
               f'chapter_number{self.number})'
