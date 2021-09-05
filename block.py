import time
import hashlib
from collections import OrderedDict

class TreeNode: # to store the blockchain
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.children = []

class Tree:
    def __init__(self, rootId, rootValue): # we'll store blockId in rootId, and the actual genesis block in rootvalue
        self.root = TreeNode(rootId, rootValue)
        self.totalNodes = 1 # 1 because of root node
    
    def addNode(self, parentId, nodeId, nodeVal):
        parentNode = self.searchNode(parentId)
        if(not parentNode):
            print("Parent not found, can't add node: "+ nodeId)
            return
        parentNode.children.append(TreeNode(nodeId, nodeVal))
        self.totalNodes += 1

    def searchNode(self, keyId):
        return self._searchNode(self.root, keyId)
    
    def _searchNode(self, currentNode, keyId):
        if(currentNode.key == keyId):
            return currentNode
        else:
            for child in currentNode.children:
                return self._searchNode(child, keyId)

    def printTree(self):
        flag = [0] * self.totalNodes
        for i in range(self.totalNodes):
            flag[i] = True
        self._printTree(self.root, flag, 0, False)

    def _printTree(self, x, flag, depth, isLast):
        if (x == None):
            return
        
        for i in range(depth):
            if(flag[i] == True):
                print("| "+"  ",end="")
            else:
                print("  "+"  ",end="")

        if(depth == 0):
            print("Genesis: "+x.key)
        elif(isLast):
            print("+--- " + x.key )
            flag[depth] = False
        else:
            print("+--- " + x.key )

        it = 0
        for child in x.children:
            it += 1
            self._printTree(child, flag, depth+1, it == len(x.children))
        flag[depth] = True

class Block:
    def __init__(self, transactions):
        self.timestamp = time.time();  # Time block was created
        self.nonce = "010101"
        self.index = hashlib.sha256(str(self.timestamp) + str(self.nonce)).hexdigest(); #Block Number
        self.transactions = transactions; #Transaction Data
        self.prevblk_link=None

class Blockchain:
    def __init__(self):
        self.chain = Tree()

    def getLastBlock(self):
        return  self.chain[-1]

    def addBlock(self, block):
        if (len(self.chain) > 0):
            block.prevblk_link = self.getLastBlock().index;
        else:
            block.prevblk_link = None
        self.chain.append(block);


# This class is moved to transaction.py
# class Transactions(object):
#     def __init__(self, sender, reciever, amt):
#         self.sender = sender;
#         self.reciever = reciever;
#         self.amt = amt;
#         self.time = time.time();
#         self.trxnid = hashlib.sha256(str(self.time)).hexdigest();
