from apscheduler.schedulers.background import BackgroundScheduler
from run_pipeline import run_pipeline

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(run_pipeline, "interval", minutes=5)
    scheduler.start()
