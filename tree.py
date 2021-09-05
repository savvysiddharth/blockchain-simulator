class TreeNode: # to store the blockchain
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.children = []

class Tree:
    def __init__(self, rootId, rootValue): # we'll store blockId in rootId, and the actual genesis block in rootvalue
        self.root = TreeNode(rootId, rootValue)
        self.totalNodes = 1 # 1 because of root node
    
    def addNode(self, parentId, nodeId, nodeVal):
        parentNode = self.searchNode(parentId)
        if(not parentNode):
            print("Parent not found, can't add node: "+ nodeId)
            return
        parentNode.children.append(TreeNode(nodeId, nodeVal))
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
        return self._getDeepestNode(self.root, self.root)[1]

    def _getDeepestNode(self, currentNode, currentDeepest):
        maxDepth = 0
        for child in currentNode.children:
            childDepth = self._getDeepestNode(child, currentDeepest)[0]
            if(childDepth > maxDepth):
                maxDepth = childDepth
                currentDeepest = child
        maxDepth = maxDepth + 1
        return [maxDepth ,currentDeepest]

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