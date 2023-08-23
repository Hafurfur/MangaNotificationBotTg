from .base import Base

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class MgAccountTrackedMgAssociationTable(Base):
    __tablename__ = 'mg_acc_tr_mg_assoc'

    mg_acc_id: Mapped[int] = mapped_column(ForeignKey('manga_accounts.account_id'), primary_key=True)
    tracked_mg_id: Mapped[int] = mapped_column(ForeignKey('tracked_manga.manga_id'), primary_key=True)

    def __str__(self):
        return f'MgAccountTrackedMgAssociationTable(mg_acc_id={self.mg_acc_id}, tracked_mg_id={self.tracked_mg_id})'
