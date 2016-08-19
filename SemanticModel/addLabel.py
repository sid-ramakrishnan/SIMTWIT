# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 19:24:07 2015

@author: rkd
"""

from __future__ import division
from pymongo import MongoClient
import json
from os import listdir
from os.path import isfile, join
from alchemyapi import AlchemyAPI
from fuzzywuzzy import fuzz
import re
from nltk.corpus import stopwords
import operator
import csv

client = MongoClient('localhost', 27017)
db=client.MinorProject

def buildTaxonomy(filename):
    with open(filename) as json_data:
        entries = json.load(json_data)
        json_data.close()
    
    for e in entries:
        try:
            print e['link'][0]
            hlist=str.split(e['link'][0].encode('ascii'),'/')
            hlist=[h.lower() for h in hlist if len(h)>0 and '%' not in h]
        except IndexError:
            continue
    
        #mongo: keyword,[[parents,root_parent]....]
    
        print hlist
        for i in range(len(hlist)):
            try :
                subject_num_mapping[hlist[i]]
                continue
            except KeyError:
                print 'regular entry'
            mongoentry=db.hierarchy.find_one({'keyword':hlist[i]})
            if i==0:
                if mongoentry is None:
                    mongoentry={
                    'keyword':hlist[i],
                    'pr_list':[]
                    }
               
                    db.hierarchy.insert(mongoentry)
                else:
                    continue
            
            elif mongoentry is None:
               mongoentry={
                    'keyword':hlist[i],
                    'pr_list':[[hlist[      0],hlist[i-1]]]
                }
               
               db.hierarchy.insert(mongoentry)
                
            else:
               
               a=mongoentry['pr_list']
               a.append([hlist[0],hlist[i-1]])
               #a=list(set(a))
               db.hierarchy.update(
                { 'keyword':hlist[i] },
                {
                  '$set': {
                    'pr_list': a
                  }
                },upsert=False)
                
        


def removeStopWords(sentence):
    #removing all special characters
    sentence=' '.join(re.sub('[^A-Za-z0-9]+', '', e) for e in sentence.split())

    sentence=sentence.lower()
    stop = stopwords.words('english')
    a= [i for i in sentence.split() if i not in stop]
    return " ".join(a)

def checkMatch(word ):
    print word
    tokens=str.split(word," ")
    tobereturned=[]
    hierentries=db.hierarchy.find()
    #scoreList={}
    #{'word':'score'}
    maximum=0
    for t in tokens:
        for h in hierentries:
            score=2*fuzz.partial_ratio(h['keyword'],t)+fuzz.ratio(h['keyword'],t)
            if maximum<score:
                maximum=score
            if score>240:
                tobereturned.extend([{'keyword':h['keyword'],'pr_list':h['pr_list'],'query':word,'score':score}])
                #print h['keyword']
                #scoreList[h['keyword']]=score
    
    for tbr in tobereturned:
        tbr['score']=tbr['score']/maximum
        
    return tobereturned


def label(text):
    alchHierarchy=alchemyapi.taxonomy('text',text)
    try:
        topic=alchHierarchy['taxonomy']
    except KeyError:
        return []
    tobereturned=[]
    for t in topic:
        alchemyTopics=str.split(t['label'].encode('ascii'),'/')
        alchemyTopics=[removeStopWords(at) for at in alchemyTopics]
        
        if len(alchemyTopics)>=3:
            alchemyTopics=[alchemyTopics[0],alchemyTopics[1],alchemyTopics[2]]
        
        for at in alchemyTopics:       
            tobereturned.extend(checkMatch(at))
        
    return tobereturned

def processLabels(labels):
    global num_subject_mapping
    print labels
    matrix=[0] * len(num_subject_mapping)
    denominator=0
    for l in labels:
        for entry in l['pr_list']:
            try:
                print entry,subject_num_mapping[entry[0]]
                matrix[subject_num_mapping[entry[0]]-1]+=l['score']
                denominator+=1
            except:
                continue
    for e in matrix:
        if denominator is not 0:
            e=round(e/denominator,2)
        
    return matrix
    
'''
mypath='/home/rkd/Desktop/tutorial/JSON'    

onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) if '~' not in f]

for f in onlyfiles:
    print f
    q=buildTaxonomy('JSON/'+f)
'''
alchemyapi = AlchemyAPI()

num_subject_mapping={
    1:'arts',2:'business',3:'computers',4:'games',5:'health',6:'home',
    7:'news',8:'recreation',9:'reference',10:'regional',11:'science',12:'shopping',
    13:'society',14:'sports',15:'world'}
    
subject_num_mapping=dict ( (v,k) for k, v in num_subject_mapping.items())
#text = 'Lenovo Yoga Tab future tablets CEO Yang Yuanqing'
#a=label(text)
#b=processLabels(a)

a=label('office equipment')
b=processLabels(a)
'''
#old dataset
sample_tweets=db.sample_tweets.find()
features=list(num_subject_mapping.values())
features=[['username']+features]
for st in sample_tweets:
    for t in st['tweets']:
        matrix=[0] * (len(num_subject_mapping)+1)
        a=label(t)
        b=processLabels(a)
        #matrix=[x+y for x,y in zip(matrix,b)]
        matrix=[st['username']]+b
        features.append(matrix)
    
with open('sample_features.csv', 'wb') as fp:
    a = csv.writer(fp, delimiter=',')
    a.writerows(features)
'''
#real dataset
'''
clean_tweets=db.real_clean_tweets.find()
features=list(num_subject_mapping.values())
features=[['username']+features]
for ct in clean_tweets:
    for t in ct['feature_list']:
        matrix=[0] * (len(num_subject_mapping)+1)
        a=label(t)
        b=processLabels(a)
        b=[round(q,2) for q in b]
        #matrix=[x+y for x,y in zip(matrix,b)]
        matrix=[ct['screen_name']]+b
        features.append(matrix)
    
with open('real_features.csv', 'wb') as fp:
    a = csv.writer(fp, delimiter=',')
    a.writerows(features)
'''