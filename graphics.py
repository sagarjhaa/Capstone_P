__author__ = 'sjha1'

from Tkinter import *
from constants import *
from pymongo import MongoClient
import csv
import subprocess as sp

import pymongo
from neo4jrestclient.client import GraphDatabase

class generate_graph():
    def __init__(self,root,text):

        self.text = text
        #self.directory = directory
        self.var_database = None
        self.var_collection = None
        self.record_count = 1
        self.proc = None

        #Creating top level widget
        top=self.top=Toplevel(root,background= BACKGROUND)

        self.top.title("Graph Settings")
        self.top.resizable(0,0)

        #Widgets of second frame
        self.fr_second = Frame(self.top,background= BACKGROUND,borderwidth=2,highlightthickness=1)
        self.fr_second.grid(row=0,column=0,columnspan=2,ipadx=50,sticky="w",padx=20,pady=10)

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
        self.lbl_auto_collection.grid(row=1,column=0,sticky=(W),pady = 10)

        #read the collections of each database for option widget
        collection_names = self.read_collection_name()
        collection_names.insert(0,"Select")
        self.var_collection = StringVar(self.top)
        self.var_collection.set(collection_names[0])
        self.op_collection = apply(OptionMenu,(self.fr_second,self.var_collection) + tuple(collection_names))
        self.op_collection.grid(row=1,column=1,sticky=(E,W))

        self.btnGraph = Button(self.fr_second,text="Generate Graph",command=self.genGraph)
        self.btnGraph.grid(row=2,column=1,sticky=(W,N),rowspan=2,pady=10)

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

    def genGraph(self):
        self.db = self.var_database.get()
        self.coll = self.var_collection.get()

        db = GraphDatabase("http://localhost:7474", username="neo4j", password="sagar123")
        conn = pymongo.MongoClient("localhost:27017")
        db1 = conn[str(self.db)]
        coll = db1[str(self.coll)]
        docs = coll.find({"text":{"$regex":"^RT"}}).limit(3)
        i = 1
        user = db.labels.create("User")
        for doc in docs:

            try:
                actual_user = doc['user_name']
                text = doc['text']
                text_list = text.split(":")
                retweet_User = text_list[0]
                retweet_User_id = retweet_User[4:]

                u1 = db.nodes.create(name=actual_user)
                user.add(u1)
                u2 = db.nodes.create(name=retweet_User_id)
                user.add(u2)
                u1.relationships.create("Retweets",u2)

                temp_text =  str(i) + str(doc['user_name']) + " Retweets " + str(retweet_User_id)
                print temp_text
                writeCalculations(self.text,temp_text,False,None)
                i += 1
            except Exception as e:
                print "-"*30


