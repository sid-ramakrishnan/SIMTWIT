"""
Created on Mon Mar 23 23:01:21 2015

@author: shravan
"""

import pandas as pd
import numpy as np
import csv as csv
from sklearn.ensemble import RandomForestClassifier

    
csv_file_object = csv.reader(open('/home/shravan/Desktop/testNorm.csv', 'rb'))
data=[]                                                  

for row in csv_file_object:
    data.append(row)
data = np.array(data)

dataalone = data[0::,0:6]
answers = data[0::,6]
dictionary = {"Sports":0,"Politics":1,"Technology":2,"Entertainment":3,"Finance":4,"Health":5}
answersalone = []
for a in answers:
    answersalone.append(dictionary[a])

csv_file_object = csv.reader(open('/home/shravan/Desktop/testsetNorm.csv', 'rb'))
datatest=[]                                                  

for row in csv_file_object:
    datatest.append(row)
datatest = np.array(datatest)

dataalone = [map(float, x) for x in dataalone]
datatest = [map(float, x) for x in datatest]

print 'Training...'
forest = RandomForestClassifier(n_estimators=100)
forest = forest.fit( dataalone, answersalone )

print 'Predicting...'
output = forest.predict(datatest).astype(int)

