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
        n = constants.TotalNodes
        graph = []
        visited = []
        for i in range(n):
            graph.append([])
            visited.append(False)

        edges = random.randrange(n-1, n*(n-1)/2)
        edgesUsed = 0 # to keep track of current edges
        currentNode = random.randrange(0,n)
        visited[currentNode] = True
        # Begin random walk..
        while(edgesUsed <= edges):
            availableChildren = []
            if(edgesUsed < n-1): # if graph is not connected yet..
                for i in range(n):
                    if(visited[i] == False and i != currentNode): # make edge only with unvisited node
                        availableChildren.append(i)
            else: # done connecting the graph
                for i in range(n):
                    if(i != currentNode): # make edge with any node except with itself
                        availableChildren.append(i)
                availableChildren = list(set(availableChildren) - set(graph[currentNode]))
            if(len(availableChildren) == 0):
                currentNode = random.randrange(0,n)
                continue
            nextNode = availableChildren[random.randrange(0,len(availableChildren))]
            graph[currentNode].append(nextNode) # add edge into the graph
            graph[nextNode].append(currentNode) # bcoz, undirected
            edgesUsed += 1
            visited[nextNode] = True
            currentNode = nextNode # move to the next node

        return graph

    def getRandomReceiever(self, sender): 
        peerIndex = random.randrange(0, constants.TotalNodes, 1)
        while peerIndex == sender.id:
            peerIndex = random.randrange(0, constants.TotalNodes, 1) # picking a peer differnt from sender
        return peerIndex