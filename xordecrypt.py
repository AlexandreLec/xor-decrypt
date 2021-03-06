import os
import sys
import operator
import getopt
import argparse
from random import shuffle
import numpy as np
import time
import multiprocessing as mp

start_time = time.time()

# Read the file in hex format (to simplify computation)

def open_file_hex(filename):
    with open(filename, 'rb') as f:
        hexdata = f.read().hex()
    return hexdata.upper()

def write_file(filename, content):
    try:
        with open(filename, 'x', encoding='utf-8') as f:
            f.write(content)
    except FileExistsError:
        ack = input("File "+decrypted_file +
                    " exists, do you want to overwrite it? [y/n]")
        if ack is "y":
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)

def load_dictionnary(lang):
    if lang is "FR":
        with open("dicts/liste_fr.txt") as f:
            dict_fr = [line.rstrip() for line in f]
    else:
        print("Unknow dictionnary, please specify another one")
    dict_fr = np.array(dict_fr)
    np.random.shuffle(dict_fr)
    return dict_fr

def check_decryption(content, dictio):
    words_found = 0
    for word in content.split():
        if word in dictio:
            words_found += 1
        if words_found > 30:
            return True
    return False

def listToString(l):
    str1 = ""
    for element in l:
        str1 += element
    return str1

def analysis(data, key_len, shift):
    values = []
    # shift represent a given char in the key
    i = shift
    while i < len(data):
        values.append(data[i]+data[i+1])
        i = i + key_len*2
    # Compute the frequencies of each cipher char, sort them in desceding order
    res_analysis = {i: values.count(i) for i in values}
    res_analysis = sorted(res_analysis.items(), key=operator.itemgetter(1), reverse=True)
    return [shift, chr(int(res_analysis[1][0], 16)^101)]

def guess_key(data, key_len):
    key =""
    nprocs = mp.cpu_count()
    pool = mp.Pool(processes=nprocs)
    result = pool.starmap(analysis, [(data, key_len, i) for i in range(0, key_len*2,2)])
    for c in result:
        key += c[1]
    return key

def decrypt_xor(data, key):
    i = 0
    plaintxt = ""
    while i < len(data):
        for k in key:
            try:
                plaintxt += chr(int(data[i]+data[i+1], 16)^ord(k))
                i = i + 2
            except IndexError:
                break
    return plaintxt

def try_decrypt_file():
    if encrypted_file is None:
        print("Please specify a file to decrypt")
    elif decrypted_file is None:
        print("Please specify a file to save the decrypted content")
    elif keylen is None:
        print("Please specify the lenght of the key to guess")
    else:
        dict_fr = load_dictionnary("FR")
        data = open_file_hex(encrypted_file)
        key_computed = guess_key(data, keylen)
        print("Key computed : "+key_computed)
        decoded_content = decrypt_xor(data, key_computed)
        print("Checking if output content is French")
        print(check_decryption(decoded_content, dict_fr))
        print("--- %s seconds ---" % (time.time() - start_time))
        write_file(decrypted_file, decoded_content)

def decrypt_file():
    data = open_file_hex(encrypted_file)
    decoded_content = decrypt_xor(data, key_user)
    write_file(decrypted_file, decoded_content)

def usage():
    print("Incorrect usage, please check xor-decrypt --help")

def display_help():
    print("-e : file to decrypt \n-d : file to save the decrypted content \n-l : key's lenght to guess")

def main(argv):
    global encrypted_file
    encrypted_file = None
    global decrypted_file
    decrypted_file = None
    global keylen
    keylen = None
    global key_user
    key_user = None

    try:
        opts, args = getopt.getopt(argv, "he:d:l:k:", ["help", "encrypted=", "decryted=", "keylen=", "key="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            display_help()
            sys.exit()
        elif opt in ("-d", "--decrypted"):
            decrypted_file = arg
        elif opt in ("-e", "--encryted"):
            encrypted_file = arg
        elif opt in ("-l", "--keylen"):
            keylen = int(arg)
        elif opt in ("-k", "--key"):
            key_user = arg
    if key_user is None:
        try_decrypt_file()
    else:
        decrypt_file()

if __name__ == "__main__":
    main(sys.argv[1:])

