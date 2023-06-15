from __future__ import annotations
from typing import TYPE_CHECKING
from .base import Base

from sqlalchemy import ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .manga_accounts import MangaAccounts


class TelegramAccounts(Base):
    __tablename__ = 'telegram_accounts'

    account_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    create_date: Mapped[DateTime] = mapped_column(DateTime(timezone=False), nullable=False, server_default=func.now())
    update_date: Mapped[DateTime] = mapped_column(DateTime(timezone=False), nullable=False, server_default=func.now())
    manga_account_id: Mapped[int] = mapped_column(ForeignKey('manga_accounts.account_id'), nullable=True)
    username: Mapped[str] = mapped_column(nullable=True)
    first_name: Mapped[str] = mapped_column(nullable=False)
    second_name: Mapped[str] = mapped_column(nullable=True)
    active: Mapped[bool] = mapped_column(nullable=False)

    manga_account: Mapped[MangaAccounts] = relationship(back_populates='telegram_accounts')

    def __repr__(self):
        return self

    def __str__(self):
        return f'TelegramAccounts(account_id={self.account_id}, create_date={self.create_date}, ' \
               f'update_date={self.update_date}, manga_account_id={self.manga_account_id}, username={self.username}, ' \
               f'first_name={self.first_name}, second_name={self.second_name}, active={self.active})'
