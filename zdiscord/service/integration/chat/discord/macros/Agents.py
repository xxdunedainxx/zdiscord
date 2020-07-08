from zdiscord.App import App

"""
from pathos.multiprocessing import ProcessingPool as Pool
import time

p = Pool(1)
p.map(self.__middleware.run, [self])

while True:
    time.sleep(5)
    p.join()
"""
from pathos.multiprocessing import ProcessingPool as Pool
import queue
def create_app_process(conf:{}):
    p = Pool(1)
    p.map(App, [conf, True])