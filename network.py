import node
import constants

class Network:
    def __init__(self):
        self.nodes = self.initializeNodes()
        self.graph = self.randomSampling()
        self.threshold = 2**128 # threshold for PROOF-OF-WORK

    def initializeNodes(self): # generates nodes (z% slow, 100-z% fast)
        nodes = []
        slow = int((constants.Z/100) * constants.TotalNodes);
        fast = constants.TotalNodes - slow;
        id = 0
        for i in range(slow):
            nodes.append(node.Node(id, "slow"))
            id += 1

        for i in range(fast):
            nodes.append(node.Node(id, "fast"))
            id += 1

        return nodes

    def randomSampling(self):
        graph = [ # hardcoded adjancency list
            [1,2],
            [0,3,4],
            [0],
            [1],
            [1]
        ]
        # get number of peers
        return graph