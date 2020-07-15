from multiprocessing import Process
from datetime import datetime

from zdiscord.util.general.Job import Job

# Represents a currently running job
class JobProcess:

  def __init__(self, jobRef: Job, ttl: int = 1800):
    # Default 30 minutes as time to live
    self.time_to_live_seconds: int = ttl

    self.spin_up_time: datetime = None
    self.process: Process = None
    self.job = jobRef

  def timed_out(self):
    return (datetime.now() - self.spin_up_time).seconds > self.time_to_live_seconds

  def run(self):
    self.spin_up_time = datetime.now()

    self.process.start()


  # Destroy process if its timed out
  def expire(self):
    if self.timed_out():
      if self.process.is_alive():
        self.process.kill()