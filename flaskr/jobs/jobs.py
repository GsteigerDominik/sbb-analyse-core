from apscheduler.schedulers.background import BackgroundScheduler

import atexit
import poller.poller
from flaskr import app

scheduler = BackgroundScheduler(timezone="Europe/Zurich")
 #Config in Swiss local time
scheduler.start()
scheduler.add_job(func=poller.poller.runPollJob, trigger='cron', day='*', hour=10, minute=45)
# /!\ IMPORTANT /!\ : Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())
