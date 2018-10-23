#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed May 30 13:33:34 2018

@author: Sahit
"""

from Tkinter import *
import time

import tkFileDialog
import tkMessageBox
from tkColorChooser import askcolor
import datetime
import webbrowser
from tkFileDialog import askopenfilename, asksaveasfilename

from dev import webExtracter



class TestApp(Text, object):
    def __init__(self, parent = None, *args, **kwargs):
        self.parent = parent
        super(TestApp, self).__init__(parent, *args, **kwargs)
        self.sents = []
        self.bind('<Key>', self.print_contents)
        
        self.sent_index = [0]
        
        

    def print_contents(self, key):
        contents = self.get(1.0, 'end')
        try:
            if contents[-2] == '.' or contents[-2] == '?': 
                print '[%s]' % contents.replace('\n', '\\n')
                self.sent_index.append(len(contents))
                current_sent = contents[self.sent_index[-2]:self.sent_index[-1]]
                self.sents.append(contents[self.sent_index[-2]:self.sent_index[-1]])
                
        except:
            None
            
   
    
    
class Application(Text):
    def __init__(self, master=None):
        # intiliazing super class  - must always initilize a super-class for all sub-classes
        Text.__init__(self, master)
        self.grid()
        # master is the instance of Tk()
        self.master.title("MarkUp")

        for r in range(6):
            self.master.rowconfigure(r, weight=1)    
        
        self.Frame2 = Text(master, bg='#FFFCE9')
        self.Frame2.grid(row = 3, column = 0, rowspan = 3, columnspan = 2, sticky = W+E+N+S)
        self.Frame3 = TestApp()
        self.Frame3.grid(row = 0, column = 2, rowspan = 6, columnspan = 3, sticky = W+E+N+S)
             
        self.labelText = StringVar()
        self.Frame1 = Label(master, bg='#FFFCE9', textvariable=self.labelText)
        self.Frame1.grid(row = 0, column = 0, rowspan = 3, columnspan = 2, sticky = W+E+N+S)
        
    
        
    def run(self):
        sentences = self.Frame3.sents
        mod = webExtracter()
        mod.sentence_checker(sentences[0], sentences[1:] )

    def abort(self):
        print 'process abort process'

    def update_labelText(self, text):
        self.labelText.set(text)
    
        
    def line(self):
        lin = "_" * 60
        self.Frame3.insert(INSERT,lin)
    
    
    def date(self):
        data = datetime.date.today()
        self.Frame3.insert(INSERT,data)
    
    def normal(self):
        self.Frame3.config(font = ("Arial", 10))
    
    def bold(self):
        self.Frame3.config(font = ("Arial", 10, "bold"))
    
    def underline(self):
        self.Frame3.config(font = ("Arial", 10, "underline"))
    
    def italic(self):
        self.Frame3.config(font = ("Arial",10,"italic"))
    
    def font(self):
        (triple,color) = askcolor()
        if color:
           self.Frame3.config(foreground=color)
    
    def kill(self):
        root.destroy()
    
    def about(self):
        pass
    
    def opn(self):
        self.delete(1.0 , END)
        file = open(askopenfilename() , 'r')
        if file != '':
            txt = file.read()
            self.Frame3.insert(INSERT,txt)
        else:
            pass
    
    def save(self):
        filename = asksaveasfilename()
        if filename:
            alltext = self.Frame3.get(1.0, END)                      
            open(filename, 'w').write(alltext) 
    
    def copy(self):
        self.Frame3.clipboard_clear()
        self.Frame3.clipboard_append(self.Frame3.selection_get()) 
    
    def paste(self):
        try:
            teext = self.selection_get(selection='CLIPBOARD')
            self.Frame3.insert(INSERT, teext)
        except:
            tkMessageBox.showerror("Errore","Gli appunti sono vuoti!")
    
    def clear(self):
        sel = self.Frame3.get(SEL_FIRST, SEL_LAST)
        self.Frame3.delete(SEL_FIRST, SEL_LAST)
    
    def clearall(self):
        self.Frame3.delete(1.0 , END)
    
    def background(self):
        (triple,color) = askcolor()
        if color:
           self.Frame3.config(background=color)
    
    def about(self):
        ab = Toplevel(root)
        txt = "Enrix's pad\nRealizzato da Enrix (C)\n http://www.enrixweb.altervista.org\nIl programma è rilasciato sotto licensa GPL"
        la = Label(ab,text=txt,foreground='blue')
        la.pack()
    
    def web(self):
        webbrowser.open('http://www.enrixweb.altervista.org')
              
root = Tk()
app = Application(master=root)      
app.update_labelText('typing..')
menu = Menu(root)

filemenu = Menu(root)
root.config(menu = menu)
menu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="Open", command=app.opn)
filemenu.add_command(label="Save", command=app.save)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=app.kill)

functionmenu = Menu(menu)
menu.add_cascade(label="Check", menu=functionmenu)
functionmenu.add_command(label="Run", command=app.run)
functionmenu.add_command(label="Abort", command=app.abort)




modmenu = Menu(root)
menu.add_cascade(label="Edit",menu = modmenu)
modmenu.add_command(label="Copy", command = app.copy)
modmenu.add_command(label="Paste", command=app.paste)
modmenu.add_separator()
modmenu.add_command(label = "Clear", command = app.clear)
modmenu.add_command(label = "Clear All", command = app.clearall)


insmenu = Menu(root)
menu.add_cascade(label="Insert",menu= insmenu)
insmenu.add_command(label="Date",command=app.date)
insmenu.add_command(label="Line",command=app.line)

formatmenu = Menu(menu)
menu.add_cascade(label="Format",menu = formatmenu)
formatmenu.add_cascade(label="Font", command = app.font)
formatmenu.add_separator()
formatmenu.add_radiobutton(label='Normal',command=app.normal)
formatmenu.add_radiobutton(label='Bold',command=app.bold)
formatmenu.add_radiobutton(label='Underline',command=app.underline)
formatmenu.add_radiobutton(label='Italic',command=app.italic)

persomenu = Menu(root)
menu.add_cascade(label="Personalize",menu=persomenu)
persomenu.add_command(label="Background", command=app.background)

                 

helpmenu = Menu(menu)
menu.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="About", command=app.about)
helpmenu.add_command(label="Web", command = app.web)


app.mainloop()
