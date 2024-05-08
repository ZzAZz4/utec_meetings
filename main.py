import dotenv
import os
from apscheduler.schedulers.background import BackgroundScheduler
import tzlocal

from utec.gui.update_job import ScheduleUpdater
from utec.gui.window_display import start_program


def main():
    dotenv.load_dotenv()
    executors = {'default': {'type': 'threadpool', 'max_workers': 20}}
    jobstores = {'default': {'type': 'memory'},
                 'classes': {'type': 'sqlalchemy', 'url': os.environ['DBURI']}}

    sched = BackgroundScheduler(
        executors=executors,
        jobstores=jobstores,
        timezone=str(tzlocal.get_localzone())
    )
    updater = ScheduleUpdater(sched)

    start_program(sched, updater)


if __name__ == '__main__':
    main()
