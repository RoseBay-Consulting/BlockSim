import logging
from logging import FileHandler
import time
import datetime
import os
def creater_logger():
    now = datetime.datetime.now()
    today = now.strftime("%Y-%m-%d")
    time_now = now.strftime("%H_%M_%S")
    loggerPath = os.path.join(os.getcwd(),'logs')
    folderpath = os.path.join(os.getcwd(), 'logs/%s'%today)
    fullpath = os.path.join(folderpath,time_now)

    if os.path.exists(folderpath):
        print(True)
        os.mkdir(fullpath)
    else:
        if os.path.exists(loggerPath) == False:
            os.mkdir(loggerPath)
        os.mkdir(folderpath)
        os.mkdir(fullpath)

    PENDING_TRANSACTION = '%s/pending_transactions.csv'%fullpath
    UNIQUE_BLOCKS='%s/unique_blocks.csv'%fullpath
    BLOCK_CREATION='%s/network_stability_time.csv'%fullpath
    MESSAGE_COUNT= '%s/message_count.csv'%fullpath
    logger= '%s/blockchain.csv'%fullpath
    block_stability='%s/block_stability_msg.csv'%fullpath

    message_count_logger=logging.getLogger("blockchain.MESSAGE_COUNT")
    message_count_logger.setLevel(logging.INFO)
    messaging_logger_file_handler = FileHandler(MESSAGE_COUNT)
    messaging_logger_file_handler.setLevel(logging.INFO)
    message_count_logger.addHandler(messaging_logger_file_handler)

    block_creation_logger=logging.getLogger("blockchain.BLOCK_CREATION")
    block_creation_logger.setLevel(logging.INFO)
    block_logger_file_handler = FileHandler(BLOCK_CREATION)
    block_logger_file_handler.setLevel(logging.INFO)
    block_creation_logger.addHandler(block_logger_file_handler)

    unique_block_logger=logging.getLogger("blockchain.UNIQUE_BLOCKS")
    unique_block_logger.setLevel(logging.INFO)
    unique_block_logger_file_handler = FileHandler(UNIQUE_BLOCKS)
    unique_block_logger_file_handler.setLevel(logging.INFO)
    unique_block_logger.addHandler(unique_block_logger_file_handler)

    pending_transaction_logger=logging.getLogger("blockchain.PENDING_TRANSACTION")
    pending_transaction_logger.setLevel(logging.INFO)
    pending_transaction_logger_file_handler = FileHandler(PENDING_TRANSACTION)
    pending_transaction_logger_file_handler.setLevel(logging.INFO)
    pending_transaction_logger.addHandler(pending_transaction_logger_file_handler)

    root_logger=logging.getLogger("blockchain.logger")
    root_logger.setLevel(logging.DEBUG)
    root_logger_file_handler = FileHandler(logger)
    root_logger_file_handler.setLevel(logging.DEBUG)
    root_logger.addHandler(root_logger_file_handler)

    block_stability_logger=logging.getLogger("blockchain.block_stability")
    block_stability_logger.setLevel(logging.INFO)
    block_stability_logger_file_handler = FileHandler(block_stability)
    block_stability_logger_file_handler.setLevel(logging.INFO)
    block_stability_logger.addHandler(block_stability_logger_file_handler)

    message_count_logger.info("Time,message_count")
    block_creation_logger.info("Stability time")
    pending_transaction_logger.info("Time, pending_transaction")
    unique_block_logger.info("Time,unique_blocks")
    block_stability_logger.info("Time,Node,Block")



    return message_count_logger,block_creation_logger,unique_block_logger,pending_transaction_logger,root_logger,block_stability_logger
