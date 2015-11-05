__author__ = 'sjha1'

import ctypes
from Tkinter import *
user32 = ctypes.windll.user32
WIDTH,HEIGHT = user32.GetSystemMetrics(0),user32.GetSystemMetrics(1)
print WIDTH,HEIGHT
canvasWidth,canvasHeight,margin_x, margin_y = WIDTH, HEIGHT,WIDTH/2,HEIGHT/2
WIDTH -= 20
HEIGHT -= 75
#canvasWidth,canvasHeight,margin_x, margin_y = WIDTH, HEIGHT,WIDTH, HEIGHT
BACKGROUND = "Grey"



def writeCalculations(widget,text,error,NB=None):
    if error:

        widget.tag_configure('error',foreground='red')
        widget.insert(END,text,'error')
        NB.select(1)
    else:
        if type(text)== dict:
            widget.insert(END,"{")
            widget.insert(END,"\n")
            textid = " "*20+"id:"+str(text['id'])
            widget.insert(END,textid)
            widget.insert(END,"\n")

            for key,value in text.items():
                if key <> "id":
                    textvalue = " "*20 + str(key) +":" + str(value)
                    widget.insert(END,textvalue)
                    widget.insert(END,"\n")
            widget.insert(END,"}")
        else:
            pass
            #widget.insert(END,text)

    widget.insert(END,"\n")