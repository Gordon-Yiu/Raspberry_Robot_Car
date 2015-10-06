# -*- coding: utf-8 -*-
from Tkinter import *
 
class GUIDemo(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.createWidgets()
 
    def createWidgets(self):
        self.inputText = Label(self)
        self.inputText["text"] = "Input:"
        self.inputText.grid(row=0, column=0)
        self.inputField = Entry(self)
        self.inputField["width"] = 50
        self.inputField.grid(row=0, column=1, columnspan=6)
 
        self.outputText = Label(self)
        self.outputText["text"] = "Output:"
        self.outputText.grid(row=1, column=0)
        self.outputField = Entry(self)
        self.outputField["width"] = 50
        self.outputField.grid(row=1, column=1, columnspan=6)
         
        self.new = Button(self)
        self.new["text"] = "New"
        self.new.grid(row=2, column=0)
        self.new["command"] =  self.newMethod
        self.load = Button(self)
        self.load["text"] = "Load"
        self.load.grid(row=2, column=1)
        self.load["command"] =  self.loadMethod
        self.save = Button(self)
        self.save["text"] = "Save"
        self.save.grid(row=2, column=2)
        self.save["command"] =  self.saveMethod
        self.encode = Button(self)
        self.encode["text"] = "Encode"
        self.encode.grid(row=2, column=3)
        self.encode["command"] =  self.encodeMethod
        self.decode = Button(self)
        self.decode["text"] = "Decode"
        self.decode.grid(row=2, column=4)
        self.decode["command"] =  self.decodeMethod
        self.clear = Button(self)
        self.clear["text"] = "Clear"
        self.clear.grid(row=2, column=5)
        self.clear["command"] =  self.clearMethod
        self.copy = Button(self)
        self.copy["text"] = "Copy"
        self.copy.grid(row=2, column=6)
        self.copy["command"] =  self.copyMethod
 
        self.displayText = Label(self)
        self.displayText["text"] = "something happened"
        self.displayText.grid(row=3, column=0, columnspan=7)
     
    def newMethod(self):
        self.displayText["text"] = "This is New button."
 
    def loadMethod(self):
        self.displayText["text"] = "This is Load button."
 
    def saveMethod(self):
        self.displayText["text"] = "This is Save button."
 
    def encodeMethod(self):
        self.displayText["text"] = "This is Encode button."
 
    def decodeMethod(self):
       self.displayText["text"] = "This is Decode button."
 
    def clearMethod(self):
       self.displayText["text"] = "This is Clear button."
 
    def copyMethod(self):
       self.displayText["text"] = "This is Copy button."
       self.inputField["text"]="copy button"
 
if __name__ == '__main__':
    root = Tk()
    app = GUIDemo(master=root)
    app.mainloop()
 
# 《程式語言教學誌》的範例程式
# http://pydoing.blogspot.com/
# 檔名：tkdemo3.py
# 功能：示範 Python 程式
# 作者：張凱慶
# 時間：西元 2012 年 12 月
