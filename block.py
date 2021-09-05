import time
import hashlib
import tree

class Block:
    def __init__(self, transactions):
        self.timestamp = time.time();  # Time block was created
        self.nonce = "010101"
        self.index = hashlib.sha256(str(self.timestamp) + str(self.nonce)).hexdigest(); #Block Number
        self.transactions = transactions; #Transaction Data
        self.prevblk_link=None

class Blockchain:
    def __init__(self):
        self.chain = None

    def getLastBlock(self):
        return  self.chain[-1]

    def addBlock(self, block): # appends block to longest chain
        if (self.chain == None):
            block.prevblk_link = None
            self.chain = tree.Tree(block.index, block)
        else:
            # need to do something else, maybe..
            longestChainLastNode = self.chain.getDeepestNode()
            block.prevblk_link = longestChainLastNode.key
            self.chain.addNode(longestChainLastNode.key, block.index, block)