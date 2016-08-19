# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 16:05:37 2015

@author: rkd
"""

def readFile(filename):
    with open(filename) as json_data:
        d = json.load(json_data)
        json_data.close()
        return d
