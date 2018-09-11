'''
This is the UI of the editor.

The following UI is constructed with 3 windows.
1. The console, which will give information about the current running function
2. The main editting area
3. An arbitary window
'''
from Tkinter import *
import time
import tkFileDialog
import tkMessageBox
from tkColorChooser import askcolor
import datetime
import webbrowser
from tkFileDialog import askopenfilename, asksaveasfilename
import threading
from multiprocessing import Queue, Pool, Process
from extracter import webExtracter


class Application(Text):
    def __init__(self, master=None):
        # intiliazing super class  - must always initilize a super-class for all sub-classes
        Text.__init__(self, master)
        self.grid()
        self.interval = 1
        # master is the instance of Tk()
        self.master.title("PyWord")
        self.labelText = 'baby'

        for r in range(6):
            self.master.rowconfigure(r, weight=1)    
        
        self.Frame2 = Text(master, bg='#FFFCE9')
        self.Frame2.grid(row = 3, column = 0, rowspan = 3, columnspan = 2, sticky = W+E+N+S)
        #Adds the edit window to the UI
        self.Frame3 = TestApp()
        self.Frame3.grid(row = 0, column = 2, rowspan = 6, columnspan = 3, sticky = W+E+N+S)
             
        self.labelText_var = StringVar()
        self.Frame1 = Label(master, bg='#FFFCE9', textvariable=self.labelText_var)
        self.Frame1.grid(row = 0, column = 0, rowspan = 3, columnspan = 2, sticky = W+E+N+S)
        
    # Console functionality functions
    def update_labelText(self, text):
        self.labelText_var.set(text)


    def run(self):   
        while True:
            print 'running...'
            text = self.labelText
            print text
            self.update_labelText(text)
            time.sleep(1)
            
    # main fact checking functions
    def checker(self, webExtracter):
        match_queries = {}
        self.labelText = 'checker is running...'
        for sentence in self.Frame3.sents:
            if sentence not in match_queries.keys():
                q = Queue()
                l = webExtracter()
                #picks up webextracter function from the argument
                p = Process(target=l.sentence_checker, args=(sentence, self.Frame3.sents, q))
                p.start()
                p.join()
                match = q.get()
                match_queries[sentence] = match          
                self.labelText = 'match percentage of '+ sentence+ ' is  50%'
            
    # basic menu functionality
  
    def testing_the_text(self):
        self.labelText = 'hello'
        
        
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
        txt = "PyWord, still under development, and yet alive!"
        la = Label(ab,text=txt,foreground='blue')
        la.pack()
    
    def web(self):
        #webbrowser.open('')