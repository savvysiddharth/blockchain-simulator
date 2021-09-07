import numpy as np
import time
import random
from block import Block
from block import Blockchain
from transaction import Transaction
import constants

class Node(object):
    def __init__(self, id, type, network):
        self.id = id
        self.type = type
        self.utxo = [] # list of unspent transactions
        self.blockchain = Blockchain()
        self.network = network # in which network this node belongs to
        self.txnQueue = []
        self.txnSent = [] # when the node is done forwarding, it will trash txn in this list
        self.blockQueue = []
        self.blockSent = [] # when the node is done forwarding, it will trash txn in this list
        self.lastTxnTime = time.time()
        self.TxnInterarrivalTime = Transaction.getTxnInterarrivalTime()
        self.lastBlockTime = time.time()
        self.BlockInterarrivalTime = Block.getBlockInterarrivalTime()
        self.longestChainLength = 1 # bcoz, genesis block is initialized
        self.previouslyAdded = False

    def printNode(self):
        print("nodeId: ", self.id)
        print("type:", self.type)
        # print("utxo:", self.utxo)
        # print("txnQueue:", self.txnQueue)
        # print("txnSent:", self.txnSent)
        print("--------------------------")

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
        self.deleteCoins(coins)
        txn = Transaction(self.id, receiverId, coins)
        self.txnQueue.append(txn)
        return txn

    def generateBlock(self):
        longestChain = self.blockchain.getLongestChain()
        txnsToAddInBlock = []
        for txn in self.txnSent:
            alreadyInBlock = False
            for block in longestChain:
                if txn in block.transactions:
                    pass
                else:
                    alreadyInBlock = True
                    break
            if(not alreadyInBlock):
                txnsToAddInBlock.append(txn)
        newBlock = Block(txnsToAddInBlock)
        return newBlock

    def doRoutine(self): # runs at each loop for each node
        if(time.time() - self.lastTxnTime >= self.TxnInterarrivalTime): # generate transaction if it is time to
            txn = self.generateTransaction()
            if(constants.enableLiveTransactionPrinting):
                txn.printTransaction()
            self.lastTxn = time.time()
            self.TxnInterarrivalTime = Transaction.getTxnInterarrivalTime() # updating for next transaction

        if(time.time() - self.lastBlockTime >= self.BlockInterarrivalTime): # generate block if it is time to
            # if(random.random() > 0.5):
            self.check_new_blocks()
            block = self.generateBlock()
            self.blockchain.addBlock(block) # adds block to current longest chain
            self.longestChainLength += 1
            self.broadcast_block(block)
            self.lastBlockTime = time.time()
            self.BlockInterarrivalTime = Block.getBlockInterarrivalTime()
            if(self.blockchain.getLongestChain()[0].id == self.previouslyAdded):
                print('here..')
                self.broadcast_block(self.previouslyAdded)

        self.check_and_broadcast_transaction() # broadcast txns in txn queue
        # self.check_new_blocks() # checks blocks in block queue
        return

    def check_new_blocks(self):        
        if(self.blockQueue): # if block queue is not empty
            currBlock = self.blockQueue.pop(0)
            blockParentId = currBlock.prev
            if(self.blockchain.searchBlock(blockParentId) != None): # the parent block exists in the blockchain
                self.blockchain.addBlockToParent(blockParentId, currBlock)
                if(len(self.blockchain.getLongestChain()) > self.longestChainLength):
                    self.previouslyAdded = currBlock
        return

    def broadcast_block(self, block):
        nextNodes = self.network.graph[self.id]
        for adjNodeIndex in nextNodes:
            adjNode = self.network.nodes[adjNodeIndex]
            latency = self.latency(adjNode, "block")/1000
            sentTime = time.time()
            while(time.time() - sentTime < latency): # busy waiting
                pass
            adjNode.blockQueue.append(block)
        return

    def coinsOwned(self): # calculates coins owned using utxo
        totalCoins = 0
        for txn in self.utxo:
            totalCoins += txn.coins
        return totalCoins
    
    def deleteCoins(self, coins): # deletes transactions from utxo whose outputs are used
        deletedYet = 0
        toDelete = []
        for i in range(len(self.utxo)):
            needCoins = coins - deletedYet
            if(needCoins == 0):
                break
            if(self.utxo[i].coins >= needCoins):
                self.utxo[i].coins -= needCoins
                if(self.utxo[i].coins == 0):
                    toDelete.append(i)
                break
            else:
                deletedYet += self.utxo[i].coins
                toDelete.append(i)
        for index in toDelete:
            self.utxo[index] = 0
        self.utxo = [i for i in self.utxo if i != 0]
    
    def addTransaction(self, transaction):
        self.txnQueue.append(transaction)

    def check_and_broadcast_transaction(self): # implements Q.6 # broadcasts earliest transaction received
        if self.txnQueue: # if pending txns exist
            currTxn = self.txnQueue.pop(0)
            if currTxn not in self.txnSent: # ensures that txn is not already sent
                self.txnSent.append(currTxn)
                if(currTxn.receiver == self.id): # if this node itself is the reciver, put it in utxo
                    self.utxo.append(currTxn)
                nextNodes = self.network.graph[self.id]
                for adjNodeIndex in nextNodes:
                    adjNode = self.network.nodes[adjNodeIndex]
                    latency = self.latency(adjNode, "transaction")/1000
                    currentTime = time.time()
                    while(time.time() - currentTime < latency): # busy waiting
                        pass
                    adjNode.txnQueue.append(currTxn)
            else: # discard the transaction
                pass