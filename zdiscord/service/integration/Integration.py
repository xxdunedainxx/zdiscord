from zdiscord.service.Service import Service

class IIntegration(Service):
    def __init__(self, name: str):
        super().__init__(name=name)