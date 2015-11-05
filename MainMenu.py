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


if __name__ == '__main__':
    Application()
