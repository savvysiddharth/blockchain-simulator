import time

class TreeNode: # to store the blockchain
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.arrivalTime = None
        self.children = []
        self.parent = None

class Tree:
    def __init__(self, rootId, rootValue): # we'll store blockId in rootId, and the actual genesis block in rootvalue
        self.root = TreeNode(rootId, rootValue)
        self.totalNodes = 1 # 1 because of root node
    
    def addNode(self, parentId, nodeId, nodeVal):
        parentNode = self.searchNode(parentId)
        if(parentNode == None):
            print("Parent not found, can't add node: "+ nodeId)
            return
        newNode = TreeNode(nodeId, nodeVal)
        newNode.parent = parentNode
        newNode.arrivalTime = time.time()
        parentNode.children.append(newNode)
        self.totalNodes += 1

    def searchNode(self, keyId):
        return self._searchNode(self.root, keyId)

    def _searchNode(self, currentNode, keyId):
        if(currentNode.key == keyId):
            return currentNode
        else:
            for child in currentNode.children:
                return self._searchNode(child, keyId)

    def printTree(self):
        flag = [0] * self.totalNodes
        for i in range(self.totalNodes):
            flag[i] = True
        self._printTree(self.root, flag, 0, False)

    def getDeepestNode(self):
        res = [self.root]
        maxLevel = [-1]
        self._getDeepestNode(self.root, 0, maxLevel, res)
        # print(res[0])
        if(res[0].children):
            res[0] = res[0].children[0]
        return res[0]
    
    def _getDeepestNode(self, currentNode, level, maxLevel, res):
        if(currentNode != None):
            level += 1
            for child in currentNode.children:
               self. _getDeepestNode(child, level, maxLevel, res)
               if(level > maxLevel[0]):
                   res[0] = currentNode
                   maxLevel[0] = level

    # def _getDeepestNode(self, currentNode, currentDeepest, maxDepth):
    #     maxDepth = 0
    #     for child in currentNode.children:
    #         childDepth = self._getDeepestNode(child, currentDeepest, maxDepth)[0]
    #         if(childDepth > maxDepth):
    #             maxDepth = childDepth
    #             currentDeepest = child
    #     maxDepth = maxDepth + 1
    #     return [maxDepth ,currentDeepest]

    def _printTree(self, x, flag, depth, isLast):
        if (x == None):
            return
        
        for i in range(depth):
            if(flag[i] == True):
                print("| "+"  ",end="")
            else:
                print("  "+"  ",end="")

        if(depth == 0):
            print("Genesis: "+x.key)
        elif(isLast):
            print("+--- " + x.key )
            flag[depth] = False
        else:
            print("+--- " + x.key )

        it = 0
        for child in x.children:
            it += 1
            self._printTree(child, flag, depth+1, it == len(x.children))
        flag[depth] = True