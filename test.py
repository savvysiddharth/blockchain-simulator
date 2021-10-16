from tree import Tree

mytree = Tree("0", "0th")
mytree.addNode("0", "1", "1st")
mytree.addNode("0", "2", "2nd")
mytree.addNode("1", "3", "3rd")
mytree.addNode("3", "gamma", "GAMMA")
mytree.addNode("2", "4", "4th")
mytree.addNode("4", "alpha", "ALPHA")
mytree.addNode("4", "beta", "BETA")


mytree.printTree()

def getLongestChain(mytree): # does backtracking on deepest node to find longest chain
  deepestNode = mytree.getDeepestNode()
  currentNode = deepestNode
  longestChain = []
  while(currentNode != None):
    longestChain.append(currentNode.value)
    currentNode = currentNode.parent
  return longestChain

chain = getLongestChain(mytree) 
print(chain)
print(len(chain))

# ans = mytree.getDeepestNodes()
# for node in ans:
#   print(node.key)