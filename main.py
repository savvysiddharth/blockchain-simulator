import numpy as np
import simpy
import sys
import constants
from code.simulation import Simulation
from nodes import node


if len(sys.argv) - 1 < 4:
    print("Please enter 4 arguments to start simulation !!")
else:
    N = constants.TotalNodes  # no.of nodes
    Z = constants.Z  # percent of slow nodes
    Ttx_mean = constants.Ttx  # mean of inter arrival b/w transactions  part -3
    Tk = int(sys.argv[4])  # mean for random var Tk part 7

    env = simpy.Environment

    # initialising nodes
    List_of_nodes = []  # N0 , N1, N2 , N3 , ......
    for i in range(N):
        if i < int(N * float(Z / 100)):
            n = node('N%d' % i, 'slow', env)
        else:
            n = node('N%d' % i, 'fast', env)
        List_of_nodes.append(n)

    node.List_of_nodes = List_of_nodes

    # random walk on uniform distribution of node graph
    # connected graph of nodes







    #simulation
    for node in List_of_nodes:
        sim_object = Simulation(node)
        sim_object.start_simulation()

    env.run(until=100)












