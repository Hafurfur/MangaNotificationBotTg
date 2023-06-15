from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()


def start_jobs():
    from src.scheduler.jobs import send_release_job
    scheduler.start()
