from __future__ import annotations
from typing import TYPE_CHECKING, Any
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from sqlalchemy import Engine, Table, Column, Insert, Select, Update, Delete
    from sqlalchemy.engine.cursor import CursorResult


class IndividualDBMethodsAbstr(ABC):

    @abstractmethod
    def create_engine(self, **kwargs: Any):
        pass

    @abstractmethod
    def insert_on_conflict_do_update(self, table: Table,
                                     conflict_column: Column, data: dict) -> None:
        pass


class GeneralDBMethodsAbstr(ABC):

    @abstractmethod
    def create_tables(self) -> None:
        pass

    @abstractmethod
    def get_engine(self) -> Engine:
        pass

    @abstractmethod
    def insert(self, stmt: Insert, data: list[dict] | dict) -> None:
        pass

    @abstractmethod
    def select(self, stmt: Select) -> CursorResult:
        pass

    @abstractmethod
    def update(self, stmt: Update, data: list[dict] | dict) -> None:
        pass

    @abstractmethod
    def delete(self, stmt: Delete) -> None:
        pass
