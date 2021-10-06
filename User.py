from ResourceBlock import ResourceBlock as rb
from numpy.random import randint as rnd
from typing import List
import logging
import time


class User:
    def __init__(self, logs: logging, _epsilon: float):
        self.log: logging.Logger = logs.getChild(__name__)
        self.data: int = rnd(low=1, high=10) * 250
        self.epsilon = _epsilon
        self.start_time = time.time()
        self.user_rb_list: List[rb] = list()

    def rb_add_to_list(self, element: rb) -> None:
        self.user_rb_list.append(element)
        self.log.log(msg='RB has been added to list', level=1)

    def rb_update(self):
        for rb in self.user_rb_list:
            rb.rb_update_bitrate()
        self.log.log(msg='RB has been updated', level=1)

    def has_rb(self):
        return len(self.user_rb_list) == 3