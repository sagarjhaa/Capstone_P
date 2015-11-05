from Tkinter import *

root = Tk()
t1 = Text(root, height=20, width=40)
t1.pack(side='left')
t2 = Text(root, height=20, width=40)
t2.pack(side='left')

# add some text to scroll
f = open(__file__, 'r')
text = f.read()
f.close()
t1.insert('end', text)
t2.insert('end', text)

def yview(*args):

    t1.yview(*args)
    t2.yview(*args)

sb = Scrollbar(root, command=yview)
sb.pack(side='right', fill='y')

t1.configure(yscrollcommand=sb.set)
t2.configure(yscrollcommand=sb.set)

# slave = {t1: t2, t2: t1}
# for t in (t1, t2):
#     def down(event):
#         print "Down"
#         root.tk.call('tk::TextSetCursor', slave[event.widget],
#                 root.tk.call('tk::TextUpDownLine', event.widget, 1))
#     t.bind('<Down>', down, add=True)
#     def up(event):
#         print "Up"
#         root.tk.call('tk::TextSetCursor', slave[event.widget],
#                 root.tk.call('tk::TextUpDownLine', event.widget, -1))
#     t.bind('<Up>', up, add=True)

root.mainloop()