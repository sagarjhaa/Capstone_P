__author__ = 'sjha1'

from Tkinter import *
from constants import *
from pymongo import *

class importWidget():
    def __init__(self,root):

        self.var_database = None
        self.var_collection = None

        #Creating top level widget
        top=self.top=Toplevel(root,background= BACKGROUND)
        self.top.title("Database Settings")
        self.top.resizable(0,0)
        #self.top.grab_set_global()

        self.lbl_direction = Label(self.top,text="Please select one option:\n 1) Enter your Database and Collection name \n 2)Select the exisiting Database and Collection",background = BACKGROUND)
        self.lbl_direction.grid(row=0,column=0,columnspan=2,sticky=(W))



        #Dividing the widget into two frames , fr_one, fr_second
        self.fr_frame = Frame(self.top,background= BACKGROUND,borderwidth=2,highlightthickness=1)
        self.fr_frame.grid(row=1,column=0,ipadx=15,sticky=(W),ipady=15)

        #Widgets of frame one
        self.lbl_database = Label(self.fr_frame,text="Database",background= BACKGROUND)
        self.lbl_database.grid(row=0,column=0,sticky="nsew")

        self.txt_database = Entry(self.fr_frame)
        self.txt_database.grid(row=0,column=1,sticky=(W,E))

        self.lbl_collection = Label(self.fr_frame,text="Collection",background= BACKGROUND)
        self.lbl_collection.grid(row=1,column=0,sticky=(W),ipady=15)

        self.txt_collection = Entry(self.fr_frame)
        self.txt_collection.grid(row=1,column=1,sticky=(W,E))

        #Widgets of second frame
        self.fr_second = Frame(self.top,background= BACKGROUND,borderwidth=2,highlightthickness=1)
        self.fr_second.grid(row=1,column=1,ipadx=15,sticky="nsew")

        self.lbl_auto_database = Label(self.fr_second,text="Database",background= BACKGROUND)
        self.lbl_auto_database.grid(row=0,column=0,sticky=(W))

        #read the database names for option widget
        database_names = self.read_database_name()
        database_names.insert(0,"Select")
        self.var_database = StringVar(self.top)
        self.var_database.set(database_names[0])
        self.op_database = apply(OptionMenu,(self.fr_second,self.var_database) + tuple(database_names))
        self.op_database.grid(row=0,column=1,sticky=(E,W))
        self.op_database.config(width=10)

        self.lbl_auto_collection = Label(self.fr_second,text="Collection",background= BACKGROUND)
        self.lbl_auto_collection.grid(row=1,column=0,sticky=(W))

        #read the collections of each database for option widget
        collection_names = self.read_collection_name()
        collection_names.insert(0,"Select")
        self.var_collection = StringVar(self.top)
        self.var_collection.set(collection_names[0])
        self.op_collection = apply(OptionMenu,(self.fr_second,self.var_collection) + tuple(collection_names))
        self.op_collection.grid(row=1,column=1,sticky=(E,W))

        self.btn_load = Button(self.top,text="Load Data")
        self.btn_load.grid(row=4,column=0,sticky=(W),padx=20)

        self.btn_quit = Button(self.top,text="Quit",command=self.quit)
        self.btn_quit.grid(row=4,column=1,sticky=(E),padx=3)

        self.read_collection_name()

        self.top.grid_rowconfigure(0, weight=1)
        self.top.grid_rowconfigure(1, weight=3)
        #self.root.grid_columnconfigure(0, weight=0)
        #self.root.grid_columnconfigure(1, weight=6)

    def read_database_name(self):
        conn = MongoClient("localhost",27017)
        return conn.database_names()

    def read_collection_name(self):
        collections = []
        conn = MongoClient("localhost",27017)
        for dbase in conn.database_names():
            db = conn[dbase]
            collections.append(db.collection_names())

        new_collections = []
        for index in range(len(collections)):
            for each in collections[index]:
                new_collections.append(each)

        return new_collections

    def quit(self):
        self.top.destroy()

