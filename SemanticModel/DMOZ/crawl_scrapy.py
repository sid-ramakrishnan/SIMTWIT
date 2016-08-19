# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 11:10:12 2015

@author: rkd

1.read file
2.take link
3.edit python script
4.run command
"""
import json
from pprint import pprint
import os
    
def readFile(filename):
    with open(filename) as json_data:
        d = json.load(json_data)
        json_data.close()
        return d
        
links=readFile('JSON/Trial/Political_Leaders,_Rulers,_and_Royalty.json')


for l in links:
    try:    
        if len(l['link'][0])<3:
            continue
    except IndexError:
        continue
    with open('/home/rkd/Desktop/tutorial/tutorial/spiders/dmoz_spider.py', 'r') as file:
        data = file.readlines()
        
    filename=l['title']
    filename=filename[0].replace (" ", "_")
    
    opjsonFile='JSON/Trial/'+filename+'.json'
    if os.path.isfile(opjsonFile):
        continue
    
    new_link=(data[8][:28]+l['link'][0]+data[8][-2:]).encode('ascii')
    data[8]=new_link
    with open('/home/rkd/Desktop/tutorial/tutorial/spiders/dmoz_spider.py', 'w') as file:
        file.writelines( data )
    
    print 'scrapy crawl dmoz -o JSON/Trial/'+filename+'.json'
    os.system('scrapy crawl dmoz -o JSON/Trial/'+filename+'.json')