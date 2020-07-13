from multiprocessing import Process
from datetime import datetime

from zdiscord.util.general.Agent import Agent

# Represents a currently running agent process
class AgentProcess:

  def __init__(self, ttl: int = 1800):
    # Default 30 minutes as time to live
    self.time_to_live_seconds: int = ttl
    self.spin_up_time: datetime = None
    self.process: Process = None

  def timed_out(self):
    return (datetime.now() - self.spin_up_time).seconds > self.time_to_live_seconds

  def run(self):
    self.spin_up_time = datetime.now()

    self.process.start()


  # Destroy process if its timed out
  def expire(self):
    if self.timed_out():
      self.process.kill()