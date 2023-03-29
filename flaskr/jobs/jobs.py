from apscheduler.schedulers.background import BackgroundScheduler

import atexit
import poller.poller
from flaskr import app

scheduler = BackgroundScheduler(max_instances=1)
 #Config in Swiss local time
scheduler.add_job(func=poller.poller.runPollJob, trigger='cron', day='*', hour=9, minute=20)
scheduler.start()
# /!\ IMPORTANT /!\ : Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())
