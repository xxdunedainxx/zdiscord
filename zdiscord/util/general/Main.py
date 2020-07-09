from zdiscord.service.ThreadQ import ThreadQueue
from zdiscord.util.general.Redis import RedisConfig
import json

class MainUtil:

  @staticmethod
  def load_master_config(path: str) -> {}:
    return json.load(open(path))

  @staticmethod
  def init_threadq():
    MASTER_CONFIG: dict = MainUtil.load_master_config('./zdiscord/master.json')

    # Thread Q Redis Set up
    ThreadQConfig: RedisConfig = RedisConfig(MASTER_CONFIG['thread_q']['redis']['host'],
                                             MASTER_CONFIG['thread_q']['redis']['port'],
                                             MASTER_CONFIG['thread_q']['redis']['db'])
    ThreadQueue.init_connection(ThreadQConfig)