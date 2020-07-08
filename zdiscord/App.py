import logging

from zdiscord.service.ServiceFactory import ServiceFactory
from zdiscord.service.integration.weather.Weather import Weather
from zdiscord.service.integration.giphy.Giphy import Giphy
from zdiscord.service.integration.alphav.AlphaV import AlphaV
from zdiscord.service.integration.chat.IChatMiddleware import IChatMiddleware
from zdiscord.service.integration.chat.discord.DiscordMiddleware import DiscordMiddleware
from zdiscord.util.logging.LogFactory import LogFactory
from zdiscord.util.error.ErrorFactory import errorStackTrace

import json

# TODO standalone object factory
# App config & object factory

class App:

    def __init__(self, config_path: str, buildAndRun: bool = False):
        self.conf: dict = {}
        self.crash_restarts: int = 3

        # Main classes
        self.chat_middleware: IChatMiddleware = None

        # plugins
        self.giphy: Giphy = None
        self.weather: Weather = None
        self.alphav: AlphaV = None

        self.ingest_config(conf=config_path)

        if buildAndRun:
            self.run()

    def run_wrapper(self, logger: logging._loggerClass):
        while self.crash_restarts > 0:
            try:
                logger.info(f"Running app w/ restarts: {self.crash_restarts}")
                self.run()
            except Exception as e:
                logger.error(f"Serious problem occured: {errorStackTrace(e)}")
                self.crash_restarts-=1
        raise Exception(f"total crashes reached!")

    def run(self):
        self.chat_middleware.run()

    # ingest config
    def ingest_config(self, conf: str):
        self.conf = json.load(open(conf))
        self.crash_restarts = self.conf['crashRestarts'] if 'crashRestarts' in self.conf.keys() else self.crash_restarts
        self.create_objects()

    # object creation
    def create_objects(self):
        if 'log' in self.conf.keys():
            LogFactory.log_dir = self.conf['log']['log_dir'] if 'log_dir' in self.conf['log'].keys() else LogFactory.log_dir
            LogFactory.log_level = self.conf['log']['log_level'] if 'log_level' in self.conf['log'].keys() else LogFactory.log_level
            LogFactory.log_stdout = self.conf['log']['log_stdout'] if 'log_stdout' in self.conf['log'].keys() else LogFactory.log_stdout

        # TODO : default giphy
        if 'giphy' in self.conf.keys():
            self.giphy=Giphy(url=self.conf['giphy']['url'], token=self.conf['giphy']['token'])
            ServiceFactory.SERVICES['giphy'] = self.giphy

        if 'weather' in self.conf.keys():
            self.weather=Weather(url=self.conf['weather']['url'], token=self.conf['weather']['token'])
            ServiceFactory.SERVICES['weather'] = self.weather

        if 'alphav' in self.conf.keys():
            self.alphav=AlphaV(url=self.conf['alphav']['url'], token=self.conf['alphav']['token'])
            ServiceFactory.SERVICES['alphav'] = self.alphav

        if 'chat' not in self.conf.keys() or 'message_factory' not in self.conf.keys():
            raise Exception('\'chat\' IS REQUIRED FOR THIS BOT')
        else:
            #TODO generic service config
            self.chat_middleware = eval(self.conf['chat']['platform'])(self.conf)
