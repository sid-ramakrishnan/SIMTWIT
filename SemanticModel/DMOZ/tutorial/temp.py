import twitter
from pymongo import MongoClient
from nltk.corpus import stopwords
import re
import tweepy

import os.path
client = MongoClient('localhost', 27017)
db=client.MinorProject

def getTwepyApi(api):
    auth = tweepy.OAuthHandler(api.__dict__['_consumer_key'],api.__dict__['_consumer_secret'])
    auth.set_access_token(api.__dict__['_access_token_key'], api.__dict__['_access_token_secret'])
    twepyapi = tweepy.API(auth)
    return twepyapi

def getStatuses(handle):
    page=1
    timeline=[]
    size=0
    global api
    while size<100:     
        
        twepyapi=getTwepyApi(api)
        statuses = twepyapi.user_timeline(screen_name=handle,page=page)
        
        if statuses:
            size=size+len(statuses)
            timeline.extend(statuses)
        else:
            # All done
            break
        page +=1  
    
    return timeline


def processText(text):
    text=text.lower()
    stop = stopwords.words('english')
    stop.extend(['rt'])
    a= [i for i in text.split() if i not in stop and "@" not in i]
    a=[re.sub(r'http?:\/\/.*[\r\n]*', '', i, flags=re.MULTILINE) for i in a]
    a= [re.sub('[^A-Za-z0-9]+', '', i) for i in a]
    a= [i for i in a if len(i)>1 and i not in stop]
    return " ".join(a)
    
def insert(status):
    #text=processText(status["text"])    
    try :
        location=status["user"]["location"]
    except KeyError:
        location = ''
        
    try :
        description=status["user"]["description"]
    except KeyError:
        description = ''
    try:
        frc=status["user"]["friends_count"]
    except KeyError:
        frc=''
    try:
        foc=status["user"]["followers_count"]
    except KeyError:
        foc=''
    entry={"user":{
            "screen_name":status["user"]["screen_name"],
            "location":location,
            "description":description,
            "friends_count":frc,
            "followers_count":foc
            },
            "text":status["text"]    
    }
    print entry
    db.real_user_tweets.insert(entry)
    return

def tweepyInsert(status):
    try :
        location=status.user.location
    except KeyError:
        location = ''
        
    try :
        description=status.user.description
    except KeyError:
        description = ''
    try:
        frc=status.user.friends_count
    except KeyError:
        frc=''
    try:
        foc=status.user.followers_count
    except KeyError:
        foc=''
    entry={"user":{
            "screen_name":status.user.screen_name,
            "location":location,
            "description":description,
            "friends_count":frc,
            "followers_count":foc
            },
            "text":status.text    
    }
    print entry
    db.real_user_tweets.insert(entry)
    return
    
api = twitter.Api(consumer_key='uZ2zywhtZo5RqEmmnJe9cLfQB',
                      consumer_secret='iOJka2mZQDOPFaLl5gOFQbsuvAm60gyu2DIqO2cyG6o4GXcyP0',
                      access_token_key='2922548846-sNsn1QXIvWsXi99dDLpMZrjW3nKVzwjrjbN6DMH',
                      access_token_secret='KnLhU8yEuAn2eMn2qabtDER7ArHdwoItFaO8O5tRhZamM')
'''                      
i=api.GetSearch("isis",count=100)
[insert(k.AsDict()) for k in i]

m=api.GetSearch("modi",count=100)
[insert(k.AsDict()) for k in m]

q=api.GetSearch("vhp",count=100)
[insert(k.AsDict()) for k in q]

m=api.GetSearch("violence",count=100)
[insert(k.AsDict()) for k in m]

a=api.GetSearch("#CWC15",count=100)
[insert(k.AsDict()) for k in a]

a=api.GetSearch("#IndiawithPakistan",count=100)
[insert(k.AsDict()) for k in a]
'''
#z=getStatuses('Shravan_Karthik')
#[tweepyInsert(a) for a in z]

#[tweepyInsert(a) for a in getStatuses('DrGarekar')]

#[tweepyInsert(a) for a in getStatuses('deepakshenoy')]

#[tweepyInsert(a) for a in getStatuses('Sid_Pee')]

#[tweepyInsert(a) for a in getStatuses('spazkapur')]

#[tweepyInsert(a) for a in getStatuses('medhanarmada')]

#tweets=db.real_user_tweets.find()

'''
donelist=[]
path='/home/rkd/Desktop/tutorial/front_end.txt'
for t in tweets:
    if t['user']['screen_name'] in donelist:
        continue
    else:
        random=db.real_user_tweets.find({'user.screen_name':t['user']['screen_name']})
        donelist.extend([t['user']['screen_name']])
        with open(path, 'a') as the_file:
            the_file.write('%%\n')
            the_file.write(t['user']['screen_name']+'\n')
           
        for bijli in random:
            with open(path, 'a') as the_file:
                the_file.write(bijli['text']+'\n')
'''
path='/home/rkd/Desktop/tutorial/clean_front_end.txt'

tweets=db.real_clean_tweets.find()
for t in tweets:
    with open(path, 'a') as the_file:
        the_file.write('%%\n')
        the_file.write(t['screen_name']+'\n')
        for a in t['feature_list']:
            with open(path, 'a') as the_file:
                the_file.write(a+'\n')
        