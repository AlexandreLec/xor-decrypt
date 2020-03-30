import operator

#Read the file in hex format (to simplify computation)
def open_file_hex(filename):
    with open(filename, 'rb') as f:
        hexdata = f.read().hex()
    return hexdata.upper()

def write_file(filename, content):
    with open(filename, 'x', encoding='ascii') as f:
        f.write(content)

def listToString(l):
    str1=""
    for element in l:
        str1+=element
    return str1

def freq_analysis(data,key_len,shift):
    values = []
    #shift represent a given char in the key
    i = shift
    while i < len(data):
        values.append(data[i]+data[i+1])
        i = i + key_len*2
    #Compute the frequencies of each cipher char, sort them in desceding order
    res_analysis = {i:values.count(i) for i in values}
    res_analysis = sorted(res_analysis.items(), key=operator.itemgetter(1), reverse=True)
    return res_analysis

def guess_key(data,key_len):
    key = []
    i = 0
    while i < key_len*2:
        #Take the second top frequency because first is probably space
        #XOR operation to retrieve a given char's key with the most frequent letter in FR alphabet : e (ASCII 101)
        key.append(chr(int(freq_analysis(data,key_len,i)[1][0],16)^101))
        i = i + 2
    return listToString(key)
    
def decrypt_xor(data, key):
    i = 0
    plaintxt = ""
    while i < len(data):
        for k in key:
            plaintxt += chr(int(data[i]+data[i+1],16)^ord(k))
            i = i + 2
    return plaintxt


data = open_file_hex('PA.txt')
key_computed = guess_key(data,6)
print("Key computed : "+key_computed)
decoded_content = decrypt_xor(data,key_computed)
write_file("PA_decrypt.txt", decoded_content)





