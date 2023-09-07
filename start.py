from src.logger.base_logger import log
import src.configs.settings
from src.configs.settings import MESSAGE_LIMIT, CALLBACK_LIMIT
from loader import scheduler, bot
import src.tele_bot.handlers
from src.tele_bot.middlewares.anti_spam import AntiSpam
import src.scheduler


def run():
    scheduler.start()

    bot.setup_middleware(AntiSpam(MESSAGE_LIMIT, CALLBACK_LIMIT))

    log.info('Старт бота')
    print('Старт бота')
    bot.infinity_polling()


if __name__ == '__main__':
    run()
