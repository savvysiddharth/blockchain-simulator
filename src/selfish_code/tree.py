import time


class TreeNode:  # to store the blockchain
  def __init__(self, key, value):
    self.key = key
    self.value = value
    self.arrivalTime = None
    self.children = []
    self.parent = None


class Tree:
  def __init__(self, rootId, rootValue):  # we'll store blockId in rootId, and the actual genesis block in rootvalue
    self.root = TreeNode(rootId, rootValue)
    self.totalNodes = 1  # 1 because of root node

  def addNode(self, parentId, nodeId, nodeVal):
    parentNode = self.searchNode(parentId)
    if (parentNode == None):
      print("Parent:" + parentId + ", not found, can't add node: " + nodeId)
      return
    newNode = TreeNode(nodeId, nodeVal)
    newNode.parent = parentNode
    newNode.arrivalTime = time.time()
    parentNode.children.append(newNode)
    self.totalNodes += 1

  def searchNode(self, keyId):
    return self._searchNode(self.root, keyId)

  def _searchNode(self, currentNode, keyId):
    if (currentNode.key == keyId):
      return currentNode
    else:
      for child in currentNode.children:
        res = self._searchNode(child, keyId)
        if(res != None):
          return res

  def printTree(self):
    flag = [0] * self.totalNodes
    for i in range(self.totalNodes):
      flag[i] = True
    self._printTree(self.root, flag, 0, False)

  def printToFile(self, file_id):
    flag = [0] * self.totalNodes
    for i in range(self.totalNodes):
      flag[i] = True
    filename = "node" + str(file_id) + ".txt"
    f = open(filename, 'w')
    f.write('----------------')
    f.write('\n')
    f.write('nodeID : ' + str(file_id))
    f.write("\n")
    f.write("-----------------")
    f.write("\n")
    f.close()
    self._printToFile(self.root, flag, 0, False, filename)

  def getDeepestNode(self): # gives earliest arriving deepest node
    res = [self.root] # list, because we want pass by reference
    maxLevel = [-1]
    self._getDeepestNode(self.root, 0, maxLevel, res)
    # print(res[0])
    if (res[0].children):
      res[0] = res[0].children[0]
    return res[0]

  def _getDeepestNode(self, currentNode, level, maxLevel, res):
    if (currentNode != None):
      level += 1
      for child in currentNode.children:
        self._getDeepestNode(child, level, maxLevel, res)
        if (level > maxLevel[0]):
          res[0] = currentNode
          maxLevel[0] = level

  def getDeepestNodes(self): # returns list of nodes at same depth (only deepest ones)
    res = [self.root]
    maxLevel = [0]
    self._getDeepestNodes(self.root, 0, maxLevel, res)
    return res

  def _getDeepestNodes(self, currentNode, level, maxLevel, res):
    if (currentNode != None):
      level += 1
      for child in currentNode.children:
        self._getDeepestNodes(child, level, maxLevel, res)
        if (level > maxLevel[0]):
          res.clear()
          res.append(child)
          maxLevel[0] = level
        elif (level == maxLevel[0]):
          res.append(child)

  # def _getDeepestNode(self, currentNode, currentDeepest, maxDepth):
  #   maxDepth = 0
  #   for child in currentNode.children:
  #     childDepth = self._getDeepestNode(child, currentDeepest, maxDepth)[0]
  #     if(childDepth > maxDepth):
  #       maxDepth = childDepth
  #       currentDeepest = child
  #   maxDepth = maxDepth + 1
  #   return [maxDepth ,currentDeepest]

  def _printTree(self, x, flag, depth, isLast):
    if (x == None):
      return

    for i in range(depth):
      if (flag[i] == True):
        print("| " + "  ", end="")
      else:
        print("  " + "  ", end="")

    if (depth == 0):
      print("Genesis: " + x.key)
    elif (isLast):
      print("+--- " + x.key)
      flag[depth] = False
    else:
      print("+--- " + x.key)
    it = 0
    for child in x.children:
      it += 1
      self._printTree(child, flag, depth + 1, it == len(x.children))
    flag[depth] = True

  def _printToFile(self, x, flag, depth, isLast, filename):
    f = open(str(filename), "a")

    if (x == None):
      return

    for i in range(depth):
      if (flag[i] == True):
        f.write("| " + "  ")
      else:
        f.write("  " + "  ")

    if (depth == 0):
      f.write("Genesis " + str(x.key) + " : " + str(x.arrivalTime))
      f.write('\n')
    elif (isLast):
      f.write("+--- " + str(x.key) + " : " + str(x.arrivalTime))
      f.write('\n')
      flag[depth] = False
    else:
      f.write("+--- " + str(x.key) + " : " + str(x.arrivalTime))
      f.write('\n')
    f.close()
    it = 0
    for child in x.children:
      it += 1
      self._printToFile(child, flag, depth + 1, it == len(x.children), filename)
    flag[depth] = True