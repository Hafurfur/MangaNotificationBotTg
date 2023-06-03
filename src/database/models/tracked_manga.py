from typing import TYPE_CHECKING
from datetime import datetime
from .base import Base

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .mg_trek_acc_association_table import MgAccountTrackedMgAssociationTable


class TrackedManga(Base):
    __tablename__ = 'tracked_manga'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    create_date: Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=False, server_default=func.now())
    update_date: Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=False, server_default=func.now())
    manga_id: Mapped[int] = mapped_column(nullable=False, unique=True)
    slug: Mapped[str] = mapped_column(nullable=False)
    name_rus: Mapped[str] = mapped_column(nullable=False)
    cover_url: Mapped[str] = mapped_column(nullable=False)

    manga_accounts: Mapped[list['MgAccountTrackedMgAssociationTable']] = relationship(back_populates='tracked_manga')

    def __repr__(self):
        return self

    def __str__(self):
        return f'TrackedManga(id={self.id}, manga_id={self.manga_id}, create_date={self.create_date}, ' \
               f'update_date={self.update_date}, slug={self.slug}, name_rus={self.name_rus}, cover_url={self.cover_url})'
