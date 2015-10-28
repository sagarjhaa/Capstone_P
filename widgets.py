__author__ = 'sjha1'

from Tkinter import *
from constants import *
from pymongo import MongoClient
import csv

class importWidget():
    def __init__(self,root,text,directory):

        self.text = text
        self.directory = directory
        self.var_database = None
        self.var_collection = None

        #Creating top level widget
        top=self.top=Toplevel(root,background= BACKGROUND)
        self.top.title("Database Settings")
        self.top.resizable(0,0)
        #self.top.grab_set_global()

        text = "Please use only one option"\
               "\n1) Enter new Database and Collection Name"\
               "\n2) Use the existing Database and Collection"\
               "\nPriority will be given to the option 1"

        self.lbl_direction = Label(self.top,text="Please use only one option",background = BACKGROUND)
        self.lbl_direction.grid(row=0,column=0,columnspan=2,sticky=(W),padx=5)

        self.lbl_direction1 = Label(self.top,text="1) Enter new Database and Collection Name",background = BACKGROUND)
        self.lbl_direction1.grid(row=1,column=0,columnspan=2,sticky=(W),padx=5)

        self.lbl_direction2 = Label(self.top,text="2) Use Existing Database and Collection",background = BACKGROUND)
        self.lbl_direction2.grid(row=2,column=0,columnspan=2,sticky=(W),padx=5)

        self.lbl_direction3 = Label(self.top,text="Priority will be given to option 1",background = BACKGROUND)
        self.lbl_direction3.grid(row=3,column=0,columnspan=2,sticky=(W),padx=5)

        #Dividing the widget into two frames , fr_one, fr_second
        self.fr_frame = Frame(self.top,background= BACKGROUND,borderwidth=2,highlightthickness=1)
        self.fr_frame.grid(row=4,column=0,ipadx=15,sticky=(W),ipady=2,padx=5,pady=10)

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
        self.fr_second.grid(row=4,column=1,columnspan=2,ipadx=5,sticky="nsew",padx=5,pady=10)

        self.lbl_auto_database = Label(self.fr_second,text="Database",background= BACKGROUND)
        self.lbl_auto_database.grid(row=0,column=0,sticky=(W))

        #read the database names for option widget
        database_names = self.read_database_name()
        database_names.insert(0,"Select")
        self.var_database = StringVar(self.top)
        self.var_database.set(database_names[0])
        self.op_database = apply(OptionMenu,(self.fr_second,self.var_database) + tuple(database_names))
        self.op_database.grid(row=0,column=1,sticky=(E,W),ipadx=10)


        self.lbl_auto_collection = Label(self.fr_second,text="Collection",background= BACKGROUND)
        self.lbl_auto_collection.grid(row=1,column=0,sticky=(W))

        #read the collections of each database for option widget
        collection_names = self.read_collection_name()
        collection_names.insert(0,"Select")
        self.var_collection = StringVar(self.top)
        self.var_collection.set(collection_names[0])
        self.op_collection = apply(OptionMenu,(self.fr_second,self.var_collection) + tuple(collection_names))
        self.op_collection.grid(row=1,column=1,sticky=(E,W))

        self.status = Label(self.top,text="Status Message",background=BACKGROUND)
        self.status.grid(row=5,column=0,sticky=(W,N),rowspan=2)

        self.btn_load = Button(self.top,text="Load Data",command=self.load_data_into_mongo)
        self.btn_load.grid(row=5,column=1,ipadx=15,rowspan=2)

        self.btn_quit = Button(self.top,text="Quit",command=self.quit)
        self.btn_quit.grid(row=5,column=2,ipadx=20,rowspan=2)

        self.read_collection_name()

        self.top.grid_rowconfigure(0, weight=1)
        self.top.grid_rowconfigure(1, weight=3)

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

    def add_record_to_mongo(self,collection, record,text):

        mongo_coll = collection

        # Now let's insert
        writeCalculations(text,record,False,None)
        mongo_coll.insert(record)

    def run_csv_file(self,csvfile, database,collection,text):
        data = 'Gonna load the CSV file "{csvfile}" into mongodb "{mongo}"\n'.format(csvfile=csvfile, mongo=str(database)+":"+str(collection))
        writeCalculations(self.text,data,False,None)
        with open(csvfile,'rb') as incsv:
            parsed = csv.DictReader(incsv, delimiter=',', quotechar='"')
            for record in parsed:
                self.add_record_to_mongo(collection, record,text)


    def load_data_into_mongo(self):

        db = self.txt_database.get()
        coll = self.txt_collection.get()

        db1 = self.var_database.get()
        coll1 = self.var_collection.get()


        if db <> "" and coll <> "":

            conn = MongoClient("localhost",27017)
            text = "Moving Data into \nDatabase: %s \nCollection: %s" % (str(db),str(coll))
            self.status.configure(text=text)
            db = conn[db]
            coll = db[coll]
            #self.run_csv_file(self.directory,db,coll,self.text)

        elif db1 <> "" and coll1 <> "":

            conn = MongoClient("localhost",27017)
            text = " Moving Data into \nDatabase: %s \nCollection: %s" % (str(db1),str(coll1))
            self.status.configure(text=text)
            db = conn[db1]
            coll = db[coll1]
            #self.run_csv_file(self.directory,db,coll,self.text)

        else:
            writeCalculations(self.text,"Some Error Occurred",False,None)



    def quit(self):
        self.top.destroy()

