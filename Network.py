import BTS
import logging


class Network:
    def __init__(self, _epsilon: float, _k: int, _s: int, _l: int, _runtime: int, _clock: int, _iterations=False):
        self.log: logging.Logger = logging.getLogger(__name__)
        self.log.log(msg='Network has been created', level=1)
        self.epsilon: float = _epsilon
        self.k: int = _k
        self.s: int = _s
        self.l: int = _l
        self.runtime = _runtime
        self.clock = _clock
        self.bts: BTS = BTS.BTS(epsilon_=self.epsilon, k_=self.k, s_=self.s, l_=self.l, logs=self.log, iterations=_iterations, runtime=self.runtime, clock=self.clock)
        self.bts.run()
