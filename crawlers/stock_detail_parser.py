from lxml.etree import HTML
import pandas as pd
import os
import numpy as np
from tqdm import tqdm

df = pd.read_csv('./data/funds_holding.csv')

def name_coding(s):
    if not isinstance(s, str):
        return None
    
    if 'quote' not in s:
        return None

    return s.replace('?', '').replace('=', '')





if __name__ == "__main__":
    
    d = {}
    output = []
    for i in tqdm(range(len(df))):
        stock_title = df['stock_title'][i]
        
        if stock_title in d:
            continue
        
        href = df['stock_href'][i]
        name_id = name_coding(href)
        if not name_id:
            continue
        
        filename = './stock_detail_page' + name_id + '.html'
        try:
            f = open(filename, 'rb').read().decode('utf-8')
        except Exception as e:
            print(filename, e)
            continue
        html = HTML(f)
        range_xpath = '//*[@id="quote-summary"]/div[1]/table/tbody/tr[6]/td[2]/text()'
        volume_xpath = '//*[@id="quote-summary"]/div[1]/table/tbody/tr[7]/td[2]/span/text()'
        capti_xpath = '//*[@id="quote-summary"]/div[2]/table/tbody/tr[1]/td[2]/span/text()'
        beta_xpath = '//*[@id="quote-summary"]/div[2]/table/tbody/tr[2]/td[2]/span/text()'

        try:
            price_range = html.xpath(range_xpath)[0]
            volume = html.xpath(volume_xpath)[0]
            capital = html.xpath(capti_xpath)[0]
            beta = html.xpath(beta_xpath)[0]
            output.append([stock_title, price_range, volume, capital, beta])
        except IndexError:
            print(filename, 'index error')
        
        d[stock_title] = 0

    output = pd.DataFrame(output)
    output.to_csv('./data/stock_detail.csv')
        


        






