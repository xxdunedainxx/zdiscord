from zdiscord.service.Service import Service
import schedule
from zdiscord.util.error.ErrorFactory import errorStackTrace
from zdiscord.util.general.JobFactory import *
from zdiscord.util.general.Job import Job
from zdiscord.util.general.JobQ import RUNNING_JOBS
import random
import string
import datetime
from multiprocessing import Process

class JobScheduler:

    class ScheduledJob:

        def __init__(self, interval: str, length: int, method=print):
            self.last_run_time: datetime = datetime.datetime.now()
            self.interval = interval
            self.length = length

            self.logic = method

            # eval next run time
            self.set_next_run_time()

        #def run(self):
        #    if self.eval_next_run_time():


        def set_next_run_time(self) -> None:
            if self.interval == 'days':
                self.next_run_time: datetime = self.last_run_time + datetime.timedelta(days=self.length)
            elif self.interval == 'hours':
                self.next_run_time: datetime = self.last_run_time + datetime.timedelta(hours=self.length)
            elif self.interval == 'seconds':
                self.next_run_time: datetime = self.last_run_time + datetime.timedelta(seconds=self.length)
            else:
                self.next_run_time: datetime = self.last_run_time + datetime.timedelta(minutes=self.length)

        def eval_next_run_time(self) -> bool:
            return datetime.datetime.now() > self.next_run_time

    JOBS = []

    @staticmethod
    def add_job(interval: str, length: int, method=print):
        JobScheduler.JOBS.append(
            JobScheduler.ScheduledJob(interval, length, method)
        )


class JobManager(Service):

    def __init__(self, jobConfigs: [], logConfig: {}):
        Service.__init__(self,name=self.__class__.__name__)

        # Map for our reference to jobs
        self.__JOBS: [Job] = []
        self.logging_config: {} = logConfig
        self.__MANAGED_JOBS = []

        # Master job schedule
        self.__JOB_SCHEDULER: schedule = schedule

        self.__init_jobs(jobs=jobConfigs)


    def run_jobs(self) -> None:
        try:
            self.__JOB_SCHEDULER.run_pending()
        except Exception as e:
            self._logger.error(f"job failed to execute!! {errorStackTrace(e)}")

    def __init_jobs(self, jobs: []):
        for job_config in jobs:
            try:
                config_injection = job_config.copy()
                config_injection.update(self.logging_config)

                job_to_add: Job = eval(job_config['JobType'])(
                    name=job_config['name'],
                    interval=job_config['interval'],
                    length=job_config['length'],
                    conf=config_injection,
                    enabled=job_config['enabled'] if 'enabled' in job_config.keys() else True
                )
                if job_to_add.enabled:
                    self.__JOBS.append(job_to_add)
                else:
                    self._logger.warning(f"Job, {job_to_add}, is disabled!")
                self.schedule(job=job_to_add)
            except Exception as e:
                self._logger.warning(f"Failed to configure job, \'{job_config}\', with error {errorStackTrace(e)}")

    def schedule(self, job: Job):
        if job.interval == 'seconds':
            self._logger.info(f"{job.name} is scheduled to run every {job.length} seconds!")
            self.__JOB_SCHEDULER.every(job.length).seconds.do(RUNNING_JOBS.append,job)
        elif job.interval == 'minutes':
            self._logger.info(f"{job.name} is scheduled to run every {job.length} minutes!")
            self.__JOB_SCHEDULER.every(job.length).minutes.do(RUNNING_JOBS.append,job)
        elif job.interval == 'hours':
            self._logger.info(f"{job.name} is scheduled to run every {job.length} hours!")
            self.__JOB_SCHEDULER.every(job.length).hours.do(RUNNING_JOBS.append,job)
        elif job.interval == 'days':
            self._logger.info(f"{job.name} is scheduled to run every {job.length} days!")
            self.__JOB_SCHEDULER.every(job.length).days.do(RUNNING_JOBS.append,job)
        elif job.interval.lower() == 'monday':
            self._logger.info(f"{job.name} is scheduled to run every Monday!")
            self.__JOB_SCHEDULER.every().monday.do(RUNNING_JOBS.append, job)
        else:
            self._logger.warning(f"Interval \'{job.interval}\' for job {job.name}, is not valid.")
            return