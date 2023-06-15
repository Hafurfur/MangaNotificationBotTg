from .database_controller import DatabaseController
from .models import TrackedManga
from .models import MangaAccounts
from .models import TelegramAccounts
from .bot_db import save_telegram_account
from .bot_db import add_account_tracking
from .bot_db import having_manga_account

DatabaseController()
