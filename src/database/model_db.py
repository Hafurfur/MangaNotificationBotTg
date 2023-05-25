from __future__ import annotations
from datetime import datetime

from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class TelegramAccounts(Base):
    __tablename__ = 'telegram_accounts'

    account_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    create_date: Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=False, server_default=func.now())
    update_date: Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=False, server_default=func.now())
    username: Mapped[str] = mapped_column(nullable=False)
    tg_first_name: Mapped[str] = mapped_column(nullable=False)
    tg_second_name: Mapped[str] = mapped_column(nullable=True)
    active: Mapped[bool] = mapped_column(nullable=False)

    manga_accounts: Mapped[list[MangaAccounts]] = relationship(secondary='tg_mg_accounts_assoc',
                                                               back_populates='telegram_accounts')


class TgMgAccountsAssociationTable(Base):
    __tablename__ = 'tg_mg_accounts_assoc'
    tg_acc_id: Mapped[int] = mapped_column(ForeignKey('telegram_accounts.account_id'), primary_key=True,
                                           autoincrement=False)
    mg_acc_id: Mapped[int] = mapped_column(ForeignKey('manga_accounts.account_id'), primary_key=True,
                                           autoincrement=False)
    create_date: Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=False, server_default=func.now())
    update_date: Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=False, server_default=func.now())


class MangaAccounts(Base):
    __tablename__ = 'manga_accounts'
    account_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    create_date: Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=False, server_default=func.now())
    update_date: Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=False, server_default=func.now())
    username: Mapped[str] = mapped_column(nullable=False)
    active: Mapped[bool] = mapped_column(nullable=False)

    telegram_accounts: Mapped[list[TelegramAccounts]] = relationship(secondary='tg_mg_accounts_assoc',
                                                                     back_populates='manga_accounts')
    tracked_manga: Mapped[list[TrackedManga]] = relationship(secondary='mg_acc_tr_mg_assoc',
                                                             back_populates='manga_accounts')


class MgAccountTrackedMgAssociationTable(Base):
    __tablename__ = 'mg_acc_tr_mg_assoc'
    mg_acc_id: Mapped[int] = mapped_column(ForeignKey('manga_accounts.account_id'), primary_key=True,
                                           autoincrement=False)
    tracked_mg_id: Mapped[int] = mapped_column(ForeignKey('tracked_manga.manga_id'), primary_key=True,
                                               autoincrement=False)
    create_date: Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=False, server_default=func.now())
    update_date: Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=False, server_default=func.now())


class TrackedManga(Base):
    __tablename__ = 'tracked_manga'
    manga_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    create_date: Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=False, server_default=func.now())
    update_date: Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=False, server_default=func.now())
    slug: Mapped[str] = mapped_column(unique=True)
    name_rus: Mapped[str] = mapped_column(nullable=False)
    cover_url: Mapped[str] = mapped_column(nullable=False)

    manga_accounts: Mapped[list[MangaAccounts]] = relationship(secondary='mg_acc_tr_mg_assoc',
                                                               back_populates='tracked_manga')


if __name__ == '__main__':
    pass
