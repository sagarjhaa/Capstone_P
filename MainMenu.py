__author__ = 'sjha1'

try:
    import tkinter as tk  # for python 3
except:
    #import Tkinter as tk  # for python 2
    from Tkinter import *
    import ttk as ttk
    import tkMessageBox
    import tkFileDialog
    import Tkconstants
    from constants import *
    import import_to_mongo
    import widgets
    import subprocess as sp
    import graphics as gp
    import nltk

#CONSTANTS FOR GLOBAL USE
ROOT = None
NB = None


class Application:
    def __init__(self):
        global ROOT

        self.root = Tk()
        ROOT = self.root

        self.root.title("Social Network Visulization")
        self.root.geometry('%dx%d+%d+%d' % (WIDTH,HEIGHT,0,0))
        self.createUI()
        self.root.mainloop()

    def createUI(self):
        global NB

        #Divide the screen in Frames
        # We have two main Frame fr_first and fr_second
        self.fr_first = LabelFrame(self.root,text = "Controls",background=BACKGROUND,highlightcolor="red",relief=RAISED)
        self.fr_first.grid(row=0,column=0,sticky="nsew")

        self.fr_second = LabelFrame(self.root,text="Window",background=BACKGROUND,highlightcolor="red",relief=RAISED)
        self.fr_second.grid(row=0,column=1,sticky="nsew")

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=0)
        self.root.grid_columnconfigure(1, weight=6)

        #Import the data to monogdb
        self.fr_import = LabelFrame(self.fr_first,text="Import Data",background=BACKGROUND)
        self.fr_import.grid(row=0,column=0,sticky=(W,N,E),ipadx=50)

        self.btn_File = Button(self.fr_import,text="File",command = self.__readcsv)
        self.btn_File.grid(row=0,column=0,sticky=(W,E),padx=10,ipadx=10,pady=10)

        self.lb_filename = Label(self.fr_import,text="Selected File",background=BACKGROUND)
        self.lb_filename.grid(row=0,column =1,sticky=(W),padx=10,pady=10)

        self.btn_import = Button(self.fr_import,text="Database Settings",command = self.__loadcsv)
        self.btn_import.grid(row=1,column=0,sticky=(W),padx=10)

        self.lb_status = Label(self.fr_import,text="Status",background=BACKGROUND)
        self.lb_status.grid(row=1,column =1,sticky=(W),padx=10,pady=10)

        style = ttk.Style()
        style.theme_create( "mystyle", parent="alt", settings={
        "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0] } },
        "TNotebook.Tab": {
            "configure": {"padding": [50, 1], "background": "#468499" },
            "map":       {"background": [("selected", "#cc0000")] } } } )

        style.theme_use("mystyle")

        self.nb_main = ttk.Notebook(self.fr_second)
        NB = self.nb_main
        self.nb_main.pack(expand=1,fill=BOTH)

        f1 = Frame(self.nb_main)
        # self.f2 = Frame(self.nb_main)

        # self.nb_main.add(self.f2,text="Canvas")
        self.nb_main.add(f1,text="Calculation")

        self.text = Text(f1,background ="White")
        # self.canvas = Canvas(self.f2)
        # self.canvas.configure(background="black")

        self.text.pack(expand=1,fill=BOTH)

        self.scale = Scrollbar(self.text,command=self.yview)
        self.scale.pack(side="right",fill="y")

        self.text.configure(yscrollcommand=self.scale.set)

        self.fr_neo4j = LabelFrame(self.fr_first,text="Graph Database",background=BACKGROUND)
        self.fr_neo4j.grid(row=1,column=0,sticky=(W,N,E),ipadx=50,pady=20)

        self.btn_start_neo = Button (self.fr_neo4j, text = "Start Server",command=self.start_neo4j)
        self.btn_start_neo.grid(row=0,column=0,sticky=(W,E),padx=10,ipadx=10,pady=10)

        self.btn_stop_neo = Button (self.fr_neo4j, text = "Stop Server",command=self.stop_neo4j)
        self.btn_stop_neo.grid(row=0,column=1,sticky=(W,E),padx=10,ipadx=10,pady=10)

        self.btn_gen_graph = Button (self.fr_neo4j, text = "Graph Settings",command=self.gen_graph)
        self.btn_gen_graph.grid(row=2,column=0,sticky=(W,E),padx=10,ipadx=10,pady=10)



    def yview(self,*args):
        self.text.yview(*args)

    def __readcsv(self):
        """Open a csv and read in the contents"""
        #print "open csv file!"
        self.directory=tkFileDialog.askopenfilename(filetypes=[("CSV","*.csv")])

        self.lb_filename.config(text= self.directory.split("/")[-1])
        writeCalculations(self.text,"Completed reading file: " + self.directory.split("/")[-1],False,NB)

        if self.directory == "":
            return

    def __loadcsv(self):
        """Move the data to the monogdb"""
        try:
            importWindow = widgets.importWidget(self.root,self.text,self.directory)
        except:
            writeCalculations(self.text,"Please select file first",True,NB)

    def start_neo4j(self):
        self.mong = sp.Popen("mongod")
        self.serve = sp.Popen("C:\\Users\\snigd\\Downloads\\neo4j-enterprise-2.3.0\\bin\\Neo4j.bat")

    def stop_neo4j(self):
        try:
            self.mong.kill()
            self.serve.kill()
        except:
            writeCalculations(self.text,"Server is off",False,None)

    def gen_graph(self):
        import pymongo
        #from neo4jrestclient.client import GraphDatabase
        #db = GraphDatabase("http://localhost:7474", username="neo4j", password="sagar123")

        conn = pymongo.MongoClient("localhost:27017")
        db1 = conn['Elections']
        coll = db1['results']
        docs = coll.find()#({"text":{"$regex":"^RT"}})#.limit(1000)
        i = 1
        #user = db.labels.create("User")
        mylist = []
        for doc in docs:
            mylist.append(doc['text'])

        print len(mylist)
        self.datalist= mylist

        self.data_list = []
        temp = []
        for i in range(len(self.datalist)):
            temp.append(self.datalist[i])
            self.data_list.append(temp)
            temp = []

        tw=[]
        itemp  = len(self.data_list)
        for i in range(itemp):
            try:
                temp_list = ",".join(self.data_list[i])
                tw.append(temp_list)
            except Exception as e:
                print self.data_list[i]

        wlist = []
        for item in tw:
            words = item.split(" ")
            for word in words:
                wlist.append(word)

        text = nltk.Text(wlist)

        # self.inputlist = ["Donald","Hillary"]
        # text.dispersion_plot(self.inputlist)

        fdist1 = nltk.FreqDist(text)
        print fdist1.most_common(50)
        # vocab1 = fdist1.keys()
        #
        # iNum = 50
        # if len(vocab1) < iNum:
        #     iNum = len(vocab1)
        #
        # fdist1.plot(5,cumulative=True)

if __name__ == '__main__':
    Application()
