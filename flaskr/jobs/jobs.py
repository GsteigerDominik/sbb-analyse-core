from apscheduler.schedulers.background import BackgroundScheduler

import atexit

from flaskr.poller import poller
from flaskr.processor import processor

scheduler = BackgroundScheduler(timezone="Europe/Zurich")
 #Config in Swiss local time
 #First Start the scheduler so no multithreading happends then add the job
 #TODO maybe make the job able to do multithreading
scheduler.start()
scheduler.add_job(func=poller.run_poll_job, trigger='cron', day='*', hour=4, minute=0)
scheduler.add_job(func=processor.run_process_job, trigger='cron', day='*', hour=22, minute=16)
# /!\ IMPORTANT /!\ : Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())
