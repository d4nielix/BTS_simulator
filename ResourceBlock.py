from numpy.random import randint, random_sample
import logging


class ResourceBlock:
    def __init__(self, logs: logging, _epsilon: float):
        self.log: logging.Logger = logs.getChild(__name__)
        self.bitrate: int = randint(low=20, high=800)
        self.epsilon = _epsilon
        self.issent: bool = self.epsilon <= random_sample()

    def rb_issent(self):
        self.issent = self.epsilon <= random_sample()

    def rb_update_bitrate(self):
        self.bitrate = randint(low=20, high=800)