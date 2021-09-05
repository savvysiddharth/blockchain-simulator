import time
import hashlib

class Block:
    def __init__(self, transactions):
        self.timestamp = time.time();  # Time block was created
        self.nonce = "010101"
        self.index = hashlib.sha256(str(self.timestamp) + str(self.nonce)).hexdigest(); #Block Number
        self.transactions = transactions; #Transaction Data
        self.prevblk_link=None

class Blockchain:
    def __init__(self):
        self.chain = []; #Blockchain is an array of Blocks

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
