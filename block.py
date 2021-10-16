import hashlib
# from numpy.core.shape_base import block
import tree
import numpy
import constants

class Block:
    def __init__(self, transactions, newBlk_crTime, cre_id):
        self.timestamp = newBlk_crTime  # Time block was created
        self.id= hashlib.sha256((str(self.timestamp) + str(cre_id)).encode('utf-8')).hexdigest()[:10]; #Block Number
        self.transactions = transactions #Transaction Data
        self.prev = None

    @staticmethod
    def getBlockInterarrivalTime(): # gets time from exponential distribution (mean = Ttx)
        return numpy.random.exponential(scale = constants.Tk, size=None)

class Blockchain:
    def __init__(self):
        self.chain = None

    def searchBlock(self, blockId):
        result = self.chain.searchNode(blockId)
        return result

    def addBlock(self, block): # appends block to longest chain
        if (self.chain == None):
            block.prev = None
            self.chain = tree.Tree(block.id, block)
        else:
            # need to do something else, maybe..
            longestChainLastNode = self.chain.getDeepestNode()
            block.prev = longestChainLastNode.key
            self.chain.addNode(longestChainLastNode.key, block.id, block)

    def addBlockToParent(self, parentId, block):
        block.prev = parentId
        self.chain.addNode(parentId, block.id, block)

    def getLongestChain(self): # does backtracking on deepest node to find longest chain
        deepestNode = self.chain.getDeepestNode()
        currentNode = deepestNode
        longestChain = []
        while(currentNode != None):
            longestChain.append(currentNode.value)
            currentNode = currentNode.parent
        return longestChain

    def getChainEndsWithBlock(self, endBlock):
        currentNode = self.chain.searchNode(endBlock.id)
        theChain = []
        while(currentNode != None):
            theChain.append(currentNode.value)
            currentNode = currentNode.parent
        return theChain

    def getDeepestBlockID(self):
        deepestNode = self.chain.getDeepestNode()
        return deepestNode.key