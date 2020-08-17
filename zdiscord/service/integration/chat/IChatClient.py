from zdiscord.service.integration.Integration import IIntegration

class IChatClient(IIntegration):


    def __init__(self, name: str):
        super().__init__(name=name)

    def run(self):
        pass

    def is_alive(self) -> bool:
        return True