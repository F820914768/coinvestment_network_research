# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 04:33:27 2020

@author: 82091
"""

import os
import random
from multiprocessing import Process


import pandas as pd
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from utils import save_page, logging

from tqdm import tqdm


N = 6
START_URL = 'https://finance.yahoo.com/mutualfunds'
HEADERS = ['"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"']
PATH = './co_investment/'
df_ip = pd.read_csv('./ip_address/ip.csv', header = None)

def open_browser():
    
    choice_ip = random.choice(df_ip.index)
    proxy_ip = "--proxy-server={}:{}".format(df_ip[0][choice_ip], df_ip[1][choice_ip])

    print('using proxy_ip', proxy_ip)

    options = ChromeOptions()
    options.add_argument(HEADERS[0])
    options.add_argument(proxy_ip)
    browser = webdriver.Chrome(options = options)
    
    return browser


df_top_funds = pd.read_csv('top_mutural_funds.csv')


files = os.listdir(PATH)
files = set([file.split('.')[0] for file in files if 'html' in file])
begin = 0 # len(files)
end = len(df_top_funds.id)

def crawl(ids):
    browser = open_browser()
    for i in tqdm(ids):
        fund_id = df_top_funds.id[i]
        if fund_id in files:
            continue
        print(i, fund_id)
        
        url = 'https://finance.yahoo.com/quote/{0}/holdings?p={0}'.format(fund_id)
        try:
            browser.get(url)
        except Exception as e:
            print(e)
            browser.quit()
            browser = open_browser()
            browser.get(url)
        while "无法访问" in browser.page_source or '未连接' in browser.page_source or '该网页无法正常运作' in browser.page_source:
            try:
                browser.quit()
                browser = open_browser()
                browser.get(url)
                e = 0
            except Exception as e:
                print(e)
                browser.quit()
                browser = open_browser()
                browser.get(url)
                
            
        #time.sleep(30+random.randint(0,10))
        html = browser.page_source.encode('utf-8')
        browser.execute_script("window.scrollTo(500,2000)")
        #time.sleep(10+random.randint(0,10))
        
        filename = PATH + fund_id + '.html'
        save_page(html, filename)
        logging(PATH, filename, '200')
        #time.sleep(10+random.randint(0,10))
        
        
if __name__ == '__main__':
    delta = (end - begin) // N
    processes = []
    for i in range(N):
        p = Process(target = crawl, 
                    args = (range(begin+delta*i, begin+delta*(i+1)),))
        processes.append(p)
    for process in processes:
        process.start()
    
    for process in processes:
        process.join()
    
    
    
    