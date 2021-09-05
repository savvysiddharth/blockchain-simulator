import numpy as np
import time

class Node(object):
    def __init__(self, id, type, network):
        self.id = id
        self.type = type
        self.utxo = [] # list of unspent transactions
        self.network = network # in which network this node belongs to
        self.txnQueue = []
        self.txnSent = [] # when the node is done forwarding, it will trash txn in this list

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
    
    def addTransaction(self, transaction):
        self.txnQueue.append(transaction)

    def broadcast(self):
        if self.txnQueues:
            if self.txnQueue[0] not in self.txnSent: # if txn is not already sent..
                currTxn = self.txnQueues.pop(0)
                self.txnSent.append(currTxn)
                nextNodes = self.network.graph[self.id]
                for adjNode in nextNodes:
                    latency = self.latency()/1000
                    currentTime = time.time()
                    while(currentTime - time.time() < latency): # busy waiting
                        pass
                    adjNode.txnQueue.append(currTxn)
                    adjNode.broadcast()