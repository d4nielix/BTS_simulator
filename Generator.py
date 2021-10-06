import math
import random


class Generator:
    def __init__(self):
        self.M: int = 2147483647
        self.A: int = 16807
        self.Q: int = 127773
        self.R: int = 2836
        self.fibon = [1,
                      2,
                      3,
                      5,
                      8,
                      13,
                      21,
                      34,
                      55,
                      89,
                      144,
                      233,
                      377,
                      610,
                      987,
                      1597,
                      2584,
                      4181,
                      6765,
                      10946,
                      17711,
                      28657,
                      46368,
                      75025,
                      121393,
                      196418,
                      317811,
                      514229,
                      832040,
                      1346269,
                      2178309,
                      3524578,
                      5702887,
                      9227465,
                      14930352,
                      24157817,
                      39088169,
                      63245986,
                      102334155,
                      165580141,
                      267914296,
                      433494437,
                      701408733]
        self.kernel: int = random.choice(self.fibon)

    def randomizer(self):
        h = math.floor(self.kernel / self.Q)
        self.kernel = self.A * (self.kernel - self.Q * h) - self.R * h
        if self.kernel < 0:
            self.kernel += self.M
        return self.kernel / self.M

    def randminmax(self, min: int, max: int):
        return self.randomizer() * (max - min) + min

    def rndexp(self, lambdavar: int):
        k = self.randomizer()
        return -(1.0 / lambdavar) * math.log(k)

    def rndzeroone(self, p: float):
        k = self.randomizer()
        if k < p:
            return 1
        else:
            return 0
