import sys
import pathlib
from pathlib import Path
import shutil
import re
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QLabel
from PyQt6 import uic

folder_path = None

def get_extensions(path): #Using pathlib to get extensions
    extension_list = []
    for child in path.iterdir(): 
        if(child.is_file() and re.sub(r"\.","",child.suffix) not in extension_list):
            extension_list.append(re.sub(r"\.","",child.suffix))
    print(f"Extensions: {extension_list}")
    organize_files(extension_list, folder_path) #organize files extension by extension

def organize_files(extension_list, path): #organize files extension by extension
    for extension in extension_list: #for loop to create a folder for each extension
        organized_directory_path = path / extension
        organized_directory_path.mkdir(exist_ok = True)
        for child in path.iterdir():
            if(re.sub(r"\.","",child.suffix) == extension):
                shutil.move(child,organized_directory_path) #moving files to their new location
    
class FolderBrowserApp(QWidget):
    def __init__(self):
        super().__init__()

        uic.loadUi("design.ui",self) #UI Load

        #DEFINING UI ELEMENTS

        self.btn_browse = self.findChild(QPushButton, "btn_browse")
        self.btn_organize = self.findChild(QPushButton, "btn_organize")
        self.lbl_status = self.findChild(QLabel,"lbl_status")

        #EVENTS

        self.btn_browse.clicked.connect(self.browse_folder)
        self.btn_organize.clicked.connect(self.organize_folder)

    #MAIN CLASS METHODS

    def browse_folder(self):
        global folder_path
        folder_path = Path(QFileDialog.getExistingDirectory(self, "Select a folder"))
        
    def organize_folder(self):
        if(folder_path == Path.cwd() or folder_path == None):
            self.lbl_status.setText("Status: You must choose a directory first!")
        else:
            if(self.lbl_status.text() != ""):
                self.lbl_status.setText("")
            print(folder_path)
            get_extensions(folder_path)

if __name__ == "__main__":
    app = QApplication(sys.argv) #App Initialization
    window = FolderBrowserApp() 
    window.show() 
    sys.exit(app.exec()) #Running until the user closes it