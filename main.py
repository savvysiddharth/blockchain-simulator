import network
import time
import tree

simulationTimeout = 60 # in seconds

def startSimulation():
    mynetwork = network.Network()
    startTime = time.time()
    while True:
        if(time.time() - startTime >= simulationTimeout):
            break
        for node in mynetwork.nodes:
            node.doRoutine()
    
    doAnalysis(mynetwork)
    

def doAnalysis(network):
    for node in network.nodes:
        node.printNode()
        node.blockchain.chain.printTree()
        for block in node.blockchain.getLongestChain():
            print(block.id,",", end="")
        print("")

# startSimulation()

# WARNING: EXPERIMENTATION ZONE AHEAD!

mytree = tree.Tree("0x001", "LoL_data_a_lot_of_data")
mytree.addNode("0x001", "0x002", "LoL_data_a_lot_of_data")
mytree.addNode("0x001", "0x003", "LoL_data_a_lot_of_data")
mytree.addNode("0x001", "0x004", "LoL_data_a_lot_of_data")

mytree.addNode("0x002", "0x005", "LoL_data_a_lot_of_data")
mytree.addNode("0x002", "0x006", "LoL_data_a_lot_of_data")
mytree.addNode("0x002", "0x007", "LoL_data_a_lot_of_data")
mytree.addNode("0x002", "0x008", "LoL_data_a_lot_of_data")
mytree.printTree()
print('deepest:', mytree.getDeepestNode().key)