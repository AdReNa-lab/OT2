from __future__ import absolute_import

import os, re
import tkinter
import tkinter.font as font
from notebooktoall.transform import transform_notebook
from pprint import pprint

from opentrons.simulate import simulate

from Vesynta_Tech.Utilities.use_tk_inter import Use_Tkinter
#Use star imports to import all possible OpenTrons2 modules. The relevant __init__.py has a defined __all__ statement.
from Vesynta_Tech.OpenTrons2 import *

############################################################

ignore_list = ['from __future__ import absolute_import',
               'import numpy as np',
               'from opentrons import types']
remove_list = ['from Vesynta_Tech.OpenTrons2 import building_blocks as bb',
               'from Vesynta_Tech.OpenTrons2 import calculate_uncertainties as calcunc',
               'from Vesynta_Tech.OpenTrons2 import meniscus_tracking as mt',
               'from Vesynta_Tech.OpenTrons2 import custom_pipetting as cusp']
cleanup_list = ['bb.', 'calcunc.', 'mt.', 'cusp.'] 

############################################################
class SelectOT2_Params:
    def __init__(self, root):
        self.filename = None
        self.labware_dir = None
        self.root = root
        self.root.title("Vesynta Ltd.")
        
        self.b1_label = tkinter.Label(self.root, text = "\n\tSelect Protocol File for Debugging\t\n", state = "active")
        self.b1_label['font'] = font.Font(family="Helvetica", size=12, weight=font.BOLD, slant=font.ITALIC)
        self.b1_label.grid(row = 0, column = 0, columnspan = 3)
        
        self.button2a = tkinter.Button(self.root, text = "IPython Notebook", command = self.opt1_select, state = "active")
        self.button2a['font'] = font.Font(family="Helvetica", size=10, weight=font.BOLD, slant=font.ITALIC)
        self.button2a.grid(row = 1, column = 0, columnspan = 1)
        self.b2a_label = tkinter.Label(self.root, text = "'.ipynb'", state = "active")
        self.b2a_label.grid(row = 2, column = 0, columnspan = 1)
        
        self.button2b = tkinter.Button(self.root, text = "Python File", command = self.opt2_select, state = "active")
        self.button2b['font'] = font.Font(family="Helvetica", size=10, weight=font.BOLD, slant=font.ITALIC)
        self.button2b.grid(row = 1, column = 2, columnspan = 1)
        self.b2b_label = tkinter.Label(self.root, text = "'.py'", state = "active")
        self.b2b_label.grid(row = 2, column = 2, columnspan = 1)
        
        self.button3 = tkinter.Button(self.root, text = "Cancel", command = self.onclosingroot, state = "active")
        self.button3['font'] = font.Font(family="Helvetica", size=10, weight=font.BOLD, slant=font.ITALIC)
        self.button3.grid(row = 3, column = 1, columnspan = 1)
        self.root.protocol("WM_DELETE_WINDOW", self.onclosingroot)
        self.root.lift()
        self.root.attributes('-topmost',True)
        self.root.after_idle(self.root.attributes,'-topmost',False)
        self.root.mainloop()
    def onclosingroot(self):
        self.root.destroy()
        print("\nWindow closed during selection!\n")
    def opt1_select(self):
        self.root.withdraw()
        self.filename = Use_Tkinter(message = "Select IPython Notebook to be debugged", file_type = [("IPython Notebook", "*.ipynb"),("All Files", "*.*")]).open_file()
        self.root.destroy()
        if self.filename == "" or self.filename == None:
            print("\nNo file selected!\n")
            self.labware_dir = None
        else:
            self.select_labware_dir(tkinter.Tk())
    def opt2_select(self):
        self.root.withdraw()
        self.filename = Use_Tkinter(message = "Select Python File to be debugged", file_type = [("Python File", "*.py"),("All Files", "*.*")]).open_file()
        self.root.destroy()
        if self.filename == "" or self.filename == None:
            print("\nNo file selected!\n")
            self.labware_dir = None
        else:
            self.select_labware_dir(tkinter.Tk())
    
    def select_labware_dir(self, root2):
        self.root2 = root2
        self.root2.title("Vesynta Ltd.")
        
        self.b4_label = tkinter.Label(self.root2, text = "\n\tSelect folder containing custom labware definitions\t\n", state = "active")
        self.b4_label['font'] = font.Font(family="Helvetica", size=12, weight=font.BOLD, slant=font.ITALIC)
        self.b4_label.grid(row = 0, column = 0, columnspan = 3)
        
        self.button5a = tkinter.Button(self.root2, text = "Select Folder", command = self.opt3_select, state = "active")
        self.button5a['font'] = font.Font(family="Helvetica", size=10, weight=font.BOLD, slant=font.ITALIC)
        self.button5a.grid(row = 1, column = 0, columnspan = 1)
        self.b5a_label = tkinter.Label(self.root2, text = "Folder must contain '.json' files", state = "active")
        self.b5a_label.grid(row = 2, column = 0, columnspan = 1)
        
        self.button5b = tkinter.Button(self.root2, text = "Not using custom labware functions", command = self.opt4_select, state = "active")
        self.button5b['font'] = font.Font(family="Helvetica", size=10, weight=font.BOLD, slant=font.ITALIC)
        self.button5b.grid(row = 1, column = 2, columnspan = 1)
        self.b5b_label = tkinter.Label(self.root2, text = "__", state = "active")
        self.b5b_label.grid(row = 2, column = 2, columnspan = 1)
        
        self.button6 = tkinter.Button(self.root2, text = "Cancel", command = self.onclosingroot2, state = "active")
        self.button6['font'] = font.Font(family="Helvetica", size=10, weight=font.BOLD, slant=font.ITALIC)
        self.button6.grid(row = 3, column = 1, columnspan = 1)
        self.root2.protocol("WM_DELETE_WINDOW", self.onclosingroot2)
        self.root2.lift()
        self.root2.attributes('-topmost',True)
        self.root2.after_idle(self.root2.attributes,'-topmost',False)
        self.root2.mainloop()
    def onclosingroot2(self):
        self.root2.destroy()
        print("\nWindow closed during selection!\n")
    def opt3_select(self):
        self.root2.withdraw()
        self.labware_dir = Use_Tkinter(message = "Enter the folder containing custom labware JSON definitions").ask_directory()
        self.root2.destroy()
        if self.labware_dir == "" or self.labware_dir == None:
            print("\nNo folder selected!\n")
    def opt4_select(self):
        self.root2.withdraw()        
        self.root2.destroy()
        print("\nCustom labware functions not used.\n")
    def results(self):
        return (self.filename, self.labware_dir)
