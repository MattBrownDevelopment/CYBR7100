class Item:

    itemMake = ""
    itemModel = ""
    itemSerial = ""
    itemValue = ""

    def __init__(self, make="", model="", serial="", value=""):
        if not make:
            print("Make of item is unspecified, defaulting to undefined")
            make = "Undefined"
        
        if not model:
            print("Model of item is unspecified, defaulting to undefined")
            model = "Undefined"

        if not serial: 
            print("Serial number is unspecified. This is required. EXITING")
            return
        
        if not value:
            print("Value is unspecified, defaulting to 0")
            value = 0
        
        if not value.isnumeric:
            print("ERROR: Value must be a numeric. EXITING")

        print("New item is made")
        print("Make is: " + make)
        print("Model is: " + model)
        print("Serial is: " + serial)
        print("Value is: " + value)

        self.itemMake = make
        self.itemModel = model
        self.itemSerial = serial
        self.itemValue = value

    def giveValues(self):
        print(self.itemMake)
        print(self.itemModel)
        print(self.itemSerial)
        print(self.itemValue)

    def getMake(self):
        return self.itemMake
    
    def getModel(self):
        return self.itemModel
    
    def getSerial(self):
        return self.itemSerial

    def getValue(self):
        return self.itemValue