# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 03:38:05 2020

@author: 82091
"""

import pandas as pd
import numba as nb
import networkx as nx
from tqdm import tqdm

import matplotlib.pyplot as plt

df = pd.read_csv('co_investment_network_stock.csv')
df['stock_title1'] = df['stock_title1'].str.lower()
df['stock_title2'] = df['stock_title2'].str.lower()

@nb.jit()
def create_edges_from_table(node1, node2, df):
    '''
    convert a DataFrame table or Numpy.ndarray table into networkx.Graph
    
    input:
    =================
    node1: str
            column index of node1
    node2: str
            column index of node2
    df: DataFrame
            table
            
    output:
    =================
    edges: list[[str, str, float or int]]
    
    '''
    g_dict = {}
    edges = []
    #highest_count = 0
    node1_list, node2_list = df[node1], df[node2]
    for i in tqdm(range(len(df))):
        n1 = node1_list.iloc[i]
        n2 = node2_list.iloc[i]
        if n1 > n2:
            n1, n2= n2, n1
        
        if (n1, n2) not in g_dict:
            g_dict[(n1, n2)] = 0
        g_dict[(n1, n2)] += 1
    
    
    for n1, n2 in g_dict:
        weight = g_dict[(n1, n2)]
        edges.append([n1, n2, weight])
        
    return edges
        


if __name__ == "__main__":
    edges = create_edges_from_table('stock_title1', 'stock_title2', df)
    graph = nx.Graph()
    graph.add_weighted_edges_from(edges)
    nx.write_gml(graph,'co-investment_network.gml')
    
    value_page_rank = nx.pagerank_scipy(graph)
    value_page_rank = pd.Series(value_page_rank)
    value_page_rank.sort_values(ascending=False, inplace=True)
    value_page_rank.to_csv('page_rank_stock_csv')
    
    plt.figure(figsize=(100,100))
    node_size = value_page_rank.copy()
    #node_size[node_size<=0.001256] = 0
    nx.draw(graph, node_size = node_size*80000,
            with_labels=False, width = 0.3, alpha = 0.5)
    plt.savefig('co-investment_network.png')
    
    