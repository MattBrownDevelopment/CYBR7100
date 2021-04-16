import boto3
import botocore
import yaml
import os
import logging

class DynamoDBClient:

    region = ""
    service = "dynamodb" #Currently only DynamoDB is used in this program
    secretKey = ""
    accessKey = ""
    tableName = ""
    logger = logging.getLogger(__name__)
    #logging.basicConfig(filename="database.log",filemode='a',format='%(asctime)s,%(levelname)s, %(message)s',datefmt='%H:%M:%S', level=logging.INFO)
    logger.addHandler(logging.StreamHandler()) # Write to console in addition to file.


    # Function to load a config file for the table name, access key, secret key and update class variables

    def loadConfig(self, pathToConfig):
        if not os.path.exists(pathToConfig):
            self.logger.error(msg="User = " + self.currentUser + ": Could not find config")     
        with open(pathToConfig, 'r') as configStream:
            try:
                data = yaml.safe_load(configStream) 
                self.region = data['region']
                self.secretKey = data['secretKey']
                self.accessKey = data['accessKey']
                self.tableName = data['TableName']
            except yaml.YAMLError as exc:
                self.logger.error(msg="User = " + self.currentUser + ": Error loading config")
                self.logger.info(exc)


    # Function to check if DynamoDB table already exists
    def tableExists(self):
        try:
            response = self.dynamoClient.describe_table(TableName=self.tableName)
            self.logger.info(msg="User = " + self.currentUser + ": DB Table exists")
            return True
        except self.dynamoClient.exceptions.ResourceNotFoundException:
            self.logger.info(msg="User = " + self.currentUser + ": Table does not exist")
            return False
    

    def putObjectInTable(self,data):
        if(self.tableExists()):
            try:
                response = self.dynamoClient.put_item(TableName=self.tableName, Item={'Item':{'B':data}})
                return True
            except Exception as ex:
                self.logger.error(msg="User = " + self.currentUser + ": Error adding object to table")
                self.logger.info(ex)
                return False
        else:
            self.logger.error(msg="User = " + self.currentUser + ": Table does not exist, can not add item to table!")
            return False

    def downloadAllObjects(self):
        # Block of code to go through the DB and get all objects.
            if(self.tableExists()):
                dbConn = boto3.resource('dynamodb',aws_access_key_id=self.accessKey, aws_secret_access_key=self.secretKey, region_name=self.region)
                table = dbConn.Table(self.tableName)
                response = table.scan()
                data = response['Items']
                # This part lets it get all objects, as there is not currently a way to query all objects with the boto3 API
                while 'LastEvaluatedKey' in response:
                    response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
                    data.extend(response['Items'])
                return data
            else:
                self.logger.error(msg="User = " + self.currentUser + ": Table does not exist")
            

    # Modified from https://www.edureka.co/community/39063/how-to-create-a-dynamodb-table-using-python
    def createTable(self):
        if not self.tableExists():
            try:
                self.dynamoClient.create_table(
                    TableName=self.tableName,
                    KeySchema=[
                        {
                            'AttributeName': 'Item',
                            'KeyType': 'HASH'  #Partition key
                        }
                    ],
                    AttributeDefinitions=[
                        {
                            'AttributeName': 'Item',
                            'AttributeType': 'B'
                        }

                    ],
                    ProvisionedThroughput={
                        'ReadCapacityUnits': 5,
                        'WriteCapacityUnits': 5
                    }
                )

            except Exception as ex:
                self.logger.error(msg="User = " + self.currentUser + ": Error creating table")
                self.logger.info(ex)

        else:
            self.logger.error(msg="User = " + self.currentUser + ": Table already exists")

    def __init__(self,configPath):
        self.currentUser = os.getlogin()
        if not os.path.exists(configPath):
            print("Could not find config file")
            return
        self.loadConfig(configPath)
        self.dynamoClient = boto3.client(self.service, aws_access_key_id=self.accessKey, aws_secret_access_key=self.secretKey, region_name=self.region)
        
