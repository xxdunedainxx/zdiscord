from zdiscord.service.Service import Service
from zdiscord.util.general.Agent import Agent
from zdiscord.util.general.AgentProcess import AgentProcess
from zdiscord.service.integration.chat.discord.agents.DiscordAgent import DiscordAgent
from zdiscord.service.integration.chat.discord.agents.games.tictactoe.TicTacToe import DiscordTicTacToe
from multiprocessing import Process
from zdiscord.util.error.ErrorFactory import errorStackTrace
from zdiscord.service.ThreadQ import ThreadQueue, ThreadQueueObject
from zdiscord.util.logging.LogFactory import LogFactory
from zdiscord.App import App
from zdiscord.util.general.Main import MainUtil
import random
import time
import json
import string

class AgentFactory(Service):
    def __init__(self, conf: {}):
        self.conf = json.load(open(conf))
        self.__init_logger()

        super().__init__(name=self.__class__.__name__)

        self.AGENT_CONFIGS: {} = {}

        self.PROC_MAP : {} = {}

        self.setup_agent_configs(self.conf)

        self._logger.info("Init Agent Factory..")

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

    def __eval_current_threads(self):
      self._logger.info(f"Checkin current processes, {self.PROC_MAP}")
      for process in self.PROC_MAP.keys():
        if process == 'main':
          continue
        elif self.PROC_MAP[process].timed_out():
          self._logger.info(f"Killing process {process}")
          self.PROC_MAP[process].expire()
        else:
          continue

    def __run_main_process(self):
      try:
        while self.PROC_MAP['main'].is_alive():
          self._logger.info("Still up....")
          if (ThreadQueue.has_thread()):
            agent_config: ThreadQueueObject = ThreadQueue.get_thread_off_queue()
            if agent_config is not None:
              self.run(agent_config)
          self.__eval_current_threads()
          time.sleep(5)
        print("main process died???")
      except Exception as e:
        self._logger.error("CRITICAL ERROR, MAIN PROCESS SHIT ITSELF. DYING")
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