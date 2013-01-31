import re
import sys
from collections import Counter
import string

secret = "32510ba9babebbbefd001547a810e67149caee11d945cd7fc81a05e9f85aac650e9052ba6a8cd8257bf14d13e6f0a803b54fde9e77472dbff89d71b57bddef121336cb85ccb8f3315f4b52e301d16e9f52f904"   

keys = {}

def read_file(file):
    with open(file) as lines:
        for line in lines:
            yield line.strip().decode('hex')

def getKey():
    key = "" 
    for index, c in enumerate(secret):
        try:
            key = key + Counter(keys[index]).most_common(1)[0][0]
        except KeyError:
            key = key + '-'
    return key

def strxor(a, b):
    if len(a) > len(b):
        return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a[:len(b)], b)])
    else:
        return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a, b[:len(a)])])

def main():
    ciphers = list(read_file("ciphers.txt"))

    for i in range(len(ciphers)):
        for j in range(i, len(ciphers)):
            if i == j:
                continue;
            for index, c in enumerate(strxor("".join(ciphers[i]), "".join(ciphers[j]))):
                if re.match("[a-zA-Z]", c):
                    key1 = chr(ord(ciphers[i][index])^32)
                    key2 = chr(ord(ciphers[j][index])^32)
                    keys[index] = keys.get(index, []) + [key1]
                    keys[index] = keys.get(index, []) + [key2]

    key = getKey()
    
    for c in ciphers:
        print strxor("".join(c), key)

if __name__ == "__main__":
    main()
