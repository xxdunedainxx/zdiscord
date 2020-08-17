from zdiscord.service.Service import Service
import random
import string
from typing import Any

class Job(Service):
    def __init__(self, name: str, interval: str, length: int, conf: {}, enabled: bool = True):
        Service.__init__(self, name=self.__class__.__name__)
        self.name: str = name
        self.interval: str = interval
        self.length: int = length
        self.job_reference: Any = None
        self.conf: {} = conf
        self.enabled = enabled

    def execute_job(self, *args, **kwargs):
        pass

    def job_id(self) -> str:
        return f"{self.name}-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"

    def job_is_alive(self) -> bool:
        return False

    def kill_job(self) -> None:
        pass