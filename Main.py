import os
import logging
import datetime
import argparse
import yaml
from Item import Item
from Datahandler import Cryptohandler as Cryptohandler
from Datahandler import Hasher as Hasher
from Datahandler import Serializer as Serializer
from DatabaseClient import DynamoDBClient
import boto3

class Demo:

    configFilePath = ""
    logging.basicConfig(filename="applog.log",filemode='a',format='%(asctime)s,%(levelname)s, %(message)s',datefmt='%Y:%m:%d:%H:%M:%S', level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.addHandler(logging.StreamHandler()) # Write to console in addition to file.

    def __init__(self,configPath):
        self.configFilePath = configPath
        self.currentUser = os.getlogin()

        self.logger.info(msg="User = " + self.currentUser + ": STARTING SESSION")


        self.loadConfig()
        if not os.path.exists(self.keyPath):
            self.logger.error(msg="User = " + self.currentUser + ": Key file path does not exist yet!")
        else:
            with open(self.keyPath, "rb") as file:
                self.theKey = file.read()
                self.logger.info(msg="User = " + self.currentUser + ": Key loaded into memory")
        
    def loadConfig(self):
        if not os.path.exists(self.configFilePath):
            self.logger.error(msg="User = " + self.currentUser + ": Could not find config file")
        with open(self.configFilePath, 'r') as configStream:
            try:
                data = yaml.safe_load(configStream) 
                self.keyPath = data['AESKeyPath']
            except yaml.YAMLError as exc:
                self.logger.error(msg="User = " + self.currentUser + ": Error reading config file")
                self.logger.error(msg=str(exc))

    def makeKey(self):
        keyPath = self.keyPath
        if os.path.exists(keyPath):
            logging.error(msg="User = " + self.currentUser + ": Key file already exists, not overwriting!")
        else:
            Cryptohandler.makeKey(32,keyPath)
            logging.info(msg="User = " + self.currentUser + ": New AES key created at " + keyPath)

    def downloadAndShowData(self):
        self.logger.info(msg="User = " + self.currentUser + ": Creating DB client")
        try:
            cloudHandler = DynamoDBClient(self.configFilePath)
            self.logger.info(msg="User = " + self.currentUser + ": Created DB client")
        except Exception as ex:
            self.logger.error(msg="User = " + self.currentUser + ": Error creating DB client")
            self.logger.error(msg=str(ex))
            return
        #Then download data off AWS
        try:
            self.logger.info(msg="User = " + self.currentUser + ": Starting DB download")
            allData = cloudHandler.downloadAllObjects()
            self.logger.info(msg="User = " + self.currentUser + ": DB Download finished")
        except Exception as ex:
            self.logger.error(msg="User = " + self.currentUser + ": Error downloading from DB")
            self.logger.error(msg=str(ex))
            return

        # Error getting data
        if allData == None:
            self.logger.info(msg="User = " + self.currentUser + ": Unable to retrieve data")
            return

        # Make a decrypter object
        decryptor = Cryptohandler(str(self.theKey))

        # Make a variable to hold decrypted data
        dataHolder = []

        self.logger.info(msg="User = " + self.currentUser + ": Starting decryption of data")
        # Loop through all the downloaded objects, and append them to the dataHolder.
        for element in allData:
            decryptedData = decryptor.decrypt(element['Item'].value)
            dataHolder.append(decryptedData)


        serlilazer = Serializer()

        #Reassemble the data
        
        self.logger.info(msg="User = " + self.currentUser + ": There were " + str(len(dataHolder)) + " items in the database")
        print("\n")
        for decryptedItem in dataHolder:
            decodedObj = serlilazer.unserializeObject(str.encode(decryptedItem))
            decodedObj.giveValues()
            print("\n")


    def addItem(self):
        make = input("Enter make ")
        model = input("Enter model ")
        number = input("Enter serial number ")
        value = input("Enter value ")

        tempItem = Item(make,model,number,value)
        serlilazer = Serializer()
        self.logger.info(msg="User = " + self.currentUser + ": Item created, serializing item")
        serialData = serlilazer.serializeObject(tempItem)

        encryptor = Cryptohandler(str(self.theKey))
        self.logger.info(msg="User = " + self.currentUser + ": Item encrypted")
        data = encryptor.encrypt(serialData)
        
        self.logger.info(msg="User = " + self.currentUser + ": Attempting to add item to DB")
        try:
            cloudHandler = DynamoDBClient(self.configFilePath)
            cloudHandler.putObjectInTable(data)
            self.logger.info(msg="User = " + self.currentUser + ": Item added successfully to DB!")
        except Exception as ex:
            self.logger.error(msg="User = " + self.currentUser + ": Error adding item to DB")
            self.logger.error(str(ex))


    def makeTable(self):

        self.logger.info(msg="User = " + self.currentUser + ": Creating DB client")
        try:
            cloudHandler = DynamoDBClient(self.configFilePath)
            self.logger.info(msg="User = " + self.currentUser + ": Created DB client")
        except Exception as ex:
            self.logger.error(msg="User = " + self.currentUser + ": Error creating DB client")
            self.logger.error(msg=str(ex))

        try:
            self.logger.info(msg="User = " + self.currentUser + ": Creating DB table")
            cloudHandler.createTable()
            self.logger.info(msg="User = " + self.currentUser + ": DB Table Made")
        except Exception as ex:
            self.logger.error(msg="User = " + self.currentUser + ": Error creating DB")
            self.logger.error(msg=str(ex))

    def setup(self):
        self.logger.info(msg="User = " + self.currentUser + ": Running setup tasks")
        self.makeKey()
        self.makeTable()
        self.logger.info(msg="User = " + self.currentUser + ": Setup Complete!")

        


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("config",help="Path to config file")
    parser.add_argument("action",help="Add or show")
    args = parser.parse_args()

    if not os.path.exists(args.config):
        print("Could not find config file! Please ensure the path exists")

    demoApp = Demo(args.config)

    if args.action.lower() == "show":
        demoApp.downloadAndShowData()
    elif args.action.lower() == "add":
        demoApp.addItem()
    elif args.action.lower() == "makekey":
        demoApp.makeKey()
    elif args.action.lower() == "maketable":
        demoApp.makeTable()
    elif args.action.lower() == "setup":
        demoApp.setup()
    else:
        print("Invalid option!")


  