############################################################
class Protocol_Simulator:
    def __init__(self, notebook_path=None, custom_labware_directory=None):
        self.notebook_path = notebook_path
        self.custom_labware_directory = custom_labware_directory
        if self.notebook_path == None or self.custom_labware_directory == None:
            self.notebook_path, self.custom_labware_directory = SelectOT2_Params(tkinter.Tk()).results()
        
        if self.notebook_path == None:
            print("\nProtocol file is required for protocol simulation...\n")
        else:
            print("\nSelected Protocol:", self.notebook_path)
            # check notebook file type
            if os.path.splitext(self.notebook_path)[1] == ".ipynb":
                self.script_path = os.path.splitext(self.notebook_path)[0] + '.py'
                self.auto_conversion()
            elif os.path.splitext(self.notebook_path)[1] == ".py":
                self.script_path = self.notebook_path
            else:
                print("\nProtocol File Type not Recognised! Please select '.py' or '.ipynb' files...\n")
            if self.custom_labware_directory == None:
                print("\nCustom labware functions not used for protocol simulation...\n")
                with open(self.script_path, 'r') as file:
                    self.run_log = simulate(protocol_file=file)
            else:
                print("\nSelected Labware definitions folder:", self.custom_labware_directory, "\n")
                with open(self.script_path, 'r') as file:
                    self.run_log = simulate(protocol_file=file, custom_labware_paths = [self.custom_labware_directory])                
    def auto_conversion(self):
        if os.path.exists(self.script_path):
            print('\nRemoving previous .py script...')
            os.remove(self.script_path)
        print('Generating new .py version...')
        
        # Transform_notebook saves the converted file in the current working directory. This needs to be temporarily changed
        # to the directory of notebook_path for conversion.
        original_cwd = os.getcwd()
        os.chdir(os.path.split(self.notebook_path)[0]+"/")
        transform_notebook(ipynb_file=self.notebook_path, export_list=['py'])
        os.chdir(original_cwd)
        
        # Run auto_compiler to compile all Vesynta_Tech modules into one single protocol.py file
        # along with the protocol itself. 
        auto_compiler(self.script_path)
        
        #Check the conversion worked
        if os.path.exists(self.script_path):
            print(os.path.split(self.notebook_path)[1], 'successfully converted to', os.path.split(self.script_path)[1])
            print()
        else:
            raise ValueError('The <.py> file was not found')
    def results(self):
        return (self.notebook_path, self.custom_labware_directory, self.run_log)
