import numpy as np

class Node(object):
    def __init__(self, id, type):
        self.id = id
        self.type = type
        self.utxo = [] # list of unspent transactions

    def latency(self, b, msg_type):
        Pij = np.random.uniform(10, 500)  # in ms as per question
        if self.type == 'fast' and b.type == 'fast':
          Cij = 100 * pow(10, 3)  # in ms
        else:
          Cij = 5 * pow(10, 3)

        if msg_type == "transaction":
          m = 0
        elif msg_type == "block":
          m = 8 * (10 ** 6)

        mean = 96*pow(10,3)/Cij
        Dij = np.random.exponential((1/mean),1)[0]
        tot_delay =Pij+Dij+(m/Cij)
        return tot_delay