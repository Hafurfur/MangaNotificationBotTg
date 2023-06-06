from typing import TYPE_CHECKING
from datetime import datetime
from .base import Base

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .mg_trek_acc_association_table import MgAccountTrackedMgAssociationTable
    from .telegram_accounts import TelegramAccounts


class MangaAccounts(Base):
    __tablename__ = 'manga_accounts'

    account_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    create_date: Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=False, server_default=func.now())
    update_date: Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=False, server_default=func.now())
    username: Mapped[str] = mapped_column(nullable=False)
    active: Mapped[bool] = mapped_column(nullable=False)

    telegram_accounts: Mapped[list['TelegramAccounts']] = relationship(back_populates='manga_account')
    readable_manga: Mapped[list['MgAccountTrackedMgAssociationTable']] = relationship(
        back_populates='manga_account')

    def __repr__(self):
        return self

    def __str__(self):
        return f'MangaAccounts(account_id={self.account_id}, create_date={self.create_date}, ' \
               f'update_date={self.update_date}, username={self.username}, active={self.active})'
