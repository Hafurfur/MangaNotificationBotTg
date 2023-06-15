from __future__ import annotations
from typing import TYPE_CHECKING
from settings import DB_TYPE, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME
from src.database.models import Base

from sqlalchemy import URL, create_engine, text

if TYPE_CHECKING:
    from sqlalchemy import Engine


class DatabaseController:
    _instance: DatabaseController = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self._engine = None
        self._create_engine()

    def _create_engine(self):
        db_url = URL.create(DB_TYPE, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)
        self._engine = create_engine(db_url)

    def get_engine(self) -> Engine:
        return self._engine

    @staticmethod
    def _create_db():
        db_url = URL.create(DB_TYPE, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT)
        engine = create_engine(db_url, echo=True)

        with engine.connect() as conn:
            conn.execute(text('COMMIT'))
            conn.execute(text(f'CREATE DATABASE {DB_NAME}'))

        engine.dispose()

    @staticmethod
    def _create_table():
        db_url = URL.create(DB_TYPE, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)
        engine = create_engine(db_url, echo=True)
        Base.metadata.create_all(engine)
        engine.dispose()
