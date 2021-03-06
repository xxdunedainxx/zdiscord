from zdiscord.service.integration.weather.Weather import Weather
from zdiscord.service.integration.giphy.Giphy import Giphy
from zdiscord.service.integration.chat.discord.DiscordClient import DiscordBot
from zdiscord.service.messaging.MessageFactory import MessageFactory
from zdiscord.util.logging.LogFactory import LogFactory

import json

# TODO standalone object factory
# App config & object factory

class App:

    def __init__(self, config_path: str):
        self.conf: dict = {}

        # Main classes
        self.discord: DiscordBot = None
        self.messager: MessageFactory = None

        # plugins
        self.giphy: Giphy = None
        self.weather: Weather = None

        self.ingest_config(conf=config_path)
        self.__message_factory_injection()

    # ingest config
    def ingest_config(self, conf: str):
        self.conf = json.load(open(conf, encoding='utf-8'))

        self.create_objects()

    # object creation
    def create_objects(self):
        if 'chat' not in self.conf.keys() or 'message_factory' not in self.conf.keys():
            raise Exception('\'chat\' IS REQUIRED FOR THIS BOT')
        else:
            self.messager = MessageFactory(self.conf['message_factory'])
            self.discord = DiscordBot(messager=self.messager)

        if 'log' in self.conf.keys():
            # TODO : set log level here?
            LogFactory.log_dir = self.conf['log']['log_dir'] if 'log_dir' in self.conf['log'].keys() else LogFactory.log_dir

        if 'giphy' in self.conf.keys():
            self.giphy=Giphy(url=self.conf['giphy']['url'], token=self.conf['giphy']['token'])

        if 'weather' in self.conf.keys():
            self.weather=Weather(url=self.conf['weather']['url'], token=self.conf['weather']['token'])

    # Message factory
    def __message_factory_injection(self):
        if self.giphy is not None:
            self.messager.add_config(key='giphy', value=self.giphy.get_giphy)

        if self.weather is not None:
            self.messager.add_config(key='weather', value=self.weather.get_weather)