from src.tele_bot.bot_controller import star_bot
from src.scheduler.cheduler_controller import start_jobs


def run():
    start_jobs()
    star_bot()


if __name__ == '__main__':
    run()
