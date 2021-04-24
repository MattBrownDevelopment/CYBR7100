1: Requirements

This program requires Python3 to be installed on your system.
You will need an AWS account and have access to your secret key and access key

2: Setup

First ensure that all required packages are installed, using pip. Your specific python and pip installation may vary, but the instructions are as follows:

pip3 install -r requirements.txt

Then, copy config.yml.template to another file, such as config.yml

Fill out the values in the config file as follows:



region: What region you want to deploy to, such as: us-east-2

secretKey: Paste your AWS SECRET key here

accessKey: Paste your AWS ACCESS key here

TableName: Choose a name for your DynamoDB table

AESKeyPath: Path to a location to store your keyfile



Note that your AES Key file will be required to decrypt and encrypt data. DO NOT LOSE THIS.

3: First run

After your config file has been made and you have installed the dependencies, you are ready to run the setup function.
This will automatically connect to AWS, create a DynamoDB table, and create an AES key.

To do this, simple type in:

python3 main.py "path/to/config/file.yml" setup

Example, assuming config.yml is in the same directory as main.py

python3 main.py "config.yml" setup


4: Adding items to the database

To add items to the DynamoDB, simply run the script with the "add" command. Example:

python3 main.py "config.yml" add

You will be prompted to enter the make, model, serial number, and value of your item.
The program will then encrypt this information with the AES key specified in your config file and and store it in the DynamoDB table specified by your config file.

5: Showing items in the database:

To view the decrypted items in the DynamoDM, simply run the script with the "show" command. Example:

python3 main.py "config.yml" show

The program will then use your config file to connect to AWS, query the database, download all objects, and decrypt them then display them to you.

NOTE: None of your serial numbers or other information is stored locally on your machine. After you close the terminal window, this information will be gone. Note that it does NOT remove the info from the database.