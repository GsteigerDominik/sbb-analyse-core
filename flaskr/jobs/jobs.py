from apscheduler.schedulers.background import BackgroundScheduler

import atexit

from flaskr.poller import poller

scheduler = BackgroundScheduler(timezone="Europe/Zurich")
 #Config in Swiss local time
 #First Start the scheduler so no multithreading happends then add the job
 #TODO maybe make the job able to do multithreading
scheduler.start()
scheduler.add_job(func=poller.run_poll_job, trigger='cron', day='*', hour=4, minute=0)
# /!\ IMPORTANT /!\ : Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())
