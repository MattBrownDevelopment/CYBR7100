from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from Cryptodome import Random
import hashlib
import base64
import pickle

# This file will contain classes for low(er) level data handling, like encryption, hashing, and serializing.

# Implemented and modified from: https://stackoverflow.com/questions/12524994/encrypt-decrypt-using-pycrypto-aes-256
class Cryptohandler:
    def __init__(self, key): 
        self.bs = AES.block_size
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw.encode()))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]

    @staticmethod
    def makeKey(length, keyOutputPath):
        if length == 16: #AES128
            key = get_random_bytes(length)
        elif length == 24: #AES192
            key = get_random_bytes(length)
        elif length == 32: #AES256
            key = get_random_bytes(length)

        with open(keyOutputPath,'wb') as keyfile:
            keyfile.write(key)
        
        return key
        

# Not implemented yet
class Hasher:

    @staticmethod
    def hashObject(objectToHash):
        return False


class Serializer:

    @staticmethod
    def serializeObject(objectToSerialize):
        #Hacky way of doing this because I am encrypting the bytes, it causes weird str to byte and vice versa issues on the pickle loading
        serialData = pickle.dumps(objectToSerialize,0).decode() 
        return str(serialData)

    @staticmethod
    def unserializeObject(data):
        restoredObject = pickle.loads(data)
        return restoredObject

