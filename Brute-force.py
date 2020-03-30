# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 16:45:16 2020

@author: Dimitri
"""
from itertools import combinations_with_replacement

for item in combinations_with_replacement('abcdefghijklmnopqrstuvwxyz', 6):
     val = (''.join(item))
     print(val)
