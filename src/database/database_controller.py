from __future__ import annotations
from typing import TYPE_CHECKING
from src.database.models import Base
from src.logger.base_logger import log


if TYPE_CHECKING:
    from sqlalchemy import Engine


class DatabaseController:
    _instance: DatabaseController = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, database):
        log.debug(f'Создание экземпляра объекта {self.__class__.__name__}')
        self._db = database
        self._engine = None

    def get_engine(self) -> Engine:
        log.info('Получение движка SQLAlchemy')
        if self._engine is None:
            self._engine = self._db.get_engine()

        return self._engine

    def create_table(self):
        log.info('Создание таблиц БД из модели')
        if self._engine is None:
            self.get_engine()

        Base.metadata.create_all(self._engine)
