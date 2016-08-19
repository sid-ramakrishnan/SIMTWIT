# -*- coding: utf-8 -*-
import json
import pprint
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db=client.MinorProject

json_file='twitter_payload.json'

with open(json_file) as f:
    content = f.readlines()


tweets=content[0].replace("\\","")
tweets=tweets.replace("<a href=","<a href=\\")
tweets=tweets.replace("\" rel=","\\\" rel=\\")
tweets=tweets.replace("\">","\\\">")
globalcount=3

i=1
count=1
tweets=tweets[count+1:]
print 't',tweets[0:10]
while len(tweets)!=0:
    while i!=0:
        if tweets[count]=='{':
            i+=1
        
        elif tweets[count]=='}':
            i-=1
        
        count+=1    
        globalcount+=1
        
    z=tweets[0:count]

    tweets=tweets[count+2:]
    count=1
    i=1
    
    #print z
    while 1:
        try:
            data=json.loads(z)
            break    
        except ValueError as v:
            print v.message
            colno=v.message[v.message.find("char")+5:-1]
            colno=long(colno)-1
            z = z[:colno] + z[(colno+1):]
        
    db.tweets.insert(data)
    db.minor_project_log.insert({"last_column":globalcount})
