# -*- coding: utf-8 -*-
import re

import matplotlib.pyplot as plt
import networkx as nx
import pandas_datareader.data as web
import pandas as pd
import numpy as np
import seaborn as sns




df = pd.read_csv('funds_holding.csv')
df = df[['stock_title', 'abbrivate_stock']]


def get_average_price(abbrivate, start='2019-1-1'):
    data = web.DataReader(abbrivate, 'yahoo', start=start)
    return data['Open'].mean()

def get_capital(s):
    if isinstance(s, float):
        return np.nan
    num = s[:-1]
    scale = s[-1]
    if scale == 'B':
        num = float(num)*10**9
    elif scale == 'M':
        num = float(num)*10**6
    else:
        return np.nan
    return num


def get_price(kind='min'):
    
    def _get(x, kind = kind):
        nums = re.findall(r'(\d+\.\d+)', x)
        if not nums:
            return np.nan
        if kind == 'min':
            return float(nums[0])
        elif kind == 'max':
            return float(nums[1])
        elif kind == 'mean':
            return (float(nums[0]) + float(nums[1]))/2
    
    return _get

if __name__ == "__main__":
    g = nx.read_gml('co-investment_network.gml')
    
    stock_detail = pd.read_csv('stock_detail.csv')
    stock_detail['0'] = stock_detail['0'].str.lower()
    stock_rank = pd.read_csv('closeness.csv', header=None)
    stock_rank.columns = ['stock_title', 'closeness']
    
    stock_detail['capital'] = stock_detail['3'].apply(get_capital)
    stock_detail['lower'] = stock_detail['1'].apply(get_price('min'))
    stock_detail['max'] = stock_detail['1'].apply(get_price('max'))
    stock_detail['mean'] = stock_detail['1'].apply(get_price('mean'))
    stock_detail['beta'] = stock_detail['4']
    
    stock = stock_detail[['0', 'lower', 'max',
                          'mean', 'capital', 'beta']].dropna()
    
    
    df = stock_rank.merge(stock, left_on = 'stock_title',
                          right_on = '0')
    
    a
    
    sns.jointplot(x = 'beta', y = 'closeness',
                  data = df, kind = 'reg')
    plt.xlim(0, 2.5)
    plt.plot((1.0,1.0),(0,0.015), 'r')
    plt.savefig('./figure/beta-closeness.png')
    plt.show()
    
    df['log average stock price'] = np.log(df['mean'])
    sns.jointplot(x = 'log average stock price', y = 'closeness',
                  data = df, kind = 'reg')
#    plt.xscale('log')
    plt.savefig('./figure/price-closeness_log.png')
    
    df['log capital'] = np.log(df.capital)
    sns.jointplot(x = 'log capital', y = 'closeness',
                  data = df, kind = 'reg')
#    plt.xscale('log')
    plt.savefig('./figure/capital-closeness_log.png')
    
    

    
    plt.figure(figsize = (100,100))
    df.index = df.stock_title
    val_map = (df['capital']/10**8).to_dict()
    colors = [val_map.get(node, 0.25) for node in g.nodes()]
    
    nx.draw(g, node_size = df['page_rank']*50000,
            c_map=plt.get_cmap('jet'), node_color=colors,
            width=0.2, color = 0.2)
    plt.savefig('fig2.png')
    
    special_node = df[df.page_rank > 0.006]
    special_node.to_csv('./special output/company_lowStock_highPageRank2.csv')
    
    
    special_node = df[df['mean'] > 450]
    special_node.to_csv('./special output/company_highStock_lowPageRank.csv')
    
    
    