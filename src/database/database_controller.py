from settings import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME
from src.database.model_db import Base

from sqlalchemy import URL, create_engine, text


class DatabaseController:
    @staticmethod
    def create_db():
        db_url = URL.create('postgresql', DB_USER, DB_PASSWORD, DB_HOST, DB_PORT)
        engine = create_engine(db_url, echo=True)

        with engine.connect() as conn:
            conn.execute(text('COMMIT'))
            conn.execute(text(f'CREATE DATABASE {DB_NAME}'))

        engine.dispose()

    @staticmethod
    def create_table():
        db_url = URL.create('postgresql', DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)
        engine = create_engine(db_url, echo=True)
        Base.metadata.create_all(engine)
        engine.dispose()


if __name__ == '__main__':
    # DatabaseController.create_table()
    pass
