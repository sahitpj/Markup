#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon May 28 11:23:17 2018

@author: Sahit
"""

#enrixpad is free software: you can redistribute it and/or modify

#it under the terms of the GNU General Public License as published by

#the Free Software Foundation, either version 3 of the License, or

#(at your option) any later version.





#This program is distributed in the hope that it will be useful,

#but WITHOUT ANY WARRANTY; without even the implied warranty of

#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the

#GNU General Public License for more details.





#You should have received a copy of the GNU General Public License

#along with this program. If not, see <http://www.gnu.org/licenses/>.



# -*- coding: cp1252 -*-

from Tkinter import *

import tkFileDialog
import tkMessageBox
from tkColorChooser import askcolor
import datetime
import webbrowser
from tkFileDialog import askopenfilename, asksaveasfilename





def line():
    lin = "_" * 60
    text.insert(INSERT,lin)

def date():
    data = datetime.date.today()
    text.insert(INSERT,data)

def normal():
    text.config(font = ("Arial", 10))

def bold():
    text.config(font = ("Arial", 10, "bold"))

def underline():
    text.config(font = ("Arial", 10, "underline"))

def italic():
    text.config(font = ("Arial",10,"italic"))

def font():
    (triple,color) = askcolor()
    if color:
       text.config(foreground=color)

def kill():
    root.destroy()

def about():
    pass

def opn():
    text.delete(1.0 , END)
    file = open(askopenfilename() , 'r')
    if file != '':
        txt = file.read()
        text.insert(INSERT,txt)
    else:
        pass

def save():
    filename = asksaveasfilename()
    if filename:
        alltext = text.get(1.0, END)                      
        open(filename, 'w').write(alltext) 

def copy():
    text.clipboard_clear()
    text.clipboard_append(text.selection_get()) 

def paste():
    try:
        teext = text.selection_get(selection='CLIPBOARD')
        text.insert(INSERT, teext)
    except:
        tkMessageBox.showerror("Errore","Gli appunti sono vuoti!")

def clear():
    sel = text.get(SEL_FIRST, SEL_LAST)
    text.delete(SEL_FIRST, SEL_LAST)

def clearall():
    text.delete(1.0 , END)

def background():
    (triple,color) = askcolor()
    if color:
       text.config(background=color)

def about():
    ab = Toplevel(root)
    txt = "Enrix's pad\nRealizzato da Enrix (C)\n http://www.enrixweb.altervista.org\nIl programma è rilasciato sotto licensa GPL"
    la = Label(ab,text=txt,foreground='blue')
    la.pack()

def web():
    webbrowser.open('http://www.enrixweb.altervista.org')

root = Tk()
root.title("Enrix's pad")
menu = Menu(root)



filemenu = Menu(root)
root.config(menu = menu)
menu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="Open", command=opn)
filemenu.add_command(label="Save", command=save)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=kill)



modmenu = Menu(root)
menu.add_cascade(label="modmenu",menu = modmenu)
modmenu.add_command(label="Copy", command = copy)
modmenu.add_command(label="Paste", command=paste)
modmenu.add_separator()
modmenu.add_command(label = "Clear", command = clear)
modmenu.add_command(label = "Clear All", command = clearall)


insmenu = Menu(root)
menu.add_cascade(label="insmenu",menu= insmenu)
insmenu.add_command(label="Date",command=date)
insmenu.add_command(label="Line",command=line)

formatmenu = Menu(menu)
menu.add_cascade(label="Format",menu = formatmenu)
formatmenu.add_cascade(label="Font", command = font)
formatmenu.add_separator()
formatmenu.add_radiobutton(label='Normal',command=normal)
formatmenu.add_radiobutton(label='Bold',command=bold)
formatmenu.add_radiobutton(label='Underline',command=underline)
formatmenu.add_radiobutton(label='Italic',command=italic)

persomenu = Menu(root)
menu.add_cascade(label="Personalizza",menu=persomenu)
persomenu.add_command(label="Background", command=background)

                 

helpmenu = Menu(menu)
menu.add_cascade(label="?", menu=helpmenu)
helpmenu.add_command(label="About", command=about)
helpmenu.add_command(label="Web", command = web)
text = Text(root, height=30, width=60, font = ("Arial", 10))




scroll = Scrollbar(root, command=text.yview)
scroll.config(command=text.yview)                  
text.config(yscrollcommand=scroll.set)           
scroll.pack(side=RIGHT, fill=Y)
text.pack()


root.resizable(0,0)
root.mainloop()