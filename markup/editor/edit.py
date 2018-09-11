'''
The following module is the main editting workspace of the editor

'''

from Tkinter import *
import time

import tkFileDialog
import tkMessageBox
from tkColorChooser import askcolor



class TestApp(Text, object):
    
    def __init__(self, parent = None, *args, **kwargs):
        self.parent = parent
        super(TestApp, self).__init__(parent, *args, **kwargs)
        self.sents = []
        self.bind('<Key>', self.print_contents)
        
        self.sent_index = [0]
        #bind sets the cursor position.
        

    def print_contents(self, key):
        contents = self.get(1.0, 'end')
        try:
            if contents[-2] == '.' or contents[-2] == '?': 
                print '[%s]' % contents.replace('\n', '\\n')
                self.sent_index.append(len(contents))
                current_sent = contents[self.sent_index[-2]:self.sent_index[-1]]
                self.sents.append(contents[self.sent_index[-2]:self.sent_index[-1]])
                #sentences of the editor are collected in the object's sent variable
                
        except:
            None