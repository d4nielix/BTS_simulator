import Network
import logging
import random


def main():
    logging.basicConfig(format='%(name)s - %(asctime)s - %(message)s', level=1)
    network = Network.Network(_epsilon=0.1, _k=15, _s=1, _l=3, _iterations=False, _runtime=1,
                              _clock=1)  # runtime - 1 sek, clock - 1 ms


if __name__ == '__main__':
    main()
