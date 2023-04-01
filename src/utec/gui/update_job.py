from apscheduler.schedulers.background import BaseScheduler
from loguru import logger
from utec.core.get import get_conferences
from utec.core.open import open_conference

class UpdateJob:
    def __init__(self, sched: BaseScheduler, uname: str, password: str, **attrs) -> None:
        self.sched = sched
        self.uname = uname
        self.password = password

    def reset_job_list(self):
        logger.info("Fetching conferences...")
        conferences = get_conferences(self.uname, self.password)

        logger.info("Removing old jobs...")
        for job in self.sched.get_jobs('classes'):
            logger.info(f"Removing job {job.id}")
            self.sched.remove_job(job.id)

        logger.info("Adding new jobs...")
        for conference in conferences:
            id = conference.course + ' | ' + conference.start.strftime("%Y-%m-%d %H:%M")
            id += '\n' + f"[skyblue underline ~{conference.url}] {conference.url}" if conference.url else 'No URL'
            self.sched.add_job(open_conference, trigger='date', run_date=conference.start, args=[conference.url], id=id, jobstore='classes')

