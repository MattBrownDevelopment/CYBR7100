import boto3
import botocore
import yaml
import os

class DynamoDBClient:

    region = ""
    service = "dynamodb" #Currently only DynamoDB is used in this program
    secretKey = ""
    accessKey = ""
    tableName = ""

    # Function to load a config file for the table name, access key, secret key and update class variables

    def loadConfig(self, pathToConfig):
        if not os.path.exists(pathToConfig):
            print("Could not find config file")
        with open(pathToConfig, 'r') as configStream:
            try:
                data = yaml.safe_load(configStream) 
                self.region = data['region']
                self.secretKey = data['secretKey']
                self.accessKey = data['accessKey']
                self.tableName = data['TableName']
            except yaml.YAMLError as exc:
                print(exc)



    # Function to check if DynamoDB table already exists
    def tableExists(self):
        try:
            response = self.dynamoClient.describe_table(TableName=self.tableName)
            print("table exists")
            return True
        except self.dynamoClient.exceptions.ResourceNotFoundException:
            print("table doesnt exist")
            return False
    

    def putObjectInTable(self,data):
        if(self.tableExists):
            try:
                response = self.dynamoClient.put_item(TableName=self.tableName, Item={'Item':{'B':data}})
            except Exception as ex:
                print("Something went wrong adding to the table!")
                print(ex)
        else:
            print("Table does not exist, can not add item")

    def downloadAllObjects(self):
            if(self.tableExists):
                dbConn = boto3.resource('dynamodb',aws_access_key_id=self.accessKey, aws_secret_access_key=self.secretKey, region_name=self.region)
                table = dbConn.Table(self.tableName)
                response = table.scan()
                data = response['Items']
                print(data)
                while 'LastEvaluatedKey' in response:
                    print("??")
                    response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
                    data.extend(response['Items'])
                return data
            

    def __init__(self,configPath):
        if not os.path.exists(configPath):
            print("Could not find config file")
            return
        self.loadConfig(configPath)
        self.dynamoClient = boto3.client(self.service, aws_access_key_id=self.accessKey, aws_secret_access_key=self.secretKey, region_name=self.region)
