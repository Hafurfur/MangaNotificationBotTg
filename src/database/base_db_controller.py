from __future__ import annotations
from typing import TYPE_CHECKING
from src.logger.base_logger import log
from src.database.db_base import GeneralDBMethodsAbstr

from sqlalchemy.exc import SQLAlchemyError, DBAPIError
from sqlalchemy import MetaData

if TYPE_CHECKING:
    from sqlalchemy import Engine, Insert, Select, Update, Delete
    from sqlalchemy.engine.cursor import CursorResult


class BaseDBController(GeneralDBMethodsAbstr):
    metadata_obj = MetaData()

    def __init__(self):
        self.engine: Engine = None

    def get_engine(self) -> Engine:
        log.info('Получение движка SQLAlchemy')
        return self.engine

    def create_tables(self) -> None:
        log.info('Создание таблиц БД из модели')
        if self.engine is None:
            log.error('Движок SQLAlchemy не был создан')
            raise ValueError('Движок SQLAlchemy не был создан')

        self.metadata_obj.create_all(self.engine)

    def insert(self, stmt: Insert, data: list[dict] | dict) -> None:
        log.info('Вставке данных в БД')
        with self.engine.connect() as conn:
            try:
                log.debug(f'Запрос = {stmt}')
                conn.execute(stmt, data)
                conn.commit()
            except (SQLAlchemyError, DBAPIError) as error:
                log.error('Ошибка при вставке в БД (SQLAlchemy)', exc_info=error)
                raise
            except Exception as error:
                log.error('Ошибка при вставке в БД', exc_info=error)
                raise

    def select(self, stmt: Select) -> CursorResult:
        log.info('Получение данных из БД')

        with self.engine.connect() as conn:
            try:
                log.debug(f'Запрос = {stmt}')
                result = conn.execute(stmt)
            except (SQLAlchemyError, DBAPIError) as error:
                log.error('Ошибка при получении из БД (SQLAlchemy)', exc_info=error)
                raise
            except Exception as error:
                log.error('Ошибка при получении из БД', exc_info=error)
                raise

        return result

    def update(self, stmt: Update, data: list[dict] | dict) -> None:
        log.info('Обновление данных в БД')
        with self.engine.connect() as conn:
            try:
                log.debug(f'Запрос = {stmt}')
                conn.execute(stmt, data)
                conn.commit()
            except (SQLAlchemyError, DBAPIError) as error:
                log.error('Ошибка при обновление данных в БД (SQLAlchemy)', exc_info=error)
                raise
            except Exception as error:
                log.error('Ошибка при обновление данных в БД', exc_info=error)
                raise

    def delete(self, stmt: Delete) -> None:
        log.info('Удаление данных из БД')
        with self.engine.connect() as conn:
            try:
                log.debug(f'Запрос = {stmt}')
                conn.execute(stmt)
                conn.commit()
            except (SQLAlchemyError, DBAPIError) as error:
                log.error('Ошибка при удалении данных из БД (SQLAlchemy)', exc_info=error)
                raise
            except Exception as error:
                log.error('Ошибка при удалении данных из БД', exc_info=error)
                raise
