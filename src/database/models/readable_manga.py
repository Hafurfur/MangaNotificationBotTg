from src.database.base_db_controller import BaseDBController

from sqlalchemy import ForeignKey, Table, Integer, Column


readable_manga = Table(
    'readable_manga',
    BaseDBController.metadata_obj,
    Column('mg_acc_id', Integer, ForeignKey('manga_accounts.id'), primary_key=True),
    Column('tracked_mg_id', Integer, ForeignKey('tracked_manga.id'), primary_key=True)
)
