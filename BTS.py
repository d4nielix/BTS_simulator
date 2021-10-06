from ResourceBlock import ResourceBlock as rb
from User import User
from typing import List
import logging
# from numpy.random import randint, exponential
import time
import matplotlib.pyplot as plt
from Generator import Generator

gnrt = Generator()


def nonzero(p: int):
    tmp = round(gnrt.rndexp(p))
    while tmp <= 0:
        tmp = round(gnrt.rndexp(p))
    return tmp


class BTS:
    def __init__(self, epsilon_: float, k_: int, s_: int, l_: int, logs: logging, iterations: bool, runtime: int,
                 clock: int):
        self.log: logging.Logger = logs.getChild(__name__)
        self.iterations = iterations
        self.epsilon: float = epsilon_
        self.k: int = k_
        self.taken_ks: int = 0
        self.s: int = s_
        self.l: int = l_
        self.tau: float = gnrt.randminmax(1, 10)
        self.lambda1 = 2
        self.lambda2 = 2
        self.t: float = nonzero(self.lambda1)
        self.t2: float = nonzero(self.lambda2)
        self.cycles: int = 0
        self.user_list: List[User] = list()
        self.iterations: bool
        self.users_served: int = 0
        self.users_counter: int = 0
        self.runtime = runtime * 1000
        self.clock = clock
        self.user_avg_time = 0
        self.transmitted_data = 0
        self.wait_list = []
        self.user_throughput = 0
        self.throughput_list = []
        self.retransmissions_time = 0
        self.retransmissions_time_list = []
        self.retransmitted_data = 0
        self.retransmissions_counter = 0
        self.log.log(msg='BTS has been created', level=1)

    def iteration(self):
        self.log.log(msg='Number of users in user list: ' + str(len(self.user_list)), level=1)

        if not self.cycles % self.t:
            self.user_add()
        if not self.cycles % self.t2:
            self.user_add()

        if not self.cycles % self.s and self.user_list:
            self.distribute_resources()
            self.log.log(msg='Resources has been distributed.', level=1)

        if not self.cycles % self.tau and self.user_list:
            self.users_update_bitrate()
            self.log.log(msg='Bitrate has been updated.', level=1)

        for user in self.user_list:
            for rb in user.user_rb_list:
                if rb.issent:
                    user.data -= rb.bitrate
                    self.transmitted_data += rb.bitrate
                    self.user_throughput += rb.bitrate
                    self.log.log(msg='Data has been transmitted.', level=1)
                else:
                    self.retransmissions_counter += 1
                    self.retransmissions_time = time.time()
                    rb.rb_issent()
                    self.retransmitted_data += rb.bitrate
                    self.retransmissions_time_list.append(time.time() - self.retransmissions_time)
                    self.retransmissions_time = 0
                    self.log.log(msg='Updating "issent"', level=1)
            if user.data <= 0:
                self.users_served += 1
                self.taken_ks -= len(user.user_rb_list)
                self.user_avg_time += time.time() - user.start_time
                self.wait_list.append(time.time() - user.start_time)
                self.throughput_list.append(self.user_throughput)
                self.user_throughput = 0
                self.user_remove(user)

        self.cycles += self.clock

    def run(self):
        logging.getLogger('matplotlib.font_manager').disabled = True
        now = time.localtime()
        sim_start = time.strftime("%H:%M:%S", now)
        start_time = time.time()
        while self.cycles < self.runtime:
            self.iteration()
            if self.iterations:
                c = input("Press ENTER for next step, or type 'quit' to quit the simulator.")
                if c == "quit":
                    break

        print("Simulation started: " + sim_start)
        sim_time = round((time.time() - start_time), 2)
        print("Simulation took: %s seconds." % sim_time)
        print("Users at all: " + str(self.users_counter))
        print("Users served: " + str(self.users_served))
        print("Ratio of served users to users at all: " + str(
            round(self.users_served / self.users_counter * 100, 2)) + "%")
        print("Finished cycles: " + str(self.cycles))
        print("Average wait time for being served: %s ms." % round(self.user_avg_time / self.users_served * 1000, 2))
        print("Average system throughput: " + str(round(self.transmitted_data / sim_time, 2)))
        print("Average user throughput: " + str(round(self.transmitted_data / sim_time / self.users_served, 2)))
        print("Average retransmissions counter: " + str(round(self.retransmissions_counter / self.users_counter, 2)))
        print("Average user retransmitted data: " + str(round(self.retransmitted_data / self.users_counter, 2)))

        plt.title('Average wait time for being served')
        plt.xlabel('Average wait time')
        plt.ylabel('Count')
        plt.hist(self.wait_list, 10)
        plt.show()
        plt.close()

        plt.title('Average user throughput')
        plt.xlabel('Average user throughput')
        plt.ylabel('Count')
        plt.hist(self.throughput_list, bins=10)
        plt.show()
        plt.close()

        plt.title('Average retransmissions time')
        plt.xlabel('Average retransmissions time')
        plt.ylabel('Count')
        plt.plot(self.retransmissions_time_list)
        # plt.show()
        # plt.close()

        with open("simdata.csv", "a", newline='') as simdata:
            simdata.write(str(sim_start) + ";" + str(sim_time) + ";" + str(self.users_counter) + ";" + str(
                self.users_served) + ";" + str(
                round(self.users_served / self.users_counter * 100, 2)) + "%;" + str(self.cycles) + ";" + str(
                round(self.user_avg_time / self.users_served * 1000, 2)) + ";" + str(
                round(self.transmitted_data / sim_time, 2)) + ";" + str(
                round(self.transmitted_data / sim_time / self.users_served, 2)) + ";" + str(
                round(self.retransmissions_counter / self.users_counter, 2)) + ";" + str(
                round(self.retransmitted_data / self.users_counter, 2)) + "\r\n")

        # with open("lambdas.csv", "a", newline='') as lambdas: lambdas.write(str(self.lambda1) + ";" + str(
        # self.lambda2) + ";" + str(round(self.user_avg_time / self.users_served * 1000, 2)) + "\r\n")

        with open("throughput.csv", "a", newline='') as throughputfile:
            throughputfile.write(str(self.throughput_list) + "\r\n")

        with open("waittime.csv", "a", newline='') as waittime:
            waittime.write(str(self.wait_list) + "\r\n")

    def user_add(self):
        self.user_list.append(User(logs=self.log, _epsilon=self.epsilon))
        self.log.log(msg='New user has appeared', level=1)
        self.users_counter += 1

    def users_update_bitrate(self):
        for user in self.user_list:
            user.rb_update()

    def user_remove(self, user: User):
        self.user_list.remove(user)
        self.log.log(msg='User has been deleted', level=1)

    def distribute_resources(self):
        for user in self.user_list:
            if not user.has_rb():
                for _ in range(self.l):
                    if self.taken_ks < self.k:
                        user.rb_add_to_list(rb(_epsilon=self.epsilon, logs=user.log))
                        self.taken_ks += 1
