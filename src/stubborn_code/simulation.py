import simpy
import network
import node
import constants
from treelib import Node as Node1
from treelib import Tree as Tree1

env = simpy.Environment()
mynetwork = network.Network(env)
#print(mynetwork.nodes)
#mynetwork.nodes.reverse()
#print(mynetwork.nodes)
for node in mynetwork.nodes:
    env.process(node.run())
env.run(until=160)


def doAnalysis(network):
    minedBlksCount = 0
    MainChainBlkLen = 0
    for node in network.nodes:
        print("--------------------------")
        node.printNode()
        minedBlksCount= minedBlksCount + len(node.minedBlks)
        #node.printTxn()

        #node.blockchain.chain.printTree()
        # print the longest chain
        print('[ ', end="")
        for block in node.blockchain.getLongestChain():
            print(block.id, ",", end="")
        print(" ]")
        MainChainBlkLen = len(node.blockchain.getLongestChain())

        mainblkckainBLKID = []
        #print(node.blockchain.getLongestChain())
        for blks in node.blockchain.getLongestChain():
            mainblkckainBLKID.append(blks.id)
        print(mainblkckainBLKID)


#using treelib tool for graph visualisation
        if(node.id < constants.TotalNodes):
            tree1 = Tree1()
            print(node.blockchain.chain.root.key)
            tree1.create_node(node.blockchain.chain.root.key,node.blockchain.chain.root.key)
            #for child in node.blockchain.chain.root.children:
            #   tree1.create_node(child.key,parent=child.parent.key)
            childrenList = node.blockchain.chain.root.children
            while(len(childrenList)>0):
                child1 = childrenList[0]
                tree1.create_node(child1.key,child1.key,parent=child1.parent.key)
                childrenList.extend(child1.children)
                childrenList.remove(child1)

            #tree1.create_node("Harry", "harry")  # No parent means its the root node
            #tree1.create_node("Jane", "jane", parent="harry")
            #tree1.create_node("Bill", "bill", parent="harry")
            #tree1.create_node("Diane", "diane", parent="jane")
            #tree1.create_node("Mary", "mary", parent="diane")
            #tree1.create_node("Mark", "mark", parent="jane")

            tree1.show()

#Analusis of MPU required
        if(node.id == constants.TotalNodes-1):
            node.printPrvChain()
            count=0
            listing=[]
            print("hola")
            print(node.privateblkchain.keys())

            for blockid in node.privateblkchain.keys():
                for blockid1 in mainblkckainBLKID:
                    if(blockid == blockid1):
                        listing.append(blockid)
                        count = count+1
                        break
            print("private mined blks in main chain ",count)
            print(listing)
            totalSlfishMinedBlks=len(node.privateblkchain.keys())
            print("total private mined blks ",totalSlfishMinedBlks)
            print("MPU node adv = ",(count/totalSlfishMinedBlks))


    print("main blk chain len ",MainChainBlkLen)
    print("MPU node overall = ",(MainChainBlkLen/minedBlksCount))
    print("Overall mined blocks count ",minedBlksCount)






doAnalysis(mynetwork)
