from zdiscord.service.ThreadQ import ThreadQueue
from zdiscord.util.general.Redis import RedisConfig
import json
from zdiscord.util.logging.LogFactory import LogFactory
from zdiscord.util.error.ErrorFactory import errorStackTrace

class MainUtil:

  @staticmethod
  def load_master_config(path: str) -> {}:
    return json.load(open(path, encoding='utf-8'))

  @staticmethod
  def init_threadq():
    MASTER_CONFIG: dict = MainUtil.load_master_config('./zdiscord/master.json')

    # Thread Q Redis Set up
    ThreadQConfig: RedisConfig = RedisConfig(MASTER_CONFIG['thread_q']['redis']['host'],
                                             MASTER_CONFIG['thread_q']['redis']['port'],
                                             MASTER_CONFIG['thread_q']['redis']['db'])
    ThreadQueue.init_connection(ThreadQConfig)