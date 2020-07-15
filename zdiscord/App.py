

import logging

from zdiscord.service.ServiceFactory import ServiceFactory
from zdiscord.service.Service import Service
from zdiscord.service.integration.weather.Weather import Weather
from zdiscord.service.integration.giphy.Giphy import Giphy
from zdiscord.service.integration.alphav.AlphaV import AlphaV
from zdiscord.service.integration.chat.discord.Discord import Discord
from zdiscord.service.integration.chat.discord.agents.DiscordAgent import DiscordAgent
from zdiscord.service.integration.chat.discord.agents.pollbot.PollAgent import PollAgent
from zdiscord.service.integration.chat.discord.agents.games.tictactoe.TicTacToe import DiscordTicTacToe
from zdiscord.util.logging.LogFactory import LogFactory
from zdiscord.util.error.ErrorFactory import errorStackTrace
from zdiscord.util.general.Main import MainUtil

import json
from typing import Any

# TODO standalone object factory
# App config & object factory
# /usr/bin/ffmpeg
# C:\\Users\\zach\\Documents\\ffmpeg\\ffmpeg-20200615-9d80f3e-win64-static\\bin\\ffmpeg.exe

class App:

    def __init__(self, config: Any, buildAndRun: bool = False):
        self.conf: dict = {}
        self.crash_restarts: int = 3

        # Main classes
        self.chat: Service = None

        # plugins
        self.giphy: Giphy = None
        self.weather: Weather = None
        self.alphav: AlphaV = None

        self.ingest_config(conf=config)

        if buildAndRun:
            self.run_wrapper()

    def run_wrapper(self, logger: logging._loggerClass):
        while self.crash_restarts > 0:
            try:
                logger.info(f"Running app w/ restarts: {self.crash_restarts}")
                MainUtil.init_threadq()
                self.run()
            except Exception as e:
                logger.error(f"Serious problem occured: {errorStackTrace(e)}")
                self.crash_restarts-=1
        raise Exception(f"total crashes reached!")

    def run(self):
        self.chat.run()

    # ingest config
    def ingest_config(self, conf: Any):
        self.conf = json.load(open(conf, encoding='utf-8')) if type(conf) is str else conf
        if 'agent_stamp' in self.conf['chat'].keys() and self.conf['chat']['agent_stamp'] is False:
            MainUtil.init_threadq()

        self.crash_restarts = self.conf['crashRestarts'] if 'crashRestarts' in self.conf.keys() else self.crash_restarts
        self.create_objects()

    # object creation
    def create_objects(self):
        if 'log' in self.conf.keys():
            LogFactory.log_dir = self.conf['log']['log_dir'] if 'log_dir' in self.conf['log'].keys() else LogFactory.log_dir
            LogFactory.log_level = self.conf['log']['log_level'] if 'log_level' in self.conf['log'].keys() else LogFactory.log_level
            LogFactory.log_stdout = self.conf['log']['log_stdout'] if 'log_stdout' in self.conf['log'].keys() else LogFactory.log_stdout

        if 'giphy' in self.conf.keys():
            self.giphy=Giphy(url=self.conf['giphy']['url'], token=self.conf['giphy']['token'])
            ServiceFactory.SERVICES['giphy'] = self.giphy

        if 'weather' in self.conf.keys():
            self.weather=Weather(url=self.conf['weather']['url'], token=self.conf['weather']['token'])
            ServiceFactory.SERVICES['weather'] = self.weather

        if 'alphav' in self.conf.keys():
            self.alphav=AlphaV(url=self.conf['alphav']['url'], token=self.conf['alphav']['token'])
            ServiceFactory.SERVICES['alphav'] = self.alphav

        if 'chat' not in self.conf.keys():
            raise Exception('\'chat\' IS REQUIRED FOR THIS BOT')
        else:
            self.chat = eval(self.conf['chat']['platform'])(self.conf)

    @staticmethod
    def appMain(config):
        try:
            app = App(config=config)
            main_log = LogFactory.get_logger(logName="main")
            main_log.info('Init main')
            app.run_wrapper(main_log)
        except Exception as e:
            print(errorStackTrace(e))
            main_log.error(f"CRITICAL ERROR IN MAIN APP!!! {errorStackTrace(e)}")
            exit(-1)