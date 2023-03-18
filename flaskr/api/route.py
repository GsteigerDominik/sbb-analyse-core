from flaskr import app
from flaskr.jobs.jobs import scheduler

@app.route('/')
def index():
    return 'Hello World!'

@app.route("/jobs")
def jobs():
    html = "<p>Use LocalTime in DevEnvironment</p> <br><table><tr><th>Name</th><th>Function</th><th>Next Execution</th></tr>"
    for job in scheduler.get_jobs():
        html += "<tr><td>"+job.name+"</td><td>"+job.func_ref+"</td><td>"+str(job.next_run_time)+"</td></tr>"
    return html+"</table>"
