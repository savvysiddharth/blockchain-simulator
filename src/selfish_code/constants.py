import numpy as np
import random

TotalNodes = 20 # Total number of nodes in the network
Z = 50 # %percentage of nodes that are slow
Ttx = 1 # mean for interarrival time of Transactions in seconds
Tk = 8 # mean for interarrival time of Blocks in seconds
alpha = 0.3 # mining power is 20% for adversary which is alpha
simTime = 20 # time in seconds, after which simulation ends and analysis are shown
enableLiveTransactionPrinting = True # prints live transactions as it occurs
enableAnalysis = True # shows network graph and blockchains at each node at end
Pij = np.random.uniform(10, 500)
fractionHonestConnected = 0.60


