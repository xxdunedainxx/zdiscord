from zdiscord.service.Service import Service
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from zdiscord.util.error.ErrorFactory import errorStackTrace
from zdiscord.util.general.JobFactory import *
from zdiscord.util.general.Job import Job
import random
import string

class JobManager(Service):

    def __init__(self, jobConfigs: []):
        Service.__init__(self,name=self.__class__.__name__)

        # Map for our reference to jobs
        self.__JOBS: [Job] = []

        # Master job schedule
        self.__JOB_SCHEDULER: AsyncIOScheduler = AsyncIOScheduler()

        self.__init_jobs(jobs=jobConfigs)

        self.__JOB_SCHEDULER.start()

    def __init_jobs(self, jobs: []):
        for job_config in jobs:
            try:
                job_to_add: Job = eval(job_config['JobType'])(name=job_config['name'],interval=job_config['interval'],length=job_config['length'])

                if 'context' in job_config.keys():
                    job_to_add.context = job_config['context']

                self.__JOBS.append(job_to_add)
                self.schedule(job=job_to_add)

            except Exception as e:
                self._logger.warning(f"Failed to configure job, \'{job_config}\', with error {errorStackTrace(e)}")

    def __job_id(self) -> str:
        return ''.join(random.choice(string.ascii_lowercase) for i in range(10))

    def schedule(self, job: Job):
        jid=f"{job.name}-{self.__job_id()}"
        if job.interval == 'seconds':
            self.__JOB_SCHEDULER.add_job(job.execute_job, 'interval', seconds=job.length, id=jid)
        elif job.interval == 'hours':
            self.__JOB_SCHEDULER.add_job(job.execute_job, 'interval', hours=job.length, id=jid)
        elif job.interval == 'days':
            self.__JOB_SCHEDULER.add_job(job.execute_job, 'interval', days=job.length, id=jid)
        else:
            self._logger.warning(f"Interval \'{job.interval}\' for job {job.name}, is not valid.")
            return
        # Grab for reference to its app schedule relative
        job.job_reference = self.__JOB_SCHEDULER.get_job(job_id=jid)