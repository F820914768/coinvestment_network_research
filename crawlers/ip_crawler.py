# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 01:16:01 2020

@author: 82091
"""

import time

from lxml.etree import HTML
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from utils import save_page, logging

from tqdm import tqdm

START_URL = 'https://free-proxy-list.net/'
HEADERS = ['"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"']
PATH = 'ip_address/'

options = ChromeOptions()
options.add_argument(HEADERS[0])

browser = webdriver.Chrome(options = options)

if __name__ == '__main__':
    f = open(PATH+'ip.csv', 'w')
    browser.get(START_URL)
    for i in range(15):
        content = browser.page_source
        html = HTML(content)

        ip_address = html.xpath('//tr//td[1]//text()')[:20]
        port = html.xpath('//tr//td[2]//text()')[:20]
        anonimity = html.xpath('//tr//td[5]//text()')[:20]
        https = html.xpath('//tr//td[@class="hx"]//text()')[:20]
        
        for i in range(len(port)):
            line = ','.join([ip_address[i], port[i], anonimity[i], https[i]])
            f.write(line)
            f.write('\n')
        time.sleep(2)
        button = browser.find_element_by_xpath('//*[@id="proxylisttable_next"]/a')
        button.click()
    f.close()
        