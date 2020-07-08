import redis
# C:\Program Files\redis-2.4.5-win32-win64\64bit
import json
class ThreadQueue:
    reddis_connection = redis.Redis(host='localhost', port=6379, db='thread_pool', charset='utf-8', decode_responses=True)

    @staticmethod
    def add_thread(config: str):
        ThreadQueue.reddis_connection.set(len(ThreadQueue.reddis_connection.keys()), config)

    @staticmethod
    def get_thread_off_queue():
        r=ThreadQueue.reddis_connection.get('0')

        ThreadQueue.reddis_connection.delete('0')

        return json.loads(r)

    @staticmethod
    def has_thread():
        return len(ThreadQueue.reddis_connection.keys()) > 0