# BlockSim Overview

## Node Generator:

1. Generates node_list and node_network from the CSV(network_model.csv)

2. Generates node_map from each node on node_list

3. Sealer node is chosen randomly from node_map for consensus 'POA' likewise Miner node is chosen randomly for consensus "POW".

        Node List ->  [100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118]

## Transaction Generator:

1. Generate random transaction size and gas using Gaussian Distribution

2. For broadcasting the transaction, node is choose manually i.e 100

3. Assigning task to the node (Appending Transaction)

## Monitor:

In every 50ms the log of message_count_logger ,pending_transaction_logger and unique_block_logger are recorded.
   

## Block Creation:
Block Creation Method:
1.  For each transaction, add the gas of the transaction to the current gas
2.  If the current gas is less than block_gas_limit, add more transaction or else hold the transaction and create a new block.
3.  For new block, store its hash as previous hash, add that block to know list and broadcast it to the other nodes.

Interrupt after receiving block from other nodes:
- If a new block is received, the mining process will be interrupted. After interrupt,
check if the previous block hash of the node matches the previous hash of the block

Hash Generation:
1. For hash key, Python’s hashlib md5 is used
2. The hash is generated from the list of string of transaction id

## Broadcaster:
1. The broadcaster broadcasts the transaction and block to all other nodes.
2. Broadcasting time delay is defined using Gaussian time delay

      	stat_random = random.gauss(delay, 9)
  
  	where,
  
		- delay 	: latency of node_network	(Mean Deviation)
 		- 9		: manually given 	        (Standard Deviation)

## Receiver:
   				
1. Receive the transactions or blocks broadcasted by other nodes. Check if the transaction was already received by the node; checking if the id of data is present in the known_list.
2. If it was previously received, then it was already broadcasted. So no need to broadcast.
3. Else, broadcast the data to other nodes.
	
    	Arguments:
		- data		: It could be a block or a transaction.
		- type		: Representation of data. 1 for block, 0 for transaction
		- sent_by	: Sender of the message


## Logs Generated:
-	The logs generated are described below:
        
		blockchain.csv 			: All the info of node generation, transaction receive, transaction broadcast, block creation, block broadcast
        network_stability_time.csv	: Calculation of block creation time | Block creation time is calcualted as (curr_time – block_start_time) * 10
        block_stability_msg.csv		: Time log of the block created and block received
        pending_transactions.csv	: No of pending transaction on the time frame
       
