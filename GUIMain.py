import tkinter as tk
from tkinter import ttk
from tkinter import * 
from tkinter import filedialog
from Main import Main
from Item import Item

class GUI:


    backendFunctions = Main()
    configLoaded = False

    def loadConfigClicked(self):
        filepath = filedialog.askopenfilename(initialdir = "",title = "Choose Your Config File",filetypes = (("Yml files","*.yml"),("all files","*.*")))
        if filepath:
            # Update internal variable for the filepath
            self.backendFunctions.configFilePath = filepath
            self.backendFunctions.loadConfig()
            self.backendFunctions.loadKey()
            self.statusbar.config(text="Config Loaded")
            self.configLoaded = True
        else:
            self.statusbar.config(text="Couldnt load config")
            self.configLoaded = False
        

    def getMakeInput(self):
        userInput = self.makeInput.get()
        return userInput


    def getModelInput(self):
        userInput = self.modelInput.get()
        return userInput


    def getSerialInput(self):
        userInput = self.serialInput.get()
        return userInput


    def getValueInput(self):
        userInput = self.valueInput.get()
        return userInput


    def validateClicked(self):

        make = self.getMakeInput()
        if not make:
            self.makeLabel.config(text="This can not be empty")
        else:
            self.makeLabel.config(text="")

        model = self.getModelInput()
        if not model:
            self.modelLabel.config(text="This can not be empty")
        else:
            self.modelLabel.config(text="")

        serial = self.getSerialInput()
        if not serial:
            self.serialLabel.config(text="This can not be empty")
        else:
            self.serialLabel.config(text="")


        value = self.getValueInput()
        if not value or not value.isnumeric():
            self.valueLabel.config(text='This can not be empty and must be numeric')
        else:
            self.valueLabel.config(text="")
        
        isValid = Item.validateItem(make,model,serial,value)

        if isValid:
            self.statusbar.config(text="Item entry is validated")
            return True
        else:
            self.statusbar.config(text="Item entry is invalid")
            return False

    def submitClicked(self):
        if self.validateClicked():
            theItem = Item(self.getMakeInput(),self.getModelInput(),self.getSerialInput(),self.getValueInput())

        if self.backendFunctions.readyToOperate():
            self.backendFunctions.addItem(theItem)
            self.statusbar.config(text="Item added to database!")
        else:
            self.statusbar.config(text="Please ensure the config is loaded!")



    def setupClicked(self):
        if self.configLoaded:
            self.backendFunctions.setup()
            self.statusbar.config(text="Setup is complete")
        else:
            self.statusbar.config(text="Please ensure the config is loaded!")


    def showValuesClicked(self):
        if self.backendFunctions.readyToOperate():
            self.statusbar.config(text="Fetching items")
            allItems = self.backendFunctions.downloadAndShowData()
            
            # Clean up the old elements first
            for child in self.tree.get_children():
                self.tree.delete(child)

            # Add all the new ones
            for element in allItems:
                
                self.tree.insert(parent='',index='end', text="",values=(element.getMake(),element.getModel(),element.getSerial(),"$" + str(element.getValue())))
                
                
            self.statusbar.config(text="Items Fetched")

        else:
            self.statusbar.config(text="Please ensure the config is loaded!")



    def __init__(self):


        self.root = Tk()
        self.root.columnconfigure((0,1,2), weight=1)
        self.root.geometry('1200x600')
        self.root.title('Serial Number App')


        self.loadConfigButton = Button(self.root, text='Load Config', font=('arial', 12, 'normal'), command=self.loadConfigClicked)#.place(x=12, y=7)
        self.loadConfigButton.grid(row = 0, column = 0, pady = 5)

        self.setupButton = Button(self.root, text='Run Setup', font=('arial', 12, 'normal'), command=self.setupClicked)#.place(x=12, y=47)
        self.setupButton.grid(row = 0, column = 1, pady = 5)
 

        self.makeInput=Entry(self.root)
        self.makeInput.grid(row = 1, column = 1, pady = 5)



        self.modelInput=Entry(self.root)
        self.modelInput.grid(row = 2, column = 1, pady = 5)

        self.serialInput=Entry(self.root)
        self.serialInput.grid(row = 3, column = 1, pady = 5)

        self.valueInput=Entry(self.root)
        self.valueInput.grid(row = 4, column = 1, pady = 5)

        self.staticmakeLabel = Label(self.root, text='Make', font=('arial', 12, 'normal'))
        self.staticmakeLabel.grid(row = 1, column = 0, pady = 5)

        self.staticmodelLabel = Label(self.root, text='Model', font=('arial', 12, 'normal'))
        self.staticmodelLabel.grid(row = 2, column = 0, pady = 5)

        self.staticserialLabel = Label(self.root, text='Serial', font=('arial', 12, 'normal'))
        self.staticserialLabel.grid(row = 3, column = 0, pady = 5)


        self.staticvalueLabel = Label(self.root, text='Value', font=('arial', 12, 'normal'))
        self.staticvalueLabel.grid(row = 4, column = 0, pady = 5)

        self.validateButton = Button(self.root, text='Validate',font=('arial', 12, 'normal'), command=self.validateClicked)
        self.validateButton.grid(row = 5, column = 0, pady = 5)



        self.submitButton = Button(self.root, text='Submit to DB', font=('arial', 12, 'normal'), command=self.submitClicked)
        self.submitButton.grid(row = 5, column = 1, pady = 5)




        self.makeLabel = Label(self.root, text='', font=('arial', 12, 'normal'))
        self.makeLabel.grid(row = 1, column = 3, pady = 5)

        self.modelLabel = Label(self.root, text='',font=('arial', 12, 'normal'))
        self.modelLabel.grid(row = 2, column = 3, pady = 5)

        self.serialLabel = Label(self.root, text='', font=('arial', 12, 'normal'))
        self.serialLabel.grid(row = 3, column = 3, pady = 5)


        self.valueLabel = Label(self.root, text='', font=('arial', 12, 'normal'))
        self.valueLabel.grid(row = 4, column = 3, pady = 5)



        self.queryDBButton = Button(self.root, text='Query and Update Values', font=('arial', 12, 'normal'), command=self.showValuesClicked)
        self.queryDBButton.grid(row = 6, column = 0, pady = 5, columnspan = 3)
        self.statusbar = Label(self.root, text="Welcome, statuses will appear here")
        self.statusbar.grid(row = 8, column = 0,columnspan= 4)

        # Make a tree for the database objects
        self.tree = ttk.Treeview(self.root,columns=("Make","Model","Serial","Value"))
        self.tree.heading('#0',text='Make')
        self.tree.heading('#1',text='Model')
        self.tree.heading('#2',text='Serial')
        self.tree.heading('#3',text='Value')
        self.tree.column('#0', stretch=tk.YES)
        self.tree.column('#1', stretch=tk.YES)
        self.tree.column('#2', stretch=tk.YES)
        self.tree.column('#3', stretch=tk.YES)
        self.treeview = self.tree

        self.tree.grid(row = 7, column = 0, columnspan = 3)
        
        self.root.mainloop()


if __name__ == "__main__":
    gui = GUI()