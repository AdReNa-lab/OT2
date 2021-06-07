from __future__ import absolute_import
import os

import tkinter
from tkinter import simpledialog
from tkinter.filedialog import askopenfilename, askopenfilenames, askdirectory

class Use_Tkinter:
    
    def __init__(self, message = None, file_type = [("All Files", "*.*")]):
        self.file_type = file_type # Default file_type is now "all files" as a list of tuples.
        self.message = message  
        
    def open_file(self):
        if not self.message:
            self.message = 'Select file to open'
        
        try:
            self.initiate_root(0)
        
        finally:
            self.destroy_root()
        
        if self.attr == '':
            print("\nWindow closed during selection. Valid path not recorded.\n")
            self.attr = None #Set attribute to None if no path is chosen.
        return self.attr
    
    def open_files(self):
        if not self.message:
                self.message = 'Select all files to open'
        try:
            self.initiate_root(1)
            
        # Idea: add exceptions, for example if user closes the window 
        finally:
            self.destroy_root()
        
        if self.attr == '':
            print("\nWindow closed during selection. Valid path not recorded.\n")
            self.attr = None #Set attribute to None if no path is chosen.
        return self.attr
    
    def ask_directory(self):
        if not self.message:
            self.message = 'Select desired directory'
        try:
            self.initiate_root(2)
            
        finally:
            self.destroy_root()
        
        if self.attr == '':
            print("\nWindow closed during selection. Valid path not recorded.\n")
            self.attr = None #Set attribute to None if no path is chosen.
        return self.attr
    
    def ask_name(self):
        if not self.message:
            self.message = 'Enter desired name'
        try:
            self.initiate_root(3)
            
        finally:
            self.destroy_root()
        
        if self.attr == '':
            print("\nWindow closed during selection. Valid path not recorded.\n")
            self.attr = None #Set attribute to None if no path is chosen.
        return self.attr
        
    def initiate_root(self, call):
        self.root = tkinter.Tk()
        self.root.attributes("-topmost", True)
        self.root.withdraw()
        
        # I suggest removing initialdir, because sometimes it is convenient to use the OS' cache of the last used folder. 
        # So the user doesn't have to keep navigating to the same folder every time.
        if call == 0:
            self.attr = askopenfilename(title = self.message, filetypes = self.file_type)
        elif call == 1:
            self.attr = askopenfilenames(title = self.message, filetypes = self.file_type)
        elif call == 2:
            self.attr = askdirectory(title = self.message, mustexist = True) #Check only for already existing folders.
            
        elif call == 3:
            self.attr = simpledialog.askstring("Name", self.message,
                                             parent=self.root)
            if self.attr == None:
                print("\nNo entry made.\n")
    
    def destroy_root(self):
        self.root.destroy()
        
if __name__ == "__main__":
    
    file = Use_Tkinter().open_file()
    print(file)
    print(Use_Tkinter().open_files())
    print(Use_Tkinter().ask_name())
    print(Use_Tkinter().ask_directory())
        
