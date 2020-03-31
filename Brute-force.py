# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 16:45:16 2020

@author: Dimitri
"""
from itertools import combinations_with_replacement
import time
from xordecrypt import *
from itertools import permutations

start_time = time.time()
dict_fr = load_dictionnary("FR")
content = open_file_hex("tests_files/PA.txt")
decryption = ""

items = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
for p in permutations(items,6):
     val = (''.join(p))
     decryption = decrypt_xor(content,val)
     if check_decryption(decryption, dict_fr):
          print(val)
          break
   
print("--- %s seconds ---" % (time.time() - start_time))