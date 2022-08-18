import time
import hashlib
import numpy
import constants

class Transaction:
    def __init__(self, sender, receiver, coins, txnGeneratedAt):
        self.sender = sender
        self.receiver = receiver
        self.timestamp = txnGeneratedAt
        self.coins = coins
        self.id = hashlib.sha256(str(str(self.timestamp)+str(sender)).encode('utf-8')).hexdigest()

    def printTransaction(self):
        print("txnId: ", self.id)
        print("sender:",self.sender)
        print("receiver:",self.receiver)
        print("time:",self.timestamp)
        print("coins:",self.coins)
        print("--------------------------")

    @staticmethod
    def getTxnInterarrivalTime(): # gets time from exponential distribution (mean = Ttx)
        return numpy.random.exponential(scale = constants.Ttx, size=None)