import dotenv
import os
from apscheduler.schedulers.background import BackgroundScheduler

from utec.gui.update_job import UpdateJob
from utec.gui.display import start_display


def main():
    dotenv.load_dotenv()
    executors = {'default': {'type': 'threadpool', 'max_workers': 20}}
    jobstores = {'default': {'type': 'memory'},
                 'classes': {'type': 'sqlalchemy', 'url': os.environ['DBURI']}}

    sched = BackgroundScheduler(executors=executors, jobstores=jobstores)
    updater = UpdateJob(sched, os.environ['USERNAME'], os.environ['PASSWORD'])
    sched.add_job(updater.reset_job_list, 'cron', hour=2,
                  minute=0, id='main_job', replace_existing=True)
    sched.start()

    start_display(sched, updater)


if __name__ == '__main__':
    main()
