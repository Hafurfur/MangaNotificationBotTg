import os
from os.path import join, dirname

from dotenv import load_dotenv

_dotenv_path = join(dirname(__file__), '.env')
load_dotenv(_dotenv_path)

# Database
DB_TYPE = os.environ.get('DB_TYPE')
DB_NAME = os.environ.get('DB_NAME')
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')

# Telegram bot
TOKEN = os.environ.get('TOKEN')
