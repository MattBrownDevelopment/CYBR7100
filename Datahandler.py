from Crypto.Cipher import AES
import pickle

# This file will contain classes for low(er) level data handling, like encryption, hashing, and serializing.

# This class will handle encryption and decryption
class Cryptohandler:

    def encryptData(self, string, key):
        cipher = AES.new(key, AES.MODE_EAX)
        nonce = cipher.nonce
        ciphertext, tag = cipher.encrypt_and_digest(string)

        return ciphertext, tag, nonce

    def decryptData(self, string, key, tag, nonce):
        cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
        plaintext = cipher.decrypt(string)
        try:
            cipher.verify(tag)
            print("This is authenticated")
            return True, plaintext
        except:
            print("Bad key or corruption has occured")
            return False

class Hasher:

    def hashObject(self, objectToHash):
        return False


class Serializer:

    def serializeObject(self, objectToSerialize):
        serialData = pickle.dumps(objectToSerialize)
        return serialData
    
    def unserializeObject(self, data):
        restoredObject = pickle.loads(data)
        return restoredObject

