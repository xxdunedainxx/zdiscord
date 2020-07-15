from zdiscord.service.Service import Service
import json
import random
from typing import Any

class VoiceFactory(Service):
    def __init__(self, confLocation: str, ffmpeg: str):
        super().__init__(name='MessageFactory')
        self._logger.info("Start up message factory...")
        self.__VOICE_CONFIGS: {} = {}
        self.ffmpeg: str = ffmpeg
        setup: bool = self.__init_config(confLocation)

    def __init_config(self, confLocation: str) -> bool:
        conf: {} = json.load(open(confLocation, encoding='utf-8'))
        self.__VOICE_CONFIGS = conf['voice'] if 'voice' in conf.keys() else {'default' : {'channel_to_join': 'Team Rheem', 'stream_link': 'https://www.youtube.com/embed/kYXRfwXfz5A'}}
        self._logger.info("init voice config")

        return True

    def fetch_stream_link(self) -> str:
        if 'rando' in self.__VOICE_CONFIGS.keys():
            return self.__VOICE_CONFIGS['rando'][random.randint(0, len(self.__VOICE_CONFIGS['rando']) - 1 )]['stream_link']
        else:
            return self.__VOICE_CONFIGS['default']['stream_link']