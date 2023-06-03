from typing import TYPE_CHECKING
from datetime import datetime
from .base import Base

from sqlalchemy import ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .manga_accounts import MangaAccounts
    from .tracked_manga import TrackedManga


class MgAccountTrackedMgAssociationTable(Base):
    __tablename__ = 'mg_acc_tr_mg_assoc'
    mg_acc_id: Mapped[int] = mapped_column(ForeignKey('manga_accounts.id'), primary_key=True)
    tracked_mg_id: Mapped[int] = mapped_column(ForeignKey('tracked_manga.id'), primary_key=True)
    create_date: Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=False, server_default=func.now())
    update_date: Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=False, server_default=func.now())

    tracked_manga: Mapped['TrackedManga'] = relationship(back_populates='manga_accounts')
    manga_account: Mapped['MangaAccounts'] = relationship(back_populates='readable_manga')

    def __repr__(self):
        return self

    def __str__(self):
        return f'MgAccountTrackedMgAssociationTable(mg_acc_id={self.mg_acc_id}, tracked_mg_id={self.tracked_mg_id}), ' \
               f'create_date={self.create_date}, update_date={self.update_date}'
