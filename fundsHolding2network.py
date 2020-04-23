# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 01:16:01 2020

@author: 82091
"""

import re
import os
import pandas as pd
from lxml.etree import HTML
from tqdm import tqdm



path = './crawlers/co_investment/'
filenames = os.listdir(path)
filenames = [filename for filename in filenames if '.html' in filename]
print('there are {} html files'.format(str(len(filenames))))
print('For example:', filenames[:10])



if __name__ == "__main__":

    output = open('./data/funds_holding.csv', 'w', encoding='utf-8')
    output.write('abbrivate_funds,funds_title,stock_title,stock_href,abbrivate_stock,holding\n')

    error_log = open('./log/holding2network.log', 'w')

    for i in tqdm(range(len(filenames))):
        filename = filenames[i]
        filepath = path + filename
        htmlfile = open(filepath, 'rb')
        html = htmlfile.read().decode('utf-8')
        html = HTML(html)

        xpath_title = '//*[@id="quote-header-info"]/div[2]/div[1]/div[1]/h1/text()'

        abbrivate = filename.split('.')[0]; print(abbrivate) 
        try:
            funds_title = html.xpath(xpath_title)[0]
        except IndexError:
            error_log.write(abbrivate)
            error_log.write('\n')
            continue
        
        xpath_number_holding = '//*[@id="Col1-0-Holdings-Proxy"]/section/div[4]/div/h3/span/text()'
        num_holding = int(re.findall(r'Top (\d+) Holding', html.xpath(xpath_number_holding)[0])[0])
        for i in range(num_holding):
            xpath_stock_title = '//*[@id="Col1-0-Holdings-Proxy"]/section/div[4]/table/tbody/tr[{}]/td[1]/text()'.format(str(i+1))                
            xpath_stock_href = '//*[@id="Col1-0-Holdings-Proxy"]/section/div[4]/table/tbody/tr[{}]/td[2]/a/@href'.format(str(i+1))  
            xpath_holding = '//*[@id="Col1-0-Holdings-Proxy"]/section/div[4]/table/tbody/tr[{}]/td[3]/text()'.format(str(i+1))

            stock_title = html.xpath(xpath_stock_title)[0]
            holding = html.xpath(xpath_holding)[0]
            try:
                href = html.xpath(xpath_stock_href)[0]
                abbrivate_stock = href.split('=')[-1]
            except IndexError:
                href, abbrivate_stock = '', ''
            
            line = ','.join([abbrivate, funds_title, stock_title, href, abbrivate_stock, holding])
            output.write(line)
            output.write('\n')
        htmlfile.close()
    output.close()
    error_log.close()


