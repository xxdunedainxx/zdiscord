from zdiscord.service.Service import Service
import json
from typing import Any

class VoiceFactory(Service):
    def __init__(self, confLocation: str):
        super().__init__(name='MessageFactory')
        self._logger.info("Start up message factory...")
        self.__VOICE_CONFIGS: {} = {}
        self.__init_config(confLocation)

    def __init_config(self, confLocation: str):
        conf: {} = json.load(open(confLocation))

        self.__VOICE_CONFIGS['voice_channel'] = conf['voice_channel'] if 'voice_channel' in conf.keys() else {'channel_to_join': 'Team Rheem', 'stream_link': 'https://www.youtube.com/embed/kYXRfwXfz5A'}
        self.channel = self.__VOICE_CONFIGS['voice_channel']['channel_to_join']
        self.stream_link = self.__VOICE_CONFIGS['voice_channel']['stream_link']
        self._logger.info("init voice config")