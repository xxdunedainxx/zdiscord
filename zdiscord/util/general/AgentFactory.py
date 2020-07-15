from zdiscord.service.Service import Service
from zdiscord.util.general.Agent import Agent
from zdiscord.util.general.AgentProcess import AgentProcess
from zdiscord.service.integration.chat.discord.agents.DiscordAgent import DiscordAgent
from zdiscord.service.integration.chat.discord.agents.games.tictactoe.TicTacToe import DiscordTicTacToe
from zdiscord.service.integration.chat.discord.agents.pollbot.PollAgent import PollAgent
from multiprocessing import Process
from zdiscord.util.error.ErrorFactory import errorStackTrace
from zdiscord.service.ThreadQ import ThreadQueue, ThreadQueueObject
from zdiscord.util.logging.LogFactory import LogFactory
from zdiscord.App import App
from zdiscord.util.general.Main import MainUtil
from zdiscord.util.general.JobManager import JobManager
from zdiscord.util.general.Job import Job
from zdiscord.util.general.JobQ import RUNNING_JOBS
from zdiscord.util.general.JobProcess import JobProcess
import random
import time
import json
import string

class AgentFactory(Service):
    def __init__(self, conf: {}):
        self.conf = json.load(open(conf, encoding='utf-8'))
        self.__init_logger()

        super().__init__(name=self.__class__.__name__)

        self.AGENT_CONFIGS: {} = {}

        self.PROC_MAP : {} = {}
        self.JOB_MAP : {} = {}

        self.setup_agent_configs(self.conf)

        self._logger.info("Init Agent Factory..")

        self.JOBS: JobManager = None
        self.__init_job_factory()

    def main(self):
        self._logger.info("Running app MAIN")
        # Initialize redis q for other procs
        MainUtil.init_threadq()

        self.PROC_MAP['main'] = Process(target=App.appMain, args=('./zdiscord/app.json',))

        # Start main worker
        self.PROC_MAP['main'].start()

        self.__run_main_process()

    def __init_logger(self):
      if 'log' in self.conf.keys():
        LogFactory.log_dir = self.conf['log']['log_dir'] if 'log_dir' in self.conf['log'].keys() else LogFactory.log_dir
        LogFactory.log_level = self.conf['log']['log_level'] if 'log_level' in self.conf[
          'log'].keys() else LogFactory.log_level
        LogFactory.log_stdout = self.conf['log']['log_stdout'] if 'log_stdout' in self.conf[
          'log'].keys() else LogFactory.log_stdout

    def __eval_current_jobs(self):
      self._logger.info(f"Checkin current jobs, {self.JOB_MAP}")
      keys_to_kill: [str] = []

      for job in self.JOB_MAP.keys():
        if job == 'main':
          continue
        elif self.JOB_MAP[job].timed_out():
          self._logger.info(f"Killing process {job}")
          self.JOB_MAP[job].expire()
          keys_to_kill.append(job)
        else:
          continue

      for key_to_kill in keys_to_kill:
        self.PROC_MAP.pop(key_to_kill)

    def __eval_current_threads(self):
      self._logger.info(f"Checkin current processes, {self.PROC_MAP}")
      keys_to_kill: [str] = []

      for process in self.PROC_MAP.keys():
        if process == 'main':
          continue
        elif self.PROC_MAP[process].timed_out():
          self._logger.info(f"Killing process {process}")
          self.PROC_MAP[process].expire()
          keys_to_kill.append(process)
        else:
          continue

      for key_to_kill in keys_to_kill:
        self.PROC_MAP.pop(key_to_kill)

    def __init_job_factory(self):
        if 'jobs' in self.conf.keys():
            self.JOBS: JobManager = JobManager(jobConfigs=self.conf['jobs'], logConfig=self.conf['log'])
        else:
            self._logger.warning("\'jobs\' config not present, no jobs set up for this app!")

    def __run_main_process(self):
      try:
        while self.PROC_MAP['main'].is_alive():
          self._logger.info("Still up....")
          if (ThreadQueue.has_thread()):
            agent_config: ThreadQueueObject = ThreadQueue.get_thread_off_queue()
            if agent_config is not None:
              self.run(agent_config)
          print(RUNNING_JOBS)
          if len(RUNNING_JOBS) > 0:
            job=RUNNING_JOBS.pop(0)
            self.run_job(job=job)

          self.__eval_current_threads()
          self.__eval_current_jobs()
          self.JOBS.run_jobs()
          time.sleep(5)
        print("main process died???")
      except Exception as e:
        self._logger.error(f"CRITICAL ERROR, MAIN PROCESS SHIT ITSELF. DYING {errorStackTrace(e)}")
        exit(-1)

    def setup_agent_configs(self, conf:{}):
        for agent in conf['chat']['agents'].keys():
            agent_conf=conf['chat']['agents'][agent]['conf'].copy()

            agent_conf['chat'] = {}
            agent_conf['chat']['token'] = conf['chat']['token']
            agent_conf['chat']['platform'] = agent_conf['platform'] if 'platform' in agent_conf.keys() else conf['chat']['platform']
            agent_conf['chat']['agent_stamp'] = True

            self.AGENT_CONFIGS[agent] = agent_conf

        self._logger.info(f"Configured agents: {str(agent_conf)}")

    def __agent_id(self) -> str:
      return ''.join(random.choice(string.ascii_lowercase) for i in range(10))


    def run_job(self, job: Job):
      try:
        job_id = f"{job.name}-{job.job_id()}"
        self._logger.info(f"Starting up job {job_id}")
        self.JOB_MAP[job_id] = JobProcess(job)
        self.JOB_MAP[job_id].process = Process(target=job.execute_job, args=(job.conf,))

        # Start child worker
        self.JOB_MAP[job_id].run()

        self._logger.info(f"{job_id} started!")
        return
      except Exception as e:
        self._logger.error(f"Failed to spin up process {errorStackTrace(e)}")
    def run(self, agent: ThreadQueueObject):
      try:
        agent_id = f"{agent.name}-{self.__agent_id()}"
        self._logger.info(f"Starting up agent {agent_id}")

        # construct child thread args
        completeArgs:{} = {}
        completeArgs.update(self.AGENT_CONFIGS[agent.name])
        completeArgs.update(agent.serialize())

        self.PROC_MAP[agent_id] = AgentProcess()
        self.PROC_MAP[agent_id].process = Process(target=App.appMain, args=(completeArgs,))

        # Start child worker
        self.PROC_MAP[agent_id].run()

        self._logger.info(f"{agent_id} started!")
        return
      except Exception as e:
        self._logger.error(f"Failed to spin up process {errorStackTrace(e)}")