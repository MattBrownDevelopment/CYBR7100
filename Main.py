import os
from Item import Item

print("Please enter a serial number ")
number = input("Enter serial number ")
print(number)

fakeItem = Item(serial=number,value="54")
fakeItem.giveValues()