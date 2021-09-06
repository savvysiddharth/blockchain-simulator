import network
import block

def startSimulation():
    mynetwork = network.Network()
    while True:
        for node in mynetwork.nodes:
            node.doRoutine()

startSimulation()

# WARNING: EXPERIMENTATION ZONE AHEAD!

mytree = block.Tree("0x001", "LoL_data_a_lot_of_data")
mytree.addNode("0x001", "0x002", "LoL_data_a_lot_of_data")
mytree.addNode("0x001", "0x003", "LoL_data_a_lot_of_data")
mytree.addNode("0x001", "0x004", "LoL_data_a_lot_of_data")

mytree.addNode("0x002", "0x005", "LoL_data_a_lot_of_data")
mytree.addNode("0x002", "0x006", "LoL_data_a_lot_of_data")
mytree.addNode("0x002", "0x007", "LoL_data_a_lot_of_data")
mytree.addNode("0x002", "0x008", "LoL_data_a_lot_of_data")
mytree.printTree()
print(mytree.getDeepestNode())