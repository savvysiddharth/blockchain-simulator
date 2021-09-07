import time
import constants
import numpy


class Simulation(object):

    def __init__(self, node):
        self.node = node
        self.env = self.node.env
        self.env.process(self.start_simulation())



    def start_simulation(self):
        self.node.simu_t = time.time()

        if self.node.simu_t > self.node.last_trxn_time + numpy.random.exponential(scale = constants.Ttx, size=None):
            self.node.transaction_generation()

        if self.node.simu_t > self.node.last_blk_time + numpy.random.exponential(scale = constants.Tk_mean_val, size=None):
            self.node.blk_generate()

        yield self.env.timeout(1)






