from Crypto.Cipher import AES
from Crypto.Util import Counter
import os
import array

print "PyCrypto CBC and CTR..."
key='140b41b22a29beb4061bda66b6747e14'.decode('hex')
cipher='4ca00ff4c898d61e1edbf1800618fb2828a226d160dad07883d04e008a7897ee2e4b7465d5290d0c0e6c6822236e1daafb94ffe0c5da05d9476be028ad7c1d81'.decode('hex')
crypt = AES.new(key, AES.MODE_CBC, cipher[:16])
print "ex1: " + crypt.decrypt(cipher[16:])

key='140b41b22a29beb4061bda66b6747e14'.decode('hex')
cipher='5b68629feb8606f9a6667670b75b38a5b4832d0f26e1ab7da33249de7d4afc48\
e713ac646ace36e872ad5fb8a512428a6e21364b0c374df45503473c5242a253'.decode('hex')
crypt = AES.new(key, AES.MODE_CBC, cipher[:16])
print "ex2: " + crypt.decrypt(cipher[16:])

key='36f18357be4dbd77f050515c73fcf9f2'.decode('hex')
cipher='69dda8455c7dd4254bf353b773304eec0ec7702330098ce7f7520d1cbbb20fc3\
88d1b0adb5054dbd7370849dbf0b88d393f252e764f1f5f7ad97ef79d59ce29f5f51eeca32eabedd9afa9329'.decode('hex')
ctr = Counter.new(128, initial_value=long(cipher[:16].encode('hex'), 16))

crypt = AES.new(key, AES.MODE_CTR, counter=ctr)
print "ex3: " + crypt.decrypt(cipher[16:])

key='36f18357be4dbd77f050515c73fcf9f2'.decode('hex')
cipher='770b80259ec33beb2561358a9f2dc617e46218c0a53cbeca695ae45faa8952aa\
0e311bde9d4e01726d3184c34451'.decode('hex')
ctr = Counter.new(128, initial_value=long(cipher[:16].encode('hex'), 16))

crypt = AES.new(key, AES.MODE_CTR, counter=ctr)
print "ex4: " + crypt.decrypt(cipher[16:])

