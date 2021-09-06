import node
import constants
import random

class Network:
    def __init__(self):
        self.nodes = self._initializeNodes()
        self.graph = self._randomSampling()
        self.threshold = 2**128 # threshold for PROOF-OF-WORK

    def _initializeNodes(self): # generates nodes (z% slow, 100-z% fast)
        nodes = []
        slow = int((constants.Z/100) * constants.TotalNodes);
        fast = constants.TotalNodes - slow;
        id = 0
        for i in range(slow):
            nodes.append(node.Node(id, "slow", self))
            id += 1

        for i in range(fast):
            nodes.append(node.Node(id, "fast", self))
            id += 1

        return nodes

    def _randomSampling(self): # generates connected graph randomly
        graph = [ # hardcoded adjancency list
            [1,2],
            [0,3,4],
            [0],
            [1],
            [1]
        ]
        # get number of peers
        return graph

    def getRandomReceiever(self, sender): 
        peerIndex = random.randrange(0, constants.TotalNodes+1, 1)
        while peerIndex == sender.id:
            peerIndex = random.randrange(0, constants.TotalNodes, 1) # picking a peer differnt from sender
        return peerIndex