from src.logger.base_logger import log
from src.configs.settings import MESSAGE_LIMIT, CALLBACK_LIMIT
from loader import bot, scheduler
import src.tele_bot.handlers
import src.scheduler.jobs
from src.tele_bot.middlewares.anti_spam import AntiSpam


def run():
    scheduler.start()
    bot.setup_middleware(AntiSpam(MESSAGE_LIMIT, CALLBACK_LIMIT))

    log.info('Старт бота')
    print('Старт бота')
    bot.infinity_polling()


if __name__ == '__main__':
    run()
