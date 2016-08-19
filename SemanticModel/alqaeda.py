# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 12:49:03 2015

@author: rkd
"""
import matplotlib.pyplot as plt
import networkx as nx
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db=client.Hci_final
G=nx.Graph()

usw=db.user_susp_words.find({"screen_name":"BokoHaramWatch"})

usw=[u['word'] for u in usw]


usw=list(set(usw))
G.add_node('BokoHaramWatch')
labels={}
labels['BokoHaramWatch']='BokoHaramWatch'

for u in usw:
    print u
    labels[u]=u
    G.add_node(u)
    G.add_edge('BokoHaramWatch',u)

pos=nx.spring_layout(G)

nx.draw_networkx_nodes(G,pos,
                       nodelist=['BokoHaramWatch'],
                       node_color='b',
                       node_size=2000,
                   alpha=0.8)  
                   
nx.draw_networkx_nodes(G,pos,
                       nodelist=usw,
                       node_color='r',
                       node_size=1000,
                   alpha=0.8)  
                       
nx.draw_networkx_labels(G,pos,labels,font_size=10)                       

#nx.draw(G)                   
plt.show()