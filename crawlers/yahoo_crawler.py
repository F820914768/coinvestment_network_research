import os
import time
import re
import random

from selenium import webdriver
from selenium.webdriver import ChromeOptions
from utils import save_page, logging


START_URL = 'https://finance.yahoo.com/mutualfunds'
HEADERS = ['"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"']


options = ChromeOptions()
options.add_argument(HEADERS[0])

browser = webdriver.Chrome(options = options)
i = 0


if __name__ == "__main__":
    
    for i in range(40):
        if i == 0:
            current_url = START_URL
        else:
            current_url = 'https://finance.yahoo.com/screener/predefined/top_mutual_funds?offset={0}&count=25'.format(str(25*i))
        
        try:
            browser.get(current_url)
        except Exception as e:
            print(e)
            browser = webdriver.Chrome(options = options)
            browser.get(current_url)
                
        print('visit' + '->' +current_url)
        time.sleep(20+random.randint(0,20))
        browser.execute_script("window.scrollTo(0,2000)")
        time.sleep(random.randint(0,10))
        content = browser.page_source
        
        while "Fw(600)" not in content:
            print('page wrong refresh')
            print('condition one:', "We’re sorry, we weren’t able to find any data" in content)
            print('condition two:', content or "Fw(600)" not in content)
            print('-'*40)
            browser.refresh()
            time.sleep(20+random.randint(0,10))
            content = browser.page_source
            
            
        html = content.encode('utf-8')
        filename = './top_funds/' + current_url.split('/')[-1] + '.html'
        filename = re.sub(r'[?&]', '', filename)
        
        save_page(html, filename)
        logging('./top_funds', current_url, '200')
        print('-'*40)