# -*- coding: utf-8 -*-
from pymongo import MongoClient
from nltk.corpus import stopwords
import re

client = MongoClient('localhost', 27017)
db=client.MinorProject

def processTweet(text):
    #text = re.sub(r'^http?:\/\/.*[\r\n]*', '', text, flags=re.MULTILINE)
    text=text.lower()
    stop = stopwords.words('english')
    stop.extend(['rt'])
    a= [i for i in text.split() if i not in stop and "@" not in i]
    a=[re.sub(r'http?:\/\/.*[\r\n]*', '', i, flags=re.MULTILINE) for i in a]
    a= [re.sub('[^A-Za-z0-9]+', '', i) for i in a]
    a= [i for i in a if len(i)>1 and i not in stop]
    return " ".join(a)

'''
#this is for entries received from the json dump file
entries=db.clean_tweets.find()

for e in entries:
    for s in e['screen_name']:
        
        processedTweet=processTweet(e['text'])
        urls=e['urls']
        
        #print s,processedTweet,urls
        
        feature_entry=db.user_tweets.find_one({'screen_name':s})
        print s,feature_entry
        if processedTweet is None:
            processedTweet=[]
            
        if urls is None:
            urls=[]
            
        if feature_entry is None:
            feature_entry={'screen_name':s,
                           'feature_list':[processedTweet],
                           'urls':[urls]
            }
            
            db.user_tweets.insert(feature_entry)
            
        else:
            feature_list=feature_entry['feature_list']
            feature_list.extend([processedTweet])
            urls=feature_entry['urls']
            urls.extend([e['urls']])
            feature_list=list(set(feature_list))
                
            db.user_tweets.update(
                { 'screen_name':s },
                {
                  '$set': {
                    'feature_list': feature_list,
                     'urls':  urls 
                  }
                },upsert=False)
                
final_entries=db.user_tweets.find()
for e in final_entries:
    tobeenteredfl=[]                
    feature_list=e['feature_list']
    for fl in feature_list:
        flentry=fl.split()
        tobeenteredfl.extend(flentry)
    feature_entry={'screen_name':e['screen_name'],
                   'feature_list':tobeenteredfl,
                   'urls':list(set(e['urls']))
        }
            
    db.user_features.insert(feature_entry)
'''
#this is for the tweets pulled real time

real_user_tweets=db.real_user_tweets.find()

for rut in real_user_tweets:
    s=rut['user']['screen_name']          
    rct=db.real_clean_tweets.find_one({"screen_name":s})
    if rct is None:
        tweets=db.real_user_tweets.find({"user.screen_name" : s})
        feature_list=list(set([processTweet(t['text']) for t in tweets]))
        entry={
            'screen_name':s,
            'feature_list':feature_list
        }
        db.real_clean_tweets.insert(entry)