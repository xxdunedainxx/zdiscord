from zdiscord.util.general.Redis import RedisConnection, RedisConfig
# C:\Program Files\redis-2.4.5-win32-win64\64bit
import json
from typing import Any

class ThreadQueueObject:

    def __init__(self, name: str, context: {}):
        self.name: str = name
        self.context: {} = context

    def serialize(self):
        return {
            "name" : self.name,
            "context" : self.context,
        }

    def serialize_raw(self):
        raw=json.dumps(self.serialize())
        return raw

    @staticmethod
    def deserialize(data: str):
        jObject = json.loads(data)
        return ThreadQueueObject(name=jObject['name'], context=jObject['context'])

class ThreadQueue:

    redis: RedisConnection = None

    @staticmethod
    def add_thread(threadObject: ThreadQueueObject):
        if ThreadQueue.redis is not None:
            items: int = len(ThreadQueue.redis.redis_connection.keys())
            ThreadQueue.redis.put_item(items, threadObject.serialize_raw())
        else:
            return

    @staticmethod
    def get_thread_off_queue(contentType: type=ThreadQueueObject) -> Any:
        print(f"Current keys {ThreadQueue.redis.redis_connection.keys()}")
        if ThreadQueue.redis is not None and len(ThreadQueue.redis.redis_connection.keys()) > 0:
            r: str = ThreadQueue.redis.get_and_delete(ThreadQueue.redis.redis_connection.keys()[0])
            if contentType is ThreadQueueObject:
                return ThreadQueueObject.deserialize(data=r.strip())
            else:
                # basic string message
                return r
        else:
            return None

    @staticmethod
    def has_thread():
        return ThreadQueue.redis is not None and ThreadQueue.redis.q_size() > 0

    @staticmethod
    def init_connection(config: RedisConfig):
        ThreadQueue.redis = RedisConnection(config=config)

