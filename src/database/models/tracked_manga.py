from src.database.base_db_controller import BaseDBController

from sqlalchemy import DateTime, func, Column, Table, Integer, String


tracked_manga = Table(
    'tracked_manga',
    BaseDBController.metadata_obj,
    Column('id', Integer, primary_key=True, autoincrement=False),
    Column('create_date', DateTime, nullable=False, server_default=func.now()),
    Column('update_date', DateTime, nullable=False, server_default=func.now()),
    Column('slug', String, nullable=False, unique=True),
    Column('name_rus', String, nullable=False),
    Column('cover_id', String, nullable=False),
    Column('last_volume', Integer, nullable=True),
    Column('last_chapter', Integer, nullable=True)

)
