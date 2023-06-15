from __future__ import annotations
from typing import TYPE_CHECKING
from .base import Base

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .manga_accounts import MangaAccounts


class TrackedManga(Base):
    __tablename__ = 'tracked_manga'

    manga_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    create_date: Mapped[DateTime] = mapped_column(DateTime(timezone=False), nullable=False, server_default=func.now())
    update_date: Mapped[DateTime] = mapped_column(DateTime(timezone=False), nullable=False, server_default=func.now())
    slug: Mapped[str] = mapped_column(nullable=False, unique=True)
    name_rus: Mapped[str] = mapped_column(nullable=False)
    cover_id: Mapped[str] = mapped_column(nullable=False)

    manga_accounts: Mapped[list[MangaAccounts]] = relationship(secondary='mg_acc_tr_mg_assoc',
                                                               back_populates='readable_manga')

    def __repr__(self):
        return self

    def __str__(self):
        return f'TrackedManga(manga_id={self.manga_id}, create_date={self.create_date}, ' \
               f'update_date={self.update_date}, slug={self.slug}, name_rus={self.name_rus}, cover_id={self.cover_id})'
