from Crypto.Cipher import AES
from Crypto.Util import Counter
import os
import array
import binascii

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS) 
unpad = lambda s : s[0:-ord(s[-1])]

def xor(first, second):
    output = []
    for f, s in zip(first, second):
        output.append(chr(f^s))
    return output

def chunks(l, n):
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

def cbc_decrypt(iv, cipher, key):
    iv_arr = bytearray(iv)
    decryptor = AES.new(key)
    output = []

    for chunk in chunks(cipher, BS):
        output = output + xor(map(ord, decryptor.decrypt(chunk)), iv_arr)
        iv_arr = bytearray(chunk)

    return "".join(output)

def ctr_decrypt(iv, cipher, key):
    iv_arr = bytearray(iv)
    decryptor = AES.new(key)
    output = []
    cipher = pad(cipher)
    ctr = Counter.new(128, initial_value=long(iv.encode('hex'), 16))

    for chunk in chunks(cipher, BS):
        output = output + xor(map(ord, decryptor.encrypt(ctr())), bytearray(chunk))
    return "".join(output)


key='140b41b22a29beb4061bda66b6747e14'.decode('hex')
iv='4ca00ff4c898d61e1edbf1800618fb2828a226d160dad07883d04e008a7897ee2e4b7465d5290d0c0e6c6822236e1daafb94ffe0c5da05d9476be028ad7c1d81'.decode('hex')[:16]
cipher='4ca00ff4c898d61e1edbf1800618fb2828a226d160dad07883d04e008a7897ee2e4b7465d5290d0c0e6c6822236e1daafb94ffe0c5da05d9476be028ad7c1d81'.decode('hex')[16:]
print "ex1: " + cbc_decrypt(iv, cipher, key)

key='140b41b22a29beb4061bda66b6747e14'.decode('hex')
iv='5b68629feb8606f9a6667670b75b38a5b4832d0f26e1ab7da33249de7d4afc48e713ac646ace36e872ad5fb8a512428a6e21364b0c374df45503473c5242a253'.decode('hex')[:16]
cipher='5b68629feb8606f9a6667670b75b38a5b4832d0f26e1ab7da33249de7d4afc48e713ac646ace36e872ad5fb8a512428a6e21364b0c374df45503473c5242a253'.decode('hex')[16:]
print "ex2: " + cbc_decrypt(iv, cipher, key)

key='36f18357be4dbd77f050515c73fcf9f2'.decode('hex')
iv='69dda8455c7dd4254bf353b773304eec0ec7702330098ce7f7520d1cbbb20fc388d1b0adb5054dbd7370849dbf0b88d393f252e764f1f5f7ad97ef79d59ce29f5f51eeca32eabedd9afa9329'.decode('hex')[:16]
cipher='69dda8455c7dd4254bf353b773304eec0ec7702330098ce7f7520d1cbbb20fc388d1b0adb5054dbd7370849dbf0b88d393f252e764f1f5f7ad97ef79d59ce29f5f51eeca32eabedd9afa9329'.decode('hex')[16:]
print "ex3: " + ctr_decrypt(iv, cipher, key)

key='36f18357be4dbd77f050515c73fcf9f2'.decode('hex')
iv='770b80259ec33beb2561358a9f2dc617e46218c0a53cbeca695ae45faa8952aa0e311bde9d4e01726d3184c34451'.decode('hex')[:16]
cipher='770b80259ec33beb2561358a9f2dc617e46218c0a53cbeca695ae45faa8952aa0e311bde9d4e01726d3184c34451'.decode('hex')[16:]
print "ex4: " + ctr_decrypt(iv, cipher, key)
