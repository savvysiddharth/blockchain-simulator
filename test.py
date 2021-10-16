from tree import Tree

mytree = Tree("0", None)

mytree.addNode("0", "1", None)
mytree.addNode("0", "2", None)


mytree.addNode("1", "alpha", None)
mytree.addNode("2", "beta", None)

mytree.printTree()