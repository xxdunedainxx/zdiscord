from zdiscord.service.Service import Service
from apscheduler.job import Job as AppSchedulerJob

class Job(Service):

    def __init__(self, name: str, interval: str, length: int):
        Service.__init__(self, name=self.__class__.__name__)
        self.name: str = name
        self.interval: str = interval
        self.length: int = length
        self.job_reference: AppSchedulerJob = None
        self.context:{} = None

    def execute_job(self, *args, **kwargs):
        pass