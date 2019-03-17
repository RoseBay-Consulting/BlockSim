import random
import time
import simpy
import logging
import copy
import json
import numpy as np
import pandas as pd
from transactions import Transaction
from blocks import Block
from network_state_graph import network_creator, csv_loader
from monitor import creater_logger

# Time Frame= 1:10ms
MINING_TIME = 2
BLOCKSIZE = 5
txpool_SIZE = 10
BLOCKTIME = 20
curr = time.ctime()
MESSAGE_COUNT = 0
max_latency = 5
BLOCKID = 99900
#logger.info("-----------------------------------Start of the new Session at %s-------------------------------"%curr)


class nodes():
    '''
    Properties:
    1. nodeID:      Representing a node

    2. txpool:      A list representing the nodes transaction pool. Its where a new transaction is appended. Acts like a buffer

    3. pendingpool: A list where transaction are stored to form a new block. 
                    Transaction are poped from txpool and are appended to this pool.

    4. block_list:  List of blocks of the node

    5. known_blocks: List of known blocks. It is used for preventing block broadcast forever. It function
                     is defined below in receiver.

    6. known_tx:    List of known Transaction. It is used for preventing block broadcast forever. It function
                     is defined below in receiver.

    7. prev_hash:   Hash of the recent block formed

    8. mine_process: A pointer representing the mining/validator/consensus process. This variable is used to 
                    handle the interrupt.


    '''

    def __init__(self, nodeID):
        self.nodeID = nodeID
        self.env = env
        self.txpool = []
        self.pendingpool = []
        self.block_gas_limit = config['block_gas_limit']
        self.block_list = []
        self.current_gas = 0
        self.current_size = 0
        self.known_blocks = []
        self.known_tx = []
        self.prev_hash = 0
        self.prev_block = 99900
        #self.res= simpy.Resource(env,capacity=1)
        self.miner_flag = 0
        self.mine_process = env.process(self.miner())
        #print("Node generated with node ID: %d " % self.nodeID)
        logger.debug('%d,%d, generated, node, -' % (env.now, self.nodeID))

    def add_transaction(self, tx):
        '''
        Method for appending a transaction to the node's transaction pool
        '''
        self.txpool.append(tx)
        self.known_tx.append(tx.id)
        self.broadcaster(tx, self.nodeID, 0, 0)
    '''
     type= 0 :transactions
     type= 1 :blocks
    '''

    def receiver(self, data, type, sent_by):
        '''
        Arguments:
        1. data: The data itself. It could be a block or a transaction.
        2. type: Representation of data. 1 for block, 0 for transaction
        3. sent_by: Sender of the message

        Function of the receiver:
        1. Receive the transactions or blocks broadcasted by other nodes. Check if the transaction was 
           already received by the node; checking if the id of data is present in the known_list. 
            1. If it was previously received, then it was already broadcasted. So no need to broadcast.
            2. Else, broadcast the data to other nodes.

        2. Generate interrupt if a new block is received.
        '''

        global MESSAGE_COUNT
        MESSAGE_COUNT -= 1
        # check if the data is transaction(0) and if the transaction is already included in the blockchain
        if type == 0 and (data.id not in self.known_tx):
            self.txpool.append(data)
            # add the transaction to the known list
            self.known_tx.append(data.id)
            #print("%d received transaction %d at %d"%(self.nodeID,data.id,self.env.now))
            logger.debug("%d,%d,received,transaction,%d " %
                         (self.env.now, self.nodeID, data.id))
            # TODO: comment the below broadcast for all connected network
            # self.broadcaster(data,self.nodeID,0,sent_by)

        # check if the data is block(1) and if the block is already included in the blockchain
        elif type == 1 and (data.id not in self.known_blocks):
            # Use a variable intr_data to store the data for interrupt.
            self.intr_data = data
            # add block to the known list
            self.known_blocks.append(data.id)
            # TODO: comment the below broadcast for all connected network
            # self.broadcaster(data,self.nodeID,1,sent_by)
            #print("%d,%d, received, block, %d"%(self.env.now,self.nodeID,data.id))
            logger.debug("%d,%d, received, block, %d" %
                         (self.env.now, self.nodeID, data.id))
            # Interrupt the mining process
            # self.receive_block()
            self.mine_process.interrupt()
        pass

    def broadcaster(self, data, nodeID, type, sent_by):
        # print("broadcasting")
        # yield env.timeout(1)
        global MESSAGE_COUNT
        # Broadcast to neighbour node. For now, broadcast to all.
        #logger.debug('%d , broadcasting, %d'%(self.nodeID,env.now))

        def propagation(delay, each, data, type):
            # TODO: take a gussian time delay
            stat_random = random.gauss(delay, 9)
            if stat_random <= 0:
                stat_random = delay
            yield self.env.timeout(stat_random)
            each.receiver(data, type, nodeID)
        #print("%d, %d, broadcasting, data, %d"%(env.now,self.nodeID,data.id))
        logger.debug("%d, %d, broadcasting, data, %d" %
                     (env.now, self.nodeID, data.id))
        for each in node_map:
            # Dont send to self and to the node which sent the message
            if (each.nodeID != self.nodeID) and (each.nodeID != sent_by):
                # insert delay using nodemap
                latency = node_network.loc[self.nodeID, each.nodeID]
                if latency != 0:
                    MESSAGE_COUNT += 1
                    self.env.process(propagation(latency, each, data, type))
                else:
                    pass
        pass

    def miner(self):
        '''
        Block creation method:
        1. For each transaction, add the gas of the transaction to the current gas.
        2. If the current gas is less than block_gas_limit, add more transaction
        3. Else, hold that transaction and create a new block
        4. For new block, store its hash as previous hash, add that block to know list and broadcast 
            it to the other nodes. 

        Interrupt after receiving block from other nodes:
            If a new block is received, the mining process will be interrupted. After interrupt,
            check if the previous block hash of the node matches the previous hash of the block.
        TODO: 
            What to do if prev hash and block id do not match  
        '''

        while True:
            try:
                yield env.timeout(0)
                if self.miner_flag == 1:
                    yield env.timeout(config["POA"]["mining_time"])
                    if len(self.txpool) != 0:
                        for each_tx in self.txpool:
                            self.current_gas += each_tx.gas
                            self.current_size += each_tx.size
                            #  Checked: done
                            if self.current_gas < self.block_gas_limit:
                                self.pendingpool.append(self.txpool.pop(0))
                            else:
                                break
                    else:
                        pass
                        # could this pass for pending pool be pass by reference ?
                    global BLOCKID
                    BLOCKID += 1
                    self.prev_block += 1
                    block = Block(self.current_size, self.prev_block,
                                  self.pendingpool, self.nodeID, self.prev_hash)
                    self.prev_hash = block.hash
                    print('%d, %d, Created, block, %d,%d' %
                          (env.now, self.nodeID, block.id, block.size))
                    logger.debug('%d, %d, Created, block,%d,%d' %
                                 (env.now, self.nodeID, block.id, block.size))
                    print("hash of block is %s" % block.hash)
                    self.block_list.insert(0, block)
                    block_stability_logger.info("%s,%d,%d,created,%d" % (
                        env.now, self.nodeID, block.id, block.size))
                    network_stability_calc(env, 'c')
                    #print("No of blocks in node %d is %d"%(self.nodeID,len(self.block_list)))
                    logger.info("No of blocks in node %d is %d" %
                                (self.nodeID, len(self.block_list)))
                    self.known_blocks.append(block.id)
                    self.broadcaster(block, self.nodeID, 1, 0)
                    self.current_gas = 0
                    self.current_size = 0
                    self.pendingpool = []
                else:
                    yield env.timeout(0.1)
            except simpy.Interrupt:
                #print("%d,%d, interrupted, block, %d " %(env.now,self.nodeID,self.intr_data.id))
                logger.debug("%d,%d, interrupted, block, %d " %
                             (env.now, self.nodeID, self.intr_data.id))
                # logger.info("testing ...No of blocks in node %d is %d"%(self.nodeID,len(self.block_list)))
                # Verify the block:
                #import ipdb; ipdb.set_trace()
                # check block number
                if self.prev_hash == self.intr_data.prev_hash:
                    #print("Previous hash match")
                    # check the list of transactions
                    block_set = set(self.intr_data.transactions)
                    node_set = set(self.pendingpool)
                    yield env.timeout(config['block_verify_time'])
                    if block_set != node_set:
                        block_extra = block_set-node_set
                        node_extra = node_set-block_set
                        # add item to known tx and transaction pool
                        # Todo : tx id could be repeated in the known tx. Use set for known_tx
                        # print("know tx before extend----> ",self.known_tx)
                        self.known_tx.extend(list(block_extra))
                        # print("know tx after extend----> ",self.known_tx)
                        # move mismatched tx from pendingpool to the txpool
                        self.temp_trans = [
                            each for each in self.pendingpool if each.id in node_extra]
                        self.txpool.extend(self.temp_trans)
                    self.block_list.insert(0, self.intr_data)
                    self.prev_hash = self.intr_data.hash
                    wait = random.randint(0, 45)
                    yield self.env.timeout(wait)
                    block_stability_logger.info("%s,%d,%d,received" % (
                        env.now, self.nodeID, self.intr_data.id))
                    network_stability_calc(env, 'r')
                    #print("No of blocks in node %d is %d"%(self.nodeID,len(self.block_list)))
                    logger.info("No of blocks in node %d is %d" %
                                (self.nodeID, len(self.block_list)))
                    self.pendingpool = []
                    self.intr_data = None
                    self.current_gas = 0
                else:
                    # print("%s,%d,%d,outofsync"%(env.now,self.nodeID,self.intr_data.id))
                    # print(self.prev_hash)
                    # print(self.intr_data.prev_hash)
                    self.prev_hash = self.intr_data.hash
                    block_stability_logger.info("%s,%d,%d,outofsync" % (
                        env.now, self.nodeID, self.intr_data.id))
                    # Simulate node restart by adding the incoming node


