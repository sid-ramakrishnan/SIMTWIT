# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 21:48:15 2015

@author: shravan
"""

import csv
import numpy 
from collections import Counter

def KNN(k , knownmat, unknownmat, knownresult):
    rows = len(unknownmat)
    unknownresult = [0] * len(unknownmat)
    distmat = [[0 for x in range(rows)] for x in range(rows)]
    for i in range(rows):
        internalresult = [0] * k
        for j in range(rows):
            #if i==j:
             #   distmat[i][j] = numpy.inf    # Assume distance for one node to itself is infinite
              #  continue
            #print numpy.array(unknownmat[i]),numpy.array(unknownmat[j])
            
            randi=[x-y for x,y in zip(unknownmat[i],knownmat[j])]
            distmat[i][j]=numpy.linalg.norm(numpy.array(randi))
            #distmat[i][j] = numpy.linalg.norm((numpy.array(unknownmat[i]) - numpy.array(knownmat[j])))
        temp=[d for d in distmat[i]]
        temp.sort()
        for j in range(k):

            internalresult[j] = knownresult[distmat[i].index(temp[j])]
        unknownresult[i] = Counter(internalresult).most_common(1)[0][0]
    return unknownresult
    
    
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
answers = KNN(1,dataalone,datatest,answersalone)
