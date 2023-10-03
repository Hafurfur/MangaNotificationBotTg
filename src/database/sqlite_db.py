from __future__ import annotations
from typing import TYPE_CHECKING, Any
from pathlib import Path
from os import makedirs
from src.logger.base_logger import log
from src.database.db_base import IndividualDBMethodsAbstr
from src.database.base_db_controller import BaseDBController

from sqlalchemy import URL, create_engine
from sqlalchemy.exc import SQLAlchemyError, DBAPIError
from sqlalchemy.dialects.sqlite import DATETIME, insert

if TYPE_CHECKING:
    from sqlalchemy import Engine, Table, Column


class SqliteDB(BaseDBController, IndividualDBMethodsAbstr):

    def __init__(self, data_dir: str, truncate_microseconds: bool = False) -> None:
        super().__init__()
        log.debug(f'Создание объекта БД SQLite {self.__class__.__name__} | '
                  f'db_dir = {data_dir}, truncate_microseconds = {truncate_microseconds}')
        self.db_dir = f'{data_dir}/db/'
        self.db_name = 'manga_notif_bot.db'
        self.truncate_microseconds = truncate_microseconds

        self._make_db_dir()
        self._datetime_without_microsecond()

    def create_engine(self, **kwargs: Any) -> Engine:
        log.info('Создание движка БД для диалекта SQLite')
        try:
            db_url = URL.create(drivername='sqlite', database=f'{Path(self.db_dir, self.db_name)}')
            self.engine = create_engine(url=db_url, **kwargs)
        except (SQLAlchemyError, DBAPIError) as error:
            log.error('Ошибка при создании движка (SQLAlchemy)', exc_info=error)
            raise
        except Exception as error:
            log.error('Ошибка при создании движка', exc_info=error)
            raise

        return self.engine

    def _make_db_dir(self) -> None:
        log.debug(f'Создание папки хранения БД')

        try:
            makedirs(self.db_dir, exist_ok=True)
        except Exception as error:
            log.error(f'Ошибка при создании папки хранения ДБ Sqlite', exc_info=error)
            raise

    def _datetime_without_microsecond(self) -> None:
        log.debug(f'Изменение формата даты и времени в БД. Флаг = {self.truncate_microseconds}')
        if self.truncate_microseconds:
            DATETIME._storage_format = '%(year)04d-%(month)02d-%(day)02d %(hour)02d:%(minute)02d:%(second)02d'

    def insert_on_conflict_do_update(self, table: Table, conflict_column: Column, data: dict) -> None:
        log.debug('Вставка с обновлением при конфликте данных в БД')
        with self.engine.connect() as conn:
            try:
                stmt = insert(table).values(data.get('insert_data'))
                stmt = stmt.on_conflict_do_update(index_elements=[conflict_column],
                                                  set_=dict(data.get('update_data')))
                log.debug(f'Запрос = {stmt}')
                conn.execute(stmt)
                conn.commit()
            except (SQLAlchemyError, DBAPIError) as error:
                log.error('Ошибка при вставке с обновлением при конфликте данных в БД (SQLAlchemy)', exc_info=error)
                raise
            except Exception as error:
                log.error('Ошибка при вставке с обновлением при конфликте данных в БД', exc_info=error)
                raise
