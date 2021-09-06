import numpy as np
import time
import block
import random
import transaction

class Node(object):
    def __init__(self, id, type, network):
        self.id = id    
        self.type = type
        self.utxo = [] # list of unspent transactions
        self.blockchain = block.Blockchain()
        self.network = network # in which network this node belongs to
        self.txnQueue = []
        self.txnSent = [] # when the node is done forwarding, it will trash txn in this list
        self.lastTxn = time.time()
        self.TxnInterarrivalTime = transaction.Transaction.getTxnInterarrivalTime()

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

    def generateTransaction(self):
        receiverId = self.network.getRandomReceiever(self)
        coins = self.coinsOwned() * (random.random() / 2)
        txn = transaction.Transaction(self.id, receiverId, coins)
        self.txnQueue.append(txn)
        return txn

    def doRoutine(self):
        if(time.time() - self.lastTxn >= self.TxnInterarrivalTime): # generate transaction if it is time to
            txn = self.generateTransaction()
            txn.printTransaction()
            self.lastTxn = time.time()
            self.TxnInterarrivalTime = transaction.Transaction.getTxnInterarrivalTime() # updating for next transaction

        self.broadcast() # broadcast txns in txn queue
        return

    def coinsOwned(self):
        totalCoins = 0
        for txn in self.utxo:
            totalCoins += txn.coins
        return totalCoins
    
    def addTransaction(self, transaction):
        self.txnQueue.append(transaction)

    def broadcast(self): # implements Q.6 # broadcasts earliest transaction received
        if self.txnQueue: # if pending txns exist
            currTxn = self.txnQueue.pop(0)
            if currTxn not in self.txnSent: # ensures that txn is not already sent
                self.txnSent.append(currTxn)
                nextNodes = self.network.graph[self.id]
                for adjNodeIndex in nextNodes:
                    txnRecvNode = self.network.nodes[currTxn.receiver]
                    latency = self.latency(txnRecvNode, "transaction")/1000
                    currentTime = time.time()
                    while(time.time() - currentTime < latency): # busy waiting
                        pass
                    adjNode = self.network.nodes[adjNodeIndex]
                    adjNode.txnQueue.append(currTxn)
                    # adjNode.broadcast()
            else: # discard the transaction
                pass