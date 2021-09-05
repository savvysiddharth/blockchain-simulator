import transaction
import constants
import random
import time
import numpy

def testTransaction(txn): # TEST FUNCTION : SHOULD BE MOVED TO DIFFERENT FILE
  print("sender:",txn.sender)
  print("receiver:",txn.receiver)
  print("time:",txn.timestamp)
  print("coins:",txn.coins)
  print("--------------------------")

def getPeer(): # should randomly select 2 peers from network
  # add actual code to fetch random peers
  # ...
  peer1 = random.randrange(1000,2000,1)
  peer2 = random.randrange(1000,2000,1)
  while peer2 == peer1:
    peer2 = random.randrange(1000,2000,1) # generating a peer differnt from peer1
  return peer1, peer2

def getTxnInterarrivalTime(): # gets time from exponential distribution (mean = Ttx)
  return numpy.random.exponential(scale = constants.Ttx, size=None)

# GLOBAL VARIABLES
TxnInterarrivalTime = getTxnInterarrivalTime()
LastTxnTime = time.time()

def generateTransaction():
  peer1, peer2 = getPeer()
  # for coins, you need to find out how much coins peer1 owns
  # ..
  coins = random.random() * 50
  txn = transaction.Transaction(peer1, peer2, coins)
  global TxnInterarrivalTime
  TxnInterarrivalTime = getTxnInterarrivalTime()
  return txn

def startSimulation():
  # setup peers and the network
  # ..
  global TxnInterarrivalTime
  global LastTxnTime
  while True: # infinite loop of simulation
    if(time.time() - LastTxnTime >= TxnInterarrivalTime):
      txn = generateTransaction()
      testTransaction(txn)
      TxnInterarrivalTime = getTxnInterarrivalTime()
      LastTxnTime = time.time()

    # randomly generate txn based on exponential distribution
    # ..
  return

startSimulation()

# WARNING: EXPERIMENTATION ZONE AHEAD!

# randtxn = generateTransaction()
# testTransaction(randtxn)

# random_expon = numpy.random.exponential(scale = constants.Ttx, size=None)
# print(random_expon)

# expon_dist_txns = expon.rvs(scale=constants.Ttx, loc=0, size=1000)

# print(expon_dist_txns)

# ax = sns.distplot(expon_dist_txns,
#                   kde=True,
#                   bins=100,
#                   color='skyblue',
#                   hist_kws={"linewidth": 15,'alpha':1})
# ax.set(xlabel='Exponential Distribution', ylabel='Frequency')