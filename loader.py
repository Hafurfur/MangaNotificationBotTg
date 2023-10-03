from os import getenv
from src.database.database_controller import DatabaseController
from src.database.sqlite_db import SqliteDB
from src.configs.settings import DATA_DIR, ENGINE_SETTINGS

from apscheduler.schedulers.background import BackgroundScheduler
from telebot import TeleBot, StatePickleStorage

# проверка данных из .env

db = DatabaseController(SqliteDB(data_dir=DATA_DIR, truncate_microseconds=True))
db.create_engine(**ENGINE_SETTINGS)
db.create_tables()

bot = TeleBot(token=getenv('TOKEN'), skip_pending=True,
              state_storage=StatePickleStorage(file_path=f'{DATA_DIR}/state-save/states.pkl'),
              use_class_middlewares=True)
scheduler = BackgroundScheduler()

print()
