from pyqldb.driver.qldb_driver import QldbDriver
import boto3
import botocore
import os
import yaml
import logging
from time import sleep
from qldb_helpers.block_address import *
from qldb_helpers.qldb_string_utils import *
from amazon.ion.simpleion import loads, dumps

# Class to handle QLDB ledger functions
# Most adapted from Amazon's examples:
# https://github.com/aws-samples/amazon-qldb-dmv-sample-python/tree/b3006dd005b11939912e30b4ab11a23fc72d3d9e/pyqldbsamples
class LedgerClient:

    region = ""
    service = "qldb"
    secretKey = ""
    accessKey = ""
    ledgerName = ""
    logger = logging.getLogger(__name__)
    logger.addHandler(logging.StreamHandler()) # Write to console in addition to file.

    #Modified from AWS example
    def create_qldb_driver(self):
        """
        Create a QLDB driver for executing transactions.
        :type ledger_name: str
        :param ledger_name: The QLDB ledger name.
        :type region_name: str
        :param region_name: See [1].
        :type endpoint_url: str
        :param endpoint_url: See [1].
        :type boto3_session: :py:class:`boto3.session.Session`
        :param boto3_session: The boto3 session to create the client with (see [1]).
        :rtype: :py:class:`pyqldb.driver.qldb_driver.QldbDriver`
        :return: A QLDB driver object.
        [1]: `Boto3 Session.client Reference <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/session.html#boto3.session.Session.client>`.
        """

        qldb_driver = QldbDriver(ledger_name=self.ledgerName, region_name=self.region,
                                boto3_session=self.session)
        return qldb_driver

    def loadConfig(self, pathToConfig):
        if not os.path.exists(pathToConfig):
            self.logger.error(msg="User = " + self.currentUser + ": Could not find config")     
        with open(pathToConfig, 'r') as configStream:
            try:
                data = yaml.safe_load(configStream) 
                self.region = data['region']
                self.secretKey = data['secretKey']
                self.accessKey = data['accessKey']
                self.ledgerName = data['LedgerName']
            except yaml.YAMLError as exc:
                self.logger.error(msg="User = " + self.currentUser + ": Error loading config")
                self.logger.info(exc)

    def createLedger(self):
        self.logger.info(msg="User = " + self.currentUser + " Creating the ledger named: " + self.ledgerName)
        result = self.ledgerClient.create_ledger(Name=self.ledgerName, PermissionsMode='ALLOW_ALL')
        return result

    def waitForActiveLedger(self):
        self.logger.info(msg="User = " + self.currentUser + ' Waiting for ledger to become active...')
        while True:
            result = self.ledgerClient.describe_ledger(Name=self.ledgerName)
            if result.get('State') == "ACTIVE":
                self.logger.info(msg="User = " + self.currentUser + ' Success. Ledger is active and ready to use.')
                return result
            self.logger.info(msg="User = " + self.currentUser + ' The ledger is still creating. Please wait...')
            sleep(15)

    def createAndFinalizeLedger(self):
        self.logger.info(msg="User = " + self.currentUser + ' Running Ledger and Table Setup...')
        if not self.ledgerExists():
            self.createLedger()
            self.waitForActiveLedger()

        # Create table will not make duplicates so its safe to call
        try:
            self.createTable()
        except Exception as ex:
            if (str(ex) == "An error occurred (BadRequestException) when calling the SendCommand operation: Table with name: USER.Transactions already exists"):
                self.logger.info(msg="User = " + self.currentUser + ' Ledger Table already exists')
                pass
            else:
                raise
        self.logger.info(msg="User = " + self.currentUser + ' Ledger setup is complete')

    def createTable(self):
        self.logger.info(msg="User = " + self.currentUser + " Creating the table in the ledger")
        statement = 'CREATE TABLE {}'.format("Transactions")
        cursor = self.qldb_driver.execute_lambda(lambda executor: executor.execute_statement(statement))
        self.logger.info(msg="User = " + self.currentUser + '{} table created successfully.'.format("Transactions "))
        return len(list(cursor))

    def listLedgers(self):
        result = self.ledgerClient.list_ledgers()
        ledgers = result.get('Ledgers')
        return ledgers

    def ledgerExists(self):
        allLedgers = self.listLedgers()
        for ledger in allLedgers:
            if self.ledgerName == ledger['Name']:
                return True
        return False

    def getDigest(self):
        self.logger.info(msg="User = " + self.currentUser + " Getting the current digest of the ledger named {}".format(self.ledgerName))
        result = self.ledgerClient.get_digest(Name=self.ledgerName)
        self.logger.info(msg="User = " + self.currentUser + ' Success. LedgerDigest: {}.'.format(digest_response_to_string(result)))
        return result

    def getDigestTipAddress(self):
        # Get the digest info and split the AWS IonText struct
        return self.getDigest()['DigestTipAddress']['IonText'].split("\"")[1]

    # Lambda function to insert document into ledger
    def insert_record(self, executor, arg1):
        executor.execute_statement("INSERT INTO Transactions ?", arg1)

    # Lambda function to get all documents from ledger
    def read_records(self, transaction_executor):
        cursor = transaction_executor.execute_statement("SELECT * FROM Transactions")
        dataToReturn = []

        for element in cursor:
            dataToReturn.append([element["Username"],element["TransactionID"]])

        return dataToReturn

    def writeTransaction(self, transactionID):
        # Struct for entry
        entry = { 'Username': self.currentUser,
          'TransactionID': transactionID
        }
        self.logger.info(msg="User = " + self.currentUser + ' Writing transaction to ledger')
        self.qldb_driver.execute_lambda(lambda x: self.insert_record(x, entry))

    def getAllTransactions(self):
        self.logger.info(msg="User = " + self.currentUser + ' Getting transactions from ledger')
        data = self.qldb_driver.execute_lambda(lambda x: self.read_records(x))
        return data

    # Finds if a specific transaction ID exists in the ledger
    def findTransaction(self,transactionID):
        self.logger.info(msg="User = " + self.currentUser + ' Finding specific transaction from ledger')
        allTransactions = self.getAllTransactions()
        for transaction in allTransactions:
            if transaction[1] == str(transactionID): #ID is stored as the 1 indexed item
                self.logger.info(msg="User = " + self.currentUser + ' Found transaction ID in ledger')
                return True

        self.logger.info(msg="User = " + self.currentUser + ' Could not find transaction ID in ledger')
        return False



    def __init__(self,configPath):
        self.currentUser = os.getlogin()
        if not os.path.exists(configPath):
            print("Could not find config file")
            return
        self.loadConfig(configPath)
        self.session = boto3.Session(aws_access_key_id=self.accessKey, aws_secret_access_key=self.secretKey, region_name=self.region)# botocore_session=None, profile_name=None)
        self.ledgerClient = boto3.client(self.service, aws_access_key_id=self.accessKey, aws_secret_access_key=self.secretKey, region_name=self.region)
        self.qldb_driver = self.create_qldb_driver()