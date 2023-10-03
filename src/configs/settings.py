from dotenv import load_dotenv, find_dotenv
from src.logger.base_logger import log

try:
    log.info('Загрузка переменных окружения')
    if find_dotenv():
        load_dotenv()
except Exception as error:
    log.error(f'Ошибка при загрузке переменных окружения {error}')
    raise

# Интервал времени (минуты) задания на отправку уведомлений о выходе новых глав
MAILING_JOB_INTERVAL = 5

# Интервал времени (часы) задания на обновление списка "Читаю"
UPD_READABLE_MB_JOB_INTERVAL = 1

# Ограничения по времени (секунды) сообщений от пользователя
MESSAGE_LIMIT = 2
CALLBACK_LIMIT = 0.5

DATA_DIR = './data'

# Настройки движка SQLAlchemy
ENGINE_SETTINGS = {
    'echo': False,
}