def node_generator(env):
    '''
    Generated list of 'n' nodes and network topology with latency using network_creator from 
    network_state_graph based on the parameter NO_NODES
    '''
    global nodelist
    # load from csv; should create a nodelist and node_map
    if config['load_csv'] == 1:
        global node_network
        node_network, nodelist = csv_loader()

    else:
        nodelist = random.sample(
            range(1000, 1000+config['n_nodes']), config['n_nodes'])
        node_network = network_creator(nodelist, config['max_latency'])

    global node_map
    node_map = [nodes(each) for each in nodelist]

    if config['consensus'] == "POW":
        n_sealer = config['POW']['sealer_number']
        # select n nodes randomly
        sealer_nodes = np.random.choice(node_map, n_sealer, replace=False)
        # Change the sealer_flag for those nodes
        for each in sealer_nodes:
            each.sealer_flag = 1
            #print("%d selected as sealer"%each.nodeID)

    elif config['consensus'] == "POA":
        n_sealer = config['POA']['sealer_number']
        global sealer_node
        sealer_node = random.choice(node_map)
        sealer_node.miner_flag = 1
        print("Selected sealer is %d" % sealer_node.nodeID)


def trans_generator(env):
    '''
    1. Generates transaction in a random time derived from Mean Transaction generation time and its 
    Standard Deviation.
    2. Assigns the transaction to a node radomly from the list of transactions.
    '''
    # Use a global ID for transaction
    global txID
    txID = 2300
    while True:
        # Generate random transaction size and gas
        TX_SIZE = random.gauss(config['mean_tx_size'], config['sd_tx_size'])
        TX_GAS = random.gauss(config['mean_tx_gas'], config['sd_tx_gas'])

        txID += 1
        transaction = Transaction(TX_GAS, TX_SIZE, txID)
        # Choose a node randomly from the nodelist
        #node = random.choice(nodelist)
        # choose a node manually
        node = 100
        # select a sealer

        # Assign the task to the node; Find the node object with the nodeID
        for i in node_map:
            if i.nodeID == node:
                #print("%d, %d, Appended, Transaction, %d"%(env.now,i.nodeID,txID))
                logger.debug("%d, %d,Appended, Transaction, %d" %
                             (env.now, i.nodeID, txID))
                i.add_transaction(transaction)
        yield env.timeout(random.gauss(config['mean_tx_generation'], config['sd_tx_generation']))


