from dotenv import load_dotenv, find_dotenv
from pathlib import Path
from src.logger.base_logger import log


if Path(Path.cwd(), '.env').exists():
    if not find_dotenv():
        log.debug('Не удалось загрузить .env')
    else:
        load_dotenv()
