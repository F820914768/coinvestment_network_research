import os
from lxml import etree
import pandas as pd

path = './funds_1/'
files = os.listdir(path)
files = [file for file in files if 'html' in file]


output = []

if __name__ == '__main__':
    output = []
    for filename in files:
        html = open(path+filename, 'rb').read().decode('utf-8')
        html = etree.HTML(html)
        
        rule_id = '//a[@class="Fw(600)"]//text()'
        rule_title = '//a[@class="Fw(600)"]//@title'
        rule_href = '//a[@class="Fw(600)"]//@href'
        rule_price = '//*[@id="scr-res-table"]/div[1]/table/tbody//tr/td[6]//text()'
        
        html_id = html.xpath(rule_id)
        html_title = html.xpath(rule_title)
        html_href = html.xpath(rule_href)
        html_price = html.xpath(rule_price)
        
        l = list(zip(*(html_id, html_title, 
                       html_href, html_price)))
        output.extend(l)
    
    df = pd.DataFrame(output,
                      columns = ['id', 'title', 'href', 'price_50_average'])
    df.to_csv('top_mutural_funds.csv')
        















