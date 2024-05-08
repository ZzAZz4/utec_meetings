from apscheduler.schedulers.background import BaseScheduler
from utec.core import get_conferences, open_conference


class ScheduleUpdater:
    def __init__(
        self,
        sched: BaseScheduler,
    ) -> None:
        self.sched = sched

    def refetch(self):
        conferences = get_conferences()

        for job in self.sched.get_jobs('classes'):
            self.sched.remove_job(job.id)

        for conference in conferences:
            id = conference.course + ' | ' + \
                conference.start.strftime("%Y-%m-%d %H:%M")

            if conference.url is not None:
                id += (
                    f"\n[skyblue underline ~{conference.url}]"
                    f"{conference.url}"
                )

            self.sched.add_job(
                open_conference,
                trigger='date',
                run_date=conference.start,
                args=[conference.url],
                id=id,
                jobstore='classes'
            )
