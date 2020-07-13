import redis

class RedisConfig:
    def __init__(self, host, port, db_name: str):
        self.host: str = host
        self.port: int = port
        self.db_name: str = db_name

class RedisConnection:

    REDIS_DBS: {} = {
      # Redis DB for managing threads
      'thread_pool': 0
    }

    def __init__(self, config: RedisConfig):
        self.redis_connection: redis.Redis = redis.Redis(host=config.host, port=config.port, db=RedisConnection.REDIS_DBS[config.db_name], charset='utf-8', decode_responses=True)

    def put_item(self, key, value):
        self.redis_connection.set(key, value)

    def get_item(self, key) -> str:
        return self.redis_connection.get(key)

    def delete_item(self, key) -> None:
        self.redis_connection.delete(key)

    def get_and_delete(self, key):
        get = self.get_item(key)

        self.delete_item(key)

        return get

    def q_size(self) -> int:
        return len(self.redis_connection.keys())
