import tkinter as tk
from tkinter import ttk
from tkinter import * 
from tkinter import filedialog
from Main import Main
from Item import Item

class GUI:


    mainFunctions = Main()
# this is the function called when the button is clicked
    def loadConfigClicked(self):
        filepath = filedialog.askopenfilename(initialdir = "",title = "Choose Your Config File",filetypes = (("Yml files","*.yml"),("all files","*.*")))
        if filepath:
            # Update internal variable for the filepath
            self.mainFunctions.configFilePath = filepath
            self.mainFunctions.loadConfig()
            self.mainFunctions.loadKey()
            self.statusbar.config(text="Config Loaded")
        else:
            self.statusbar.config(text="Couldnt load config")
        

    # this is a function to get the user input from the text input box
    def getMakeInput(self):
        userInput = self.makeInput.get()
        return userInput


    # this is a function to get the user input from the text input box
    def getModelInput(self):
        userInput = self.modelInput.get()
        return userInput


    # this is a function to get the user input from the text input box
    def getSerialInput(self):
        userInput = self.serialInput.get()
        return userInput


    # this is a function to get the user input from the text input box
    def getValueInput(self):
        userInput = self.valueInput.get()
        return userInput


    # this is the function called when the button is clicked
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

    # this is the function called when the button is clicked
    def submitClicked(self):
        if self.validateClicked():
            theItem = Item(self.getMakeInput(),self.getModelInput(),self.getSerialInput(),self.getValueInput())

        if self.mainFunctions.readyToOperate():
            self.mainFunctions.addItem(theItem)
            self.statusbar.config(text="Item added to database!")
        else:
            self.statusbar.config(text="Please ensure the config is loaded!")



    # this is the function called when the button is clicked
    def setupClicked(self):
        self.mainFunctions.setup()
        self.statusbar.config(text="Setup is complete")


    # this is the function called when the show values button is clicked
    def showValuesClicked(self):
        if self.mainFunctions.readyToOperate():
            self.statusbar.config(text="Fetching items")
            allItems = self.mainFunctions.downloadAndShowData()
            
            # Clean up the old elements first
            for child in self.tree.get_children():
                self.tree.delete(child)

            # Add all the new ones
            for element in allItems:
                
                self.tree.insert(parent='',index='end', text="",values=(element.getMake(),element.getModel(),element.getSerial(),element.getValue()))

        else:
            self.statusbar.config(text="Please ensure the config is loaded!")



    def __init__(self):


        self.root = Tk()

        # This is the section of code which creates the main window
        self.root.geometry('1280x750')
        #root.configure(background='#F0F8FF')
        self.root.title('Serial Number App')


        # This is the section of code which creates a button
        Button(self.root, text='Load Config', font=('arial', 12, 'normal'), command=self.loadConfigClicked).place(x=12, y=7)



        # This is the section of code which creates a text input box
        self.makeInput=Entry(self.root)
        self.makeInput.place(x=12, y=77, width=100)


        # This is the section of code which creates a text input box
        self.modelInput=Entry(self.root)
        self.modelInput.place(x=12, y=117, width=100)


        # This is the section of code which creates a text input box
        self.serialInput=Entry(self.root)
        self.serialInput.place(x=12, y=157, width=100)


        # This is the section of code which creates a text input box
        self.valueInput=Entry(self.root)
        self.valueInput.place(x=12, y=197, width=100)


        # This is the section of code which creates the a label
        Label(self.root, text='Make', font=('arial', 12, 'normal')).place(x=12, y=55)


        # This is the section of code which creates the a label
        Label(self.root, text='Model', font=('arial', 12, 'normal')).place(x=12, y=95)


        # This is the section of code which creates the a label
        Label(self.root, text='Serial', font=('arial', 12, 'normal')).place(x=12, y=135)


        # This is the section of code which creates the a label
        Label(self.root, text='Value', font=('arial', 12, 'normal')).place(x=12, y=175)


        # This is the section of code which creates a button
        Button(self.root, text='Validate',font=('arial', 12, 'normal'), command=self.validateClicked).place(x=12, y=227)


        # This is the section of code which creates a button
        Button(self.root, text='Submit', font=('arial', 12, 'normal'), command=self.submitClicked).place(x=12, y=277)


        # This is the section of code which creates a button
        Button(self.root, text='Setup', font=('arial', 12, 'normal'), command=self.setupClicked).place(x=12, y=47)


        # This is the section of code which creates the a label
        self.makeLabel = Label(self.root, text='', font=('arial', 12, 'normal'))
        self.makeLabel.place(x=120, y=77)


        # This is the section of code which creates the a label
        self.modelLabel = Label(self.root, text='',font=('arial', 12, 'normal'))
        self.modelLabel.place(x=120, y=117)

        # This is the section of code which creates the a label
        self.serialLabel = Label(self.root, text='', font=('arial', 12, 'normal'))
        self.serialLabel.place(x=120, y=157)

        # This is the section of code which creates the a label
        self.valueLabel = Label(self.root, text='', font=('arial', 12, 'normal'))
        self.valueLabel.place(x=120, y=197)


        # This is the section of code which creates a button
        Button(self.root, text='Show All Values', font=('arial', 12, 'normal'), command=self.showValuesClicked).place(x=12, y=317)
        self.statusbar = tk.Label(self.root, text="Welcome" , bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.statusbar.pack(side=tk.BOTTOM, fill=tk.X)

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

        #fakeItem = Item("Chevy","Camaro","233","211")
        #self.tree.insert(parent='',index='end',values=(fakeItem.getMake(),fakeItem.getModel(),fakeItem.getSerial(),fakeItem.getValue()))
        self.tree.place(x=150,y=350)
        self.root.mainloop()


if __name__ == "__main__":
    gui = GUI()