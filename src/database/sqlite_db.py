from typing import TYPE_CHECKING
from pathlib import Path
from src.logger.base_logger import log
from os import makedirs

from sqlalchemy import URL, create_engine, Engine
from sqlalchemy.exc import SQLAlchemyError, DBAPIError
from sqlalchemy.dialects.sqlite import DATETIME

if TYPE_CHECKING:
    from sqlalchemy import Engine


class SqliteDB:

    def __init__(self, db_name: str = None, db_dir: str = './data/db/', truncate_microseconds: bool = False):
        log.info(f'Создание экземпляра объекта {self.__class__.__name__}')
        log.debug(f'db_name={db_name}, db_dir={db_dir}')
        self.db_dir = db_dir
        self.db_name = 'bot_db.db' if db_name is None else db_name
        self.truncate_microseconds = truncate_microseconds
        self._make_db_dir()
        self._datetime_without_microsecond()

    def get_engine(self) -> Engine:
        try:
            db_url = URL.create(drivername='sqlite', database=f'{Path(self.db_dir, self.db_name)}')
            engine = create_engine(db_url, echo=False)
        except (SQLAlchemyError, DBAPIError) as error:
            log.error('Ошибка при создании движка SQLAlchemy', exc_info=error)
            raise
        except Exception as error:
            log.error('Ошибка при создании движка', exc_info=error)
            raise

        return engine

    def _make_db_dir(self) -> None:
        log.debug(f'Создание папки хранения БД')
        self.db_dir = Path(Path.cwd(), self.db_dir)

        try:
            makedirs(self.db_dir, exist_ok=True)
        except Exception as error:
            log.debug(f'Ошибка при создании папки хранения ДБ Sqlite', exc_info=error)

    def _datetime_without_microsecond(self) -> None:
        if self.truncate_microseconds:
            DATETIME._storage_format = '%(year)04d-%(month)02d-%(day)02d %(hour)02d:%(minute)02d:%(second)02d'