############################################################

def auto_compiler(file):
    # Open the autoconverted protocol.py file to find all the Vesynta_Tech modules imported
    module_list = []
    with open(file, 'r') as file_reader:
        for line in file_reader:
            if "Vesynta_Tech.OpenTrons2" in line and "import" in line:
                line = line.rstrip()
                if line.strip('# ') not in module_list:
                    module_list.append(line)
    # Find the the abspath of the modules                
    abspath = os.path.dirname(building_blocks.__file__)
    file_reader.close()
    # Overwrite the protocol.py eliminating any references to Vesynta_Tech modules.    
    with open(file, 'r') as file_reader:
        lines = file_reader.readlines()
    file_reader.close()   
    with open(file, 'w') as outfile:
        for line in lines:
            if line.rstrip() != "" and line.rstrip() not in remove_list and line[0] != "#":
                outfile.write(line)
        outfile.write("\n")
        # Then open each Vesynta_Tech module and copy it into the protocol.py
        if len(module_list) > 0:
            for module in module_list:
                searcher = 'import (.*) as'
                result = re.search(searcher, module)
                module_path = os.path.join(abspath, result.group(1)+".py")
                with open(module_path, 'r') as module_reader:
                    for line1 in module_reader:
                        if line1.rstrip() not in ignore_list and line1.rstrip() not in remove_list:
                            outfile.write(line1)
                    outfile.write("\n")
    outfile.close()
           
    # Finally cleanup the entire protocol.py removing cross-references such as bb. or mt. or cusp. or calcunc.
    if len(module_list) > 0:
        for chk in cleanup_list:
            with open(file, 'r') as file_reader:
                lines1 = file_reader.readlines()
            file_reader.close()
            with open(file, 'w') as outfile1:
                for line in lines1:
                    if chk in line.rstrip():
                        outfile1.write(line.replace(chk,''))
                    else:
                        outfile1.write(line)
            outfile1.close()
############################################################

def print_logs(log, display_type='basic'):
    
    if display_type=='basic':
        for entry in log[0]:
            print(entry['payload']['text'])
    elif display_type=='more': # Additional elements shown
        for entry in log[0]:
            print(entry['payload']['text'])
            try:
                print('\t', 'Location: ', entry['payload']['location'])
            except:
                print('\t No location in "payload" dictionary')
            try:
                print('\t', 'Instrument: ', entry['payload']['instrument'])
            except:
                print('\t No instrument in "payload" dictionary')
            print()
    elif display_type=='full': # Full output
        pprint(log)
    else:
        print('Argument given for display_type not recognised')

############################################################
#Code starts here                       
if __name__ == "__main__":
    notebook_path, custom_labware_directory, run_log = Protocol_Simulator(None, None).results()
    print_logs(run_log)
############################################################
