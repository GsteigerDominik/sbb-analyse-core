from apscheduler.schedulers.background import BackgroundScheduler

import atexit
import poller.poller
from flaskr import app

scheduler = BackgroundScheduler()
 #Config in Swiss local time
scheduler.add_job(func=poller.poller.runPollJob, trigger='cron', day='*', hour=8, minute=38)
scheduler.start()
# /!\ IMPORTANT /!\ : Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

@app.cli.command()
def runPollJob():
    """Run poll job."""
    poller.poller.runPollJob()
