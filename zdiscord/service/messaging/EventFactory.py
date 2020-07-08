from zdiscord.service.Service import Service
from zdiscord.service.messaging.Events import IEvent,EventConfig
import importlib
from typing import Any

class EventFactory(Service):
    def __init__(self, conf: {}):
        super().__init__(name=self.__class__.__name__)
        self.EVENT_IMPORTER = importlib.import_module(self.__module__)
        self._logger.info("Start up event factory...")
        self.__EVENT_CONFIGS: {} = {}
        self.__init_config(conf)




    def __init_config(self, conf: {}):
        for event_config in conf.keys():
            self.__EVENT_CONFIGS[event_config] = []
            for event in conf[event_config]:
                # Type of event must be specified in the config
                if 'type' in event.keys():
                    self.__EVENT_CONFIGS[event_config].append(getattr(self.EVENT_IMPORTER, event['type'])(conf=event))

        self._logger.info("init message config")
        self._logger.info(f"Understood messages: {self.__EVENT_CONFIGS}")



    # Must be defined by client specific middleware
    def parse_message(self, message: str) -> Any:
        raise message

    def is_valid_event(self, event: IEvent) -> EventConfig:
        # Throw away unconfigured events
        if event.type not in self.__EVENT_CONFIGS.keys():
            return None

        for valid_event in self.__EVENT_CONFIGS[event.type]:
            if valid_event.is_valid_event(event):
                return valid_event
        return None
