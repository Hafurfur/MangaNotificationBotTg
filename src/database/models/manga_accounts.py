from __future__ import annotations
from typing import TYPE_CHECKING
from .base import Base

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .tracked_manga import TrackedManga
    from .telegram_accounts import TelegramAccounts


class MangaAccounts(Base):
    __tablename__ = 'manga_accounts'

    account_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    create_date: Mapped[DateTime] = mapped_column(DateTime(timezone=False), nullable=False, server_default=func.now())
    update_date: Mapped[DateTime] = mapped_column(DateTime(timezone=False), nullable=False, server_default=func.now())
    username: Mapped[str] = mapped_column(nullable=False)
    active: Mapped[bool] = mapped_column(nullable=False)

    telegram_accounts: Mapped[list[TelegramAccounts]] = relationship(back_populates='manga_account')
    readable_manga: Mapped[list[TrackedManga]] = relationship(secondary='mg_acc_tr_mg_assoc',
                                                              back_populates='manga_accounts')

    def __str__(self):
        return f'MangaAccounts(account_id={self.account_id}, create_date={self.create_date}, ' \
               f'update_date={self.update_date}, username={self.username}, active={self.active})'
