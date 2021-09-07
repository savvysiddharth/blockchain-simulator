import random
import time

import numpy as np

from code.blk import Transactions, Block, Blockchain


class node(object):
    # block 8 transactions
    simu_t = time.time()
    List_of_nodes = []
    genesis_Block = Block([])
    globalchain = Blockchain(genesis_Block)

    def __init__(self, ID, type, env):
        self.ID = ID  # N0 ,N1 , ...
        self.type = type  # slow , fast
        self.unspent_transactions = []
        self.node_connections = []
        self.balance = 100
        self.last_trxn_time = self.simu_t  # when this node generated the last transaction

        self.transaction_list = []  # stores list of transactions it gets frm broadcast
        self.blk_list = [self.genesis_Block.index]

        self.last_blk_seen = self.genesis_Block
        self.last_blk_time = self.genesis_Block.time

        self.chain = [self.genesis_Block]  # from Blockchain to sync with
        self.node_chain = self.globalchain

    def node_connect_func(self, b):
        print("%s connecting to %s" % (self,b))
        if not b in self.node_connections:
            self.node_connections.append(b)
            if not self in b.node_connections:
                b.node_connections.appen(self)

    def transaction_generation(self):
        node_y = self.ID
        # randomly select a connected node
        for nodes in self.node_connections:
            if random.randint(0, 1):
                node_y = nodes
                break
        node_x = self.ID
        if self.balance > 0:
            C = random.randint(1, self.balance)
            self.balance = self.balance - C

            # node_y.balance =

            # transaction generate b/w node_x , node_y
            transxn = Transactions(node_x, node_y, C)
            print("%r" % transxn)
            self.unspent_transactions.append(transxn)
            self.last_trxn_time = time.time()
            gen_time = transxn.gen_time

            self.transaction_broadcast(transxn, gen_time)

        return

    def transaction_broadcast(self, txn, txn_time):
        for node in self.node_connections:
            if txn.trxnid in self.transaction_list:
                return
            else:
                node.transaction_list.append(txn.trxnid)
                node.unspent_transactions.append(txn)
                new_trxn_time = txn_time + self.latency(node, "transaction")
                node.transaction_broadcast(txn, new_trxn_time)
                return

    def latency(self, b, msg_type):
        Pij = np.random.uniform(10, 500)  # in ms as per question
        if self.type == 'fast' and b.type == 'fast':
            Cij = 100 * pow(10, 3)  # in ms
        else:
            Cij = 5 * pow(10, 3)

        if msg_type == "transaction":
            m = 0
        elif msg_type == "block":
            m = 8 * (10 ** 6)
        else:
            m = 0

        mean = 96 * pow(10, 3) / Cij
        Dij = np.random.exponential((1 / mean), 1)[0]
        tot_delay = Pij + Dij + (m / Cij)
        return tot_delay

    def blk_generate(self):
        if len(self.unspent_transactions) > 0:
            newblk_transactions = self.unspent_transactions[0:8]
            self.unspent_transactions = self.unspent_transactions[8:]

            # block gen
            blk1 = Block(newblk_transactions)
            blk1.prevblk_link = self.last_blk_seen.index
            self.last_blk_time = blk1.time
            self.last_blk_seen = blk1

            # minig starts
            self.blk_list.append(blk1.index)
            self.chain.append(blk1)
            self.node_chain.addBlock(blk1)

            # minig reward
            self.balance = self.balance + 50

            self.blk_broadcast(blk1, blk1.time)
        return

    def blk_broadcast(self, blk, blk_time):
        for ot_nodes in self.node_connections:
            if blk.index not in ot_nodes.blk_list:

                blk_arrivaltime = blk_time + self.latency(ot_nodes, "block")

                ot_nodes.blk_list.append(blk.index)
                # check for clash  ---> forking (fork resolutuion)
                if blk.prevblk_link == ot_nodes.last_blk_seen.prevblk_link and not (
                        ot_nodes.last_blk_seen.index == blk.index):
                    if ot_nodes.last_blk_time < blk_arrivaltime:
                        # append the blk
                        ot_nodes.chain.append(blk)
                        ot_nodes.node_chain.addBlock(blk)

                        ot_nodes.last_blk_seen = blk
                        ot_nodes.last_blk_time = blk_arrivaltime

                        ot_nodes.blk_broadcast(blk, blk_arrivaltime)

                    else:
                        ot_nodes.node_chain = ot_nodes.node_chain[0:len(ot_nodes.node_chain) - 1]
                        ot_nodes.node_chain.addBlock(blk)
                        ot_nodes.chain.append(blk)

                        ot_nodes.last_blk_seen = blk
                        ot_nodes.last_blk_time = blk_arrivaltime

                        ot_nodes.blk_broadcast(blk, blk_arrivaltime)
        return
