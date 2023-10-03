from src.database.base_db_controller import BaseDBController

from sqlalchemy import DateTime, func, Column, Table, Integer, String, Boolean


manga_accounts = Table(
    'manga_accounts',
    BaseDBController.metadata_obj,
    Column('id', Integer, primary_key=True, autoincrement=False),
    Column('create_date', DateTime, nullable=False, server_default=func.now()),
    Column('update_date', DateTime, nullable=False, server_default=func.now()),
    Column('username', String, nullable=False),
    Column('active', Boolean, nullable=False)
)
