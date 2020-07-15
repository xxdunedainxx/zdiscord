from zdiscord.util.general.Job import Job
import time
class BasicJob(Job):

    def __init__(self, name: str, interval: str, length: int):
        Job.__init__(self, name, interval, length)

    def execute_job(self):
        print("Blah testing..")