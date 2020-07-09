from zdiscord.util.general.Redis import RedisConnection, RedisConfig
# C:\Program Files\redis-2.4.5-win32-win64\64bit
import json


class ThreadQueue:

    redis: RedisConnection = None

    @staticmethod
    def add_thread(config: str):
        if ThreadQueue.redis is not None:
            ThreadQueue.redis.put_item(len(ThreadQueue.reddis_connection.keys()), config)
            k=ThreadQueue.redis.redis_connection.keys()
            return

    @staticmethod
    def get_thread_off_queue():
        if ThreadQueue.redis is not None and '0' in ThreadQueue.redis.redis_connection.keys():
            r = ThreadQueue.redis.get_and_delete('0')
            return json.loads(r)
        else:
            return None

    @staticmethod
    def has_thread():
        return ThreadQueue.redis is not None and ThreadQueue.redis.q_size() > 0

    @staticmethod
    def init_connection(config: RedisConfig):
        ThreadQueue.redis = RedisConnection(config=config)
