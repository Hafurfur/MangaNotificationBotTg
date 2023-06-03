from typing import TYPE_CHECKING
from datetime import datetime
from .base import Base

from sqlalchemy import ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .manga_accounts import MangaAccounts


class TelegramAccounts(Base):
    __tablename__ = 'telegram_accounts'

    id: Mapped[int] = mapped_column(primary_key=True)
    create_date: Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=False, server_default=func.now())
    update_date: Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=False, server_default=func.now())
    account_id: Mapped[int] = mapped_column(unique=True, nullable=False)
    manga_account_id: Mapped[int] = mapped_column(ForeignKey('manga_accounts.id'), nullable=True, server_default=None)
    username: Mapped[str] = mapped_column(nullable=False)
    first_name: Mapped[str] = mapped_column(nullable=False)
    second_name: Mapped[str] = mapped_column(nullable=True, server_default=None)
    active: Mapped[bool] = mapped_column(nullable=False)

    manga_account: Mapped['MangaAccounts'] = relationship(back_populates='telegram_accounts')

    def __repr__(self):
        return self

    def __str__(self):
        return f'TelegramAccounts(id={self.id}, account_id={self.account_id}, create_date={self.create_date}, ' \
               f'update_date={self.update_date}, username={self.username}, first_name={self.first_name}, ' \
               f'second_name={self.second_name}, active={self.active})'
