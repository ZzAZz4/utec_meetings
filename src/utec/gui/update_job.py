from apscheduler.schedulers.background import BaseScheduler
from utec.core import get_conferences, open_conference
from utec.core.progress import ProgressIndicator, EmptyProgressIndicator        

class ScheduleUpdater:
    def __init__(self, sched: BaseScheduler, uname: str, password: str, **attrs) -> None:
        self.sched = sched
        self.uname = uname
        self.password = password

    def refetch(self, progress: ProgressIndicator = EmptyProgressIndicator()):
        conferences = get_conferences(self.uname, self.password, progress=progress)

        for job in self.sched.get_jobs('classes'):
            self.sched.remove_job(job.id)

        for conference in conferences:
            id = conference.course + ' | ' + conference.start.strftime("%Y-%m-%d %H:%M")
            id += '\n' + f"[skyblue underline ~{conference.url}] {conference.url}" if conference.url else 'No URL'
            self.sched.add_job(open_conference, trigger='date', run_date=conference.start, args=[conference.url], id=id, jobstore='classes')

