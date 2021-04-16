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

        self.itemMake = make
        self.itemModel = model
        self.itemSerial = serial
        self.itemValue = value

    def giveValues(self):
        print("Make: " + self.itemMake)
        print("Model " + self.itemModel)
        print("Serial " + self.itemSerial)
        print("Value: " + self.itemValue)

    def getMake(self):
        return self.itemMake
    
    def getModel(self):
        return self.itemModel
    
    def getSerial(self):
        return self.itemSerial

    def getValue(self):
        return self.itemValue
    
    