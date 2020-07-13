from typing import Any

class IEvent:
    def __init__(self, type: str, context: Any = None):
        self.type = type
        self.context = context

    def serialize(self) -> {}:
        return {
            'type' : self.type,
            'context': self.context
        }

class EventConfig:
    def __init__(self, conf: {}):
        self.conf = conf
        self.lookup: str = conf['CommandLookup'] if 'CommandLookup' in conf.keys() else 'none'

    def is_valid_event(self, event: IEvent) -> bool:
        return True

    def parse_event(self, event: {}):
        return event