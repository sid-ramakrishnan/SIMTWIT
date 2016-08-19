# -*- coding: utf-8 -*-
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db=client.MinorProject

def processUser(userDict):
    return {'id':userDict['id'],
            'location':userDict['location'],
            'statuses_count':userDict['statuses_count'],
            'friends_count':userDict['friends_count'],
            'name':userDict['name'],
            'screen_name':userDict['screen_name'],
            'description':userDict['description'],
            'followers_count':userDict['followers_count']
        }

entries=db.tweets.find()

for e in entries:
    u1=e['py/state']['_json']['user']
    
    if db.users.find_one({'screen_name':u1['screen_name']}) is None:
        db.users.insert(processUser(u1))
    screen_name=[u1['screen_name']]
    text= e['py/state']['_json']['text']
    retweet_count= e['py/state']['retweet_count']
    favorite_count= e['py/state']['favorite_count']
        
    try:
        url=e['py/state']['_json']['entities']['urls'][0]['expanded_url']
    except IndexError:
        url=''
    try:
        u2=e['py/state']['retweeted_status']['py/state']['_json']['user']
        screen_name.extend([u2['screen_name']])
        if db.users.find_one({'screen_name':u2['screen_name']}) is None:
            db.users.insert(processUser(u2))
    except KeyError:
        print 'no retweets for this entry'        

    new_tweet_entry={
        'screen_name':screen_name,
        'text':text,
        'retweet_count':retweet_count,
        'favorite_count':favorite_count,
        'urls':url
    }

    db.clean_tweets.insert(new_tweet_entry)
    