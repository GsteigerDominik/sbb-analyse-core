from apscheduler.schedulers.background import BackgroundScheduler

import atexit
import poller.poller
from flaskr import app

scheduler = BackgroundScheduler()
scheduler.add_job(func=poller.poller.runPollJob, trigger='cron', day='*', hour=17, minute=35)
scheduler.start()
# /!\ IMPORTANT /!\ : Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

@app.cli.command()
def runPollJob():
    """Run poll job."""
    poller.poller.runPollJob()
