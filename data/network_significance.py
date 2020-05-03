# -*- coding: utf-8 -*-

from tqdm import tqdm

import networkx as nx
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt



g = nx.read_gml('co-investment_network.gml')
nx.density(g)

random_density = np.zeros(100)
for i in tqdm(range(100)):
    g_random = nx.random_graphs.erdos_renyi_graph(len(g.nodes()), len(g.edges()))
    random_density[i] += nx.density(g_random)
    
