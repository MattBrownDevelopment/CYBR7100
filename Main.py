import os
from Item import Item
from Datahandler import Cryptohandler as Cryptohandler
from Datahandler import Hasher as Hasher
from Datahandler import Serializer as Serializer
from DatabaseClient import DynamoDBClient


def getKey(keyPath):
    aesKey = Cryptohandler.makeKey(32,keyPath)
    return aesKey
    
    #keyPhrase = input(" Select a 32 character passphrase ")
    #if len(keyPhrase) != 32:
    #    print("uh oh")
    #else:
    # Need a byte representation for encryption
     #   return str.encode(keyPhrase)

# This file is the entry point into the program. Eventually it wall call the GUI. For now it is testing the backend stuff locally.


make = input("Enter make ")
model = input("Enter model ")
number = input("Enter serial number ")
value = input("Enter value ")

fakeItem = Item(make,model,number,value)
#fakeItem.giveValues()
theKey = getKey("myKey.txt")

serlilazer = Serializer()
serialData = serlilazer.serializeObject(fakeItem)

encryptor = Cryptohandler(str(theKey))
data = encryptor.encrypt(serialData)

cloudHandler = DynamoDBClient("config.yml")
cloudHandler.putObjectInTable(data)
#Then store the encrypted data on AWS



#Then download data off AWS
allData = cloudHandler.downloadAllObjects()
#print(type(allData))
#Then decrypt data from AWS
decryptor = Cryptohandler(str(theKey))
decryptedData = decryptor.decrypt(allData[0]['Item'].value)


#Reassemble the data
finalObj = serlilazer.unserializeObject(str.encode(decryptedData))
print("Giving values")
finalObj.giveValues()




