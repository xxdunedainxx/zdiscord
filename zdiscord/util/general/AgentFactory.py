from zdiscord.service.Service import Service
from zdiscord.util.general.Agent import Agent
from zdiscord.service.integration.chat.discord.agents.DiscordAgent import DiscordAgent
from zdiscord.service.integration.chat.discord.agents.games.tictactoe.TicTacToe import DiscordTicTacToe
from multiprocessing import Process
from zdiscord.util.error.ErrorFactory import errorStackTrace
from zdiscord.service.ThreadQ import ThreadQueue, ThreadQueueObject
from zdiscord.util.logging.LogFactory import LogFactory
from zdiscord.App import App
from zdiscord.util.general.Main import MainUtil
import time
import json

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

    def __run_main_process(self):
      while self.PROC_MAP['main'].is_alive():
        self._logger.info("Still up....")
        if (ThreadQueue.has_thread()):
          agent_config: ThreadQueueObject = ThreadQueue.get_thread_off_queue()
          if agent_config is not None:
            self.run(agent_config)
        time.sleep(5)

    def setup_agent_configs(self, conf:{}):
        for agent in conf['chat']['agents'].keys():
            agent_conf=conf['chat']['agents'][agent]['conf'].copy()

            agent_conf['chat'] = {}
            agent_conf['chat']['token'] = conf['chat']['token']
            agent_conf['chat']['platform'] = agent_conf['platform'] if 'platform' in agent_conf.keys() else conf['chat']['platform']
            agent_conf['chat']['agent_stamp'] = True

            self.AGENT_CONFIGS[agent] = agent_conf

        self._logger.info(f"Configured agents: {str(agent_conf)}")

    def run(self, agent: ThreadQueueObject):
      try:
        if 'agent' not in self.PROC_MAP.keys():
          self._logger.info(f"Starting up agent {agent.name}")

          # construct child thread args
          completeArgs:{} = {}
          completeArgs.update(self.AGENT_CONFIGS[agent.name])
          completeArgs.update(agent.serialize())

          self.PROC_MAP[agent.name] = Process(target=App.appMain, args=(completeArgs,))

          # Start child worker
          self.PROC_MAP[agent.name].start()

          self._logger.info(f"{agent.name} started!")

        else:
          self._logger.warn(f"This is a main thread and not an agent, will not start due to recursion threat.")
      except Exception as e:
        self._logger.error(f"Failed to spin up process {errorStackTrace(e)}")