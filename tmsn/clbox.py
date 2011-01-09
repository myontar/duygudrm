from Tkinter import *

class ColoredListbox(Listbox):
    def __init__(self, master=None, cnf={}, **kw):
        Listbox.__init__(self, master, cnf, **kw)
        self.listcolors()

    def listcolors(self):
        self.var1 = -1
        self.var2 = -2
        while self.var1<=(self.size()-3):
            self.var1 = self.var1+2
            self.itemconfig(self.var1, bg="white")
        while self.var2<=(self.size()-3):
            self.var2 = self.var2+2
            self.itemconfig(self.var2, bg="light blue")
        self.apply_it = self.after(1000, func=self.listcolors)

