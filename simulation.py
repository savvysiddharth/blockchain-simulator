import simpy
import network
import node
import constants

env = simpy.Environment()
mynetwork = network.Network(env)
# peers = mynetwork.nodes
for node in mynetwork.nodes:
    if(node.badType == "stubborn"):
        env.process(node.runStubborn())
    else:
        env.process(node.run())
env.run(until = constants.simTime)


def doAnalysis(network):
    for node in network.nodes:
        print("--------------------------")
        node.printNode()
        #node.printTxn()

        node.blockchain.chain.printTree()
        # print the longest chain
        print('[ ', end="")
        for block in node.blockchain.getLongestChain():
            print(block.id, ",", end="")
        print(" ]")


doAnalysis(mynetwork)