def monitor(env):
    prev_tx = 2300
    prev_block = 99900
    avg_pending_tx = 0
    while True:
        yield env.timeout(50)
        #print("Current MEssa ges in the system: %d "%MESSAGE_COUNT)
        message_count_logger.info("%d,%d" % (env.now, MESSAGE_COUNT))

        # Transaction per second(Throughput)
        avg_tx = txID-prev_tx
        prev_tx = txID
        # logger.info("%d,%d"%(env.now,avg_tx))

        # tx in pending pool
        average = len(sealer_node.txpool)
        pending_transaction_logger.info("%d,%d" % (env.now, average))

        # Eventual Consistency # Verified
        hash_list = set()
        len_list = set()
        for each in node_map:
            len_list.add(len(each.block_list))
            for block in each.block_list:
                hash_list.add(block.hash)

        unique_block_logger.info("%d,%d" % (env.now, len(hash_list)))


def network_stability_calc(env, msg):

    total = len(nodelist)-1
    if msg == 'c':
        global stb_count, start
        stb_count = 0
        start = env.now
    elif msg == 'r':
        stb_count += 1
        if stb_count >= total:
            time_taken = (env.now - start)*10
            block_creation_logger.info("%s" % (time_taken))
            stb_count = 0
        pass


if __name__ == "__main__":
    #env = simpy.rt.RealtimeEnvironment(factor=0.5)
    with open('config/config.json') as json_data:
        config = json.load(json_data)
    env = simpy.Environment()
    message_count_logger, block_creation_logger, unique_block_logger, pending_transaction_logger, logger, block_stability_logger = creater_logger()
    start_time = time.time()
    node_generator(env)
    env.process(trans_generator(env))
    env.process(monitor(env))
    # env.process(POA(env))
    env.run(until=config['sim_time'])
    elapsed_time = time.time() - start_time
    print("----------------------------------------------------------------------------------------------")
    print("Simulation ended")
    logger.info("Simulation ended")
    print("Total Time taken %d:" % elapsed_time)
    # for each in node_map:
    #     #logger.info("Blocks in node %d " %each.nodeID)
    #     print("Blocks in node %d: " %each.nodeID)
    #     for one in each.block_list:
    #         print("Created by %d"%one.generated_by)
    #         one.view_blocks()
    #         #logger.info(one.view_blocks())
    #     print("----------------------------------------------")
