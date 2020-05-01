# -*- coding: utf-8 -*-

import networkx as nx
import pandas_datareader.data as web
import pandas as pd
import numpy as np

df = pd.read_csv('funds_holding.csv')
df = df[['stock_title', 'abbrivate_stock']]


def get_average_price(abbrivate, start='2019-1-1'):
    data = web.DataReader(abbrivate, 'yahoo', start=start)
    return data['Open'].mean()


if __name__ == "__main__":
    g = nx.read_gml('co-investment_network.gml')
    
    d = web.DataReader('HII', 'yahoo', start='2019-1-1')