import os
from Item import Item
from Datahandler import Cryptohandler
from Datahandler import Hasher
from Datahandler import Serializer
import pickle

# This file is the entry point into the program. Eventually it wall call the GUI. For now it is testing the backend stuff locally.


make = input("Enter make ")
model = input("Enter model ")
number = input("Enter serial number ")
value = input("Enter value ")

fakeItem = Item(make,model,number,value)
fakeItem.giveValues()