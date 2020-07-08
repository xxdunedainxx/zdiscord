from zdiscord.service.integration.Integration import IIntegration
from zdiscord.service.integration.chat.IChatClient import IChatClient
from zdiscord.service.messaging.EventFactory import EventFactory
from zdiscord.service.messaging.CommandFactory import CommandFactory
from zdiscord.service.messaging.EventFactory import IEvent, EventConfig
from zdiscord.util.error.ErrorFactory import errorStackTrace
from typing import Any

class IChatMiddleware(IIntegration):

    def __init__(self, conf: {}):
        super().__init__(name=self.__class__.__name__)
        self._chat_client: IChatClient = None
        self._ef: EventFactory = None
        self._cf: CommandFactory = None

    def run(self):
        self._chat_client.run()

    def event_subscriber(self, event: IEvent):
        self._logger.info(f"Event from discord client \'{str(event.type)}\'")
        try:
            event_config: EventConfig = self._ef.is_valid_event(event=event)

            # Throw away invalid events
            if event is None:
                return

            self._cf.execute_cmd(event, event_config)
        except Exception as e:
            self._logger.error(f"Failed to process event {errorStackTrace(e)}")
            return