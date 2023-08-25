from os import getenv
from src.database import DatabaseController, SqliteDB

from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import sessionmaker
from telebot import TeleBot, StatePickleStorage

db = DatabaseController(SqliteDB(getenv('SQLITE_DB_NAME')))
db.create_table()
Session_db = sessionmaker(bind=db.get_engine())
bot = TeleBot(token=getenv('TOKEN'), skip_pending=True,
              state_storage=StatePickleStorage(file_path='data/state-save/states.pkl'))
scheduler = BackgroundScheduler()
