import src.configs.settings
from loader import scheduler, bot
import src.tele_bot.handlers
import src.scheduler
from src.logger.base_logger import log


def run():
    scheduler.start()

    log.info('Старт бота')
    bot.infinity_polling()


if __name__ == '__main__':
    run()
