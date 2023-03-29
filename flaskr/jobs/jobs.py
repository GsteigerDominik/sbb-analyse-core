from apscheduler.schedulers.background import BackgroundScheduler

import atexit
import poller.poller
from flaskr import app

scheduler = BackgroundScheduler(timezone="Europe/Zurich")
 #Config in Swiss local time
 #First Start the scheduler so no multithreading happends then add the job
 #TODO maybe make the job able to do multithreading
scheduler.start()
scheduler.add_job(func=poller.poller.runPollJob, trigger='cron', day='*', hour=11, minute=31)
# /!\ IMPORTANT /!\ : Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())
