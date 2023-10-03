from src.database.base_db_controller import BaseDBController

from sqlalchemy import DateTime, func, Column, Table, Integer, String, Boolean, ForeignKey, BigInteger


telegram_accounts = Table(
    'telegram_accounts',
    BaseDBController.metadata_obj,
    Column('id', BigInteger, primary_key=True, autoincrement=False),
    Column('create_date', DateTime, nullable=False, server_default=func.now()),
    Column('update_date', DateTime, nullable=False, server_default=func.now()),
    Column('manga_account_id', Integer, ForeignKey('manga_accounts.id'), nullable=True),
    Column('username', String, nullable=True),
    Column('first_name', String, nullable=False),
    Column('second_name', String, nullable=True),
    Column('active', Boolean, nullable=False),
)
