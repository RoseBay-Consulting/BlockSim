#import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
import random
# use graphviz

def show_network(data,labels):
    pass

def csv_loader():
    data = pd.read_csv("config/network_model.csv")
    data.set_index('node',inplace=True)
    nodes=data.columns.tolist()
    nodeID=[int(i) for i in nodes]
    network_df = pd.DataFrame(data.values,columns=nodeID,index=nodeID)
    print(network_df)
    graph = nx.from_numpy_matrix(network_df.values)
    #nx.draw(graph)
    #plt.show()
    return network_df,nodeID


def network_creator(nodeID,max_latency):
    '''
    Arguments:
    1. nodeID : List of nodes ID
    2. max_latency: Maximum latency to be asserted in communication between nodes
    For future improvements, make sure to handle an unconnected node.
    '''

    dimension= len(nodeID)
    # Generate a random adjency matrix of size dimension * dimension for lookup table
    np.random.seed(7)
    x=np.random.randint(2, size=(dimension, dimension))
    # Fill diagonal value with 0 for representing 0 latency for self communication.
    np.fill_diagonal(x,0)
    # Generate a graph
    graph = nx.from_numpy_matrix(x)
    # Add latency randomly
    for (u, v) in graph.edges():
        np.random.seed(7)
        graph[u][v]['weight'] = random.randint(1,max_latency) 
    network_df= pd.DataFrame(nx.to_numpy_array(graph),columns=nodeID,index=nodeID)
    print("Printing network")
    network_df.to_csv('20_nodes.csv',index=False)
    # print(network_df)
    # nx.draw(graph)
    #nx.draw(nx.from_numpy_array(network_df.values))
    return network_df