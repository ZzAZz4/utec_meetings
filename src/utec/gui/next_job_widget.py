import pytermgui as ptg
from apscheduler.schedulers.background import BaseScheduler

class NextClassWidget(ptg.Container):
    def __init__(self, sched: BaseScheduler, every_seconds=1, **attrs) -> None:
        super().__init__(**attrs)
        self.sched = sched
        self.sched.add_job(self.update_content, 'interval', seconds=every_seconds)
        self.past = []

    def update_content(self) -> None:
        jobs = self.sched.get_jobs('classes')
        if len(jobs) == 0:
            self.set_widgets(["No jobs scheduled"]) # type: ignore
            return

        next_job = jobs[0]

        if self.past and next_job != self.past[-1]:
            self.past.append(next_job)
            self.past = self.past[-5:]

        self.set_widgets([f"{next_job.id}"]) # type: ignore
        
        
