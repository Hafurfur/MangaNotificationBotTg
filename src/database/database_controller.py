from __future__ import annotations
from typing import TYPE_CHECKING, Any
from src.database.db_base import IndividualDBMethodsAbstr
from src.database.base_db_controller import BaseDBController
from src.logger.base_logger import log

if TYPE_CHECKING:
    from sqlalchemy import Engine, CursorResult, Table, Column, Insert, Select, Update, Delete


class DatabaseController(IndividualDBMethodsAbstr, BaseDBController):
    _instance: DatabaseController = None

    def __new__(cls, *args, **kwargs) -> DatabaseController:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, database: IndividualDBMethodsAbstr | BaseDBController) -> None:
        super().__init__()
        log.debug(f'Создание объекта контролера БД {self.__class__.__name__}')
        self._db = database

    def create_engine(self, **kwargs: Any) -> None:
        self._db.create_engine(**kwargs)

    def get_engine(self) -> Engine:
        return self._db.get_engine()

    def create_tables(self) -> None:
        self._db.create_tables()

    def insert(self, stmt: Insert, data: list[dict] | dict) -> None:
        return self._db.insert(stmt, data)

    def insert_on_conflict_do_update(self, table: Table,
                                     conflict_column: Column, data: dict) -> None:
        self._db.insert_on_conflict_do_update(table, conflict_column, data)

    def select(self, stmt: Select) -> CursorResult:
        return self._db.select(stmt)

    def update(self, stmt: Update, data: list[dict] | dict) -> None:
        return self._db.update(stmt, data)

    def delete(self, stmt: Delete) -> None:
        return self._db.delete(stmt)
