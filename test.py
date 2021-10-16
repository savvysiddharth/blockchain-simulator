from tree import Tree

mytree = Tree("0", None)

mytree.addNode("0", "1", None)
mytree.addNode("0", "2", None)

mytree.addNode("1", "3", None)
mytree.addNode("3", "gamma", None)

mytree.addNode("2", "4", None)

mytree.addNode("4", "alpha", None)
mytree.addNode("4", "beta", None)


mytree.printTree()

ans = mytree.getDeepestNodes()
for node in ans:
  print(node.key)
