from multiprocessing import Process
from zdiscord.util.general.Job import Job
from zdiscord.util.logging.LogFactory import LogFactory

class LogClearJob(Job):

    def __init__(self, name: str, interval: str, length: int, conf: {}, enabled: bool):
        Job.__init__(self, name, interval, length, conf, enabled)

    def execute_job(self,conf):
        LogFactory.log_dir = conf['log_dir'] if 'log_dir' in conf.keys() else LogFactory.log_dir
        LogFactory.log_level = conf['log_level'] if 'log_level' in conf.keys() else LogFactory.log_level
        LogFactory.log_stdout = conf['log_stdout'] if 'log_stdout' in conf.keys() else LogFactory.log_stdout

        # Sets up static class properties
        LogClear.init()

        LogClear.Logger.info("Running log clean up job!")

        LogClear.clean_up_logs()

    def job_is_alive(self) -> bool:
        return self.job_reference.is_alive()

    def kill_job(self) -> None:
        if self.job_reference.is_alive():
            self.job_reference.kill()


