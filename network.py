import node
import constants
import random
import block
import transaction

class Network:
  def __init__(self, env):
    self.nodes = self._initializeNodes(env)
    self.graph = self._randomSampling()
    self._connectNodes(self.graph)
    print(self.graph)


  def _initializeNodes(self, env): # generates nodes (z% slow, 100-z% fast)
    nodes = []
    slow = int((constants.Z/100) * constants.TotalNodes);
    fast = constants.TotalNodes - slow;
    initialTransactions = []
    for i in range(constants.TotalNodes):
      txn = transaction.Transaction(None, i, 50, env.now) # each node gets 50 coins (out of thin air, initially)
      initialTransactions.append(txn)
    genesisBlock = block.Block(initialTransactions, env.now, 0)
    id = 0
    for i in range(slow):
      nodes.append(node.Node(env, id, "slow", self, "no"))
      nodes[id].blockchain.addBlock(genesisBlock)
      nodes[id].utxo.append(initialTransactions[id])
      id += 1

    for i in range(fast-1):
      nodes.append(node.Node(env, id, "fast", self, "no"))
      nodes[id].blockchain.addBlock(genesisBlock)
      nodes[id].utxo.append(initialTransactions[id])
      id += 1

    # THAT ONE BAD NODE!!!!!!!!!
    nodes.append(node.Node(env, id, "fast", self, "stubborn"))
    nodes[id].blockchain.addGenesis(genesisBlock)
    nodes[id].utxo.append(initialTransactions[id])

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
    while edgesUsed <= edges:
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
    
    # graph[n-1] = []
    # for i in range(n):
    #   graph[n-1].append(i)
      
    return graph

  def _connectNodes(self, graph):
    for i in range(constants.TotalNodes):
      for adjNodeId in graph[i]:
        self.nodes[i].adjNodes.append(self.nodes[adjNodeId])

  def getRandomReceiever(self, sender):
    peerIndex = random.randrange(0, constants.TotalNodes, 1)
    while peerIndex == sender.id:
      peerIndex = random.randrange(0, constants.TotalNodes, 1) # picking a peer differnt from sender
    return peerIndex