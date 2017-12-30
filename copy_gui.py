from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import os,sys
from datetime import datetime
if os.name == 'nt':
    import win32api, win32con

formats=["MP3","FLAC","OGG","M4A","WMA","WAV","MP4","AAC","flv"]
formats_lower=[]
for i in formats:formats_lower.append(i.lower())

def Is_hidden(file_temp):
    if os.name== 'nt':
        attribute = win32api.GetFileAttributes(file_temp)
        return attribute & (win32con.FILE_ATTRIBUTE_HIDDEN | win32con.FILE_ATTRIBUTE_SYSTEM)
    else:
        return file_temp.startswith('.')


class ImgWidget1(QLabel):
    """
    Class used to show picture on Table Row
    """
    def __init__(self, imagePath,parent=None):
        super(ImgWidget1, self).__init__(parent)
        pic = QPixmap(imagePath)
        self.setPixmap(pic)

class File_dialog(QDialog):
    """
    Main class used for the dialog
    """
    def __init__(self,wi,he,path,parent=None):
        self.path = path
        self.stack = [self.path]
        self.cur_pos = 0
        super(File_dialog,self).__init__(parent)
        self.initUI(wi,he)

    def initUI(self,wi,he):
        self.moveBack = QPushButton(self)
        self.moveBack.resize(35,30)
        self.moveBack.setIcon(QIcon('moveBack.png'))
        self.moveBack.setIconSize(QSize(35,30))
        self.moveBack.move(.17*wi,10)
        self.moveBack.clicked.connect(self.moveBack_action)
        self.moveNext = QPushButton(self)
        self.moveNext.resize(35,30)
        self.moveNext.setIcon(QIcon('moveNext.png'))
        self.moveNext.setIconSize(QSize(35,30))
        self.moveNext.move(.17*wi+35,10)
        self.moveNext.clicked.connect(self.moveNext_action)

        self.btn = QPushButton("Select It",self)
        self.btn.resize(100,30)
        self.btn.move(wi-120,10)
        #self.btn.clicked.connect(self.select_it)
        self.btn.clicked.connect(self.select_action)

        self.btn1 = QPushButton("Open Folder",self)
        self.btn1.resize(150,30)
        self.btn1.move(wi-300,10)

        self.lineedit = QLineEdit("Search here",self)
        self.lineedit.resize(250,30)
        self.lineedit.move(wi-700,10)
        #self.lineedit.hide()
        self.helpbtn = QPushButton(self)
        self.helpbtn.resize(40,30)
        self.helpbtn.setIcon(QIcon('icon.png'))
        self.helpbtn.setIconSize(QSize(40,30))
        self.helpbtn.move(wi-445,10)
        #self.helpbtn.clicked.connect(self.lineedit.show)
        self.helpbtn.clicked.connect(self.search_update)

        self.lw=int(.15*wi)
        self.l1w=wi-self.lw
        self.listWidget = QListWidget(self)
        self.listWidget.resize(self.lw,he-150)
        self.listWidget.move(0,0)

        self.table = QTableWidget(self)
        self.table.horizontalHeader().setVisible(False)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setColumnCount(3)
        cw=int(.7*self.l1w)
        cw1=int(.14*self.l1w)
        cw2=int(.14*self.l1w)
        self.table.setColumnWidth(0,cw)
        self.table.setColumnWidth(1,cw1)
        self.table.setColumnWidth(2,cw2)
        self.show_files(False)
        self.table.resize(self.l1w,he-200)
        self.table.move(self.lw,50)
        self.table.setShowGrid(False)
        self.table.doubleClicked.connect(self.select_action)

        self.checkBox = QCheckBox("Show hidden files/folders",self)
        self.checkBox.resize(200,30)
        self.checkBox.move(wi-500,he-130)
        self.checkBox.toggled.connect(lambda:self.show_hidden(self.checkBox))

        self.cb = QComboBox(self)
        self.cb.addItem("All Supported Fomarts")
        self.cb.addItems(formats)
        self.cb.resize(200,30)
        self.cb.move(wi-250,he-130)

        self.resize(wi,he)
        sys.exit(self.exec_())

    def select_action(self):
        indexes = self.table.selectionModel().selectedRows()
        for index in (indexes):
            value=(self.table.item(self.table.currentRow(),0).text())[6:]
            #value=(self.table.item(self.table.currentRows(),0).text())[6:]
            print(value)
            if os.path.isdir(os.path.join(self.path,value)) == True:
                self.path=os.path.join(self.path,value)
                self.stack.append(self.path)
                #print(self.stack)
                self.cur_pos=self.cur_pos+1
                self.show_files(False)
                #self.btn.setEnabled(False)

    def moveBack_action(self):
        if self.cur_pos != 0:
                self.cur_pos=self.cur_pos-1
                self.path=self.stack[self.cur_pos]
                self.show_files(False)

    def moveNext_action(self):
        if  not self.cur_pos == len(self.stack)-1:
                self.cur_pos=self.cur_pos+1
                self.path=self.stack[self.cur_pos]
                self.show_files(False)

    def show_files(self,hidden):
        self.files_to_show()
        self.table.setRowCount(len(self.dirs)+len(self.files)+1)
        self.table.setItem(0,0,QTableWidgetItem("                                   Name"))
        self.table.setItem(0,1,QTableWidgetItem("      Size"))
        self.table.setItem(0,2,QTableWidgetItem("      Modified"))
        start,pos,j=1,1,1
        while start <= len(self.dirs):
            if hidden == False :
                if Is_hidden(self.dirs[start-1]) == True:
                    start=start+1
                    continue
            self.table.setItem(pos,0,QTableWidgetItem("      "+self.dirs[start-1]))
            self.table.setItem(pos,1,QTableWidgetItem("      "+self.dirs_size[start-1]))
            self.table.setItem(pos,2,QTableWidgetItem("      "+self.dirs_modi_time[start-1]))
            self.table.setCellWidget(pos, 0, ImgWidget1("folder.png"))
            pos,start=pos+1,start+1

        while j <= len(self.files):
            if hidden == False :
                if Is_hidden(self.files[j-1]) == True:
                    j=j+1
                    continue
            self.table.setItem(pos,0,QTableWidgetItem("      "+self.files[j-1]))
            self.table.setItem(pos,1,QTableWidgetItem("      "+self.files_size[j-1]))
            self.table.setItem(pos,2,QTableWidgetItem("      "+self.files_modi_time[j-1]))
            self.table.setCellWidget(pos, 0, ImgWidget1("music.png"))
            pos,j=pos+1,j+1

    def select_it(self):
        print("hello im done")

    def search_update(self):
        print(self.lineedit.text())
        self.lineedit.setText("")

    def show_hidden(self,cb):
        if cb.isChecked() == True:
            self.show_files(True)
        else:
            self.show_files(False)

    def files_to_show(self):
        self.files = []
        self.files_size = []
        self.files_modi_time = []
        self.dirs = []
        self.dirs_size = []
        self.dirs_modi_time = []

        def converter(num):
            for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
                if num < 1024.0:
                    return "%3.1f %s" % (num, x)
                num /= 1024.0

        for i in os.listdir(self.path):
            file_info = os.stat(os.path.join(self.path,i))
            date_= str((datetime.fromtimestamp(file_info.st_mtime)).date())
            if os.path.isdir(os.path.join(self.path,i)):
                self.dirs.append(i)
                self.dirs_size.append("NA")
                self.dirs_modi_time.append(date_)
            else:
                for j in formats_lower:
                    if i.endswith('.'+j) == True:
                        self.files.append(i)
                        self.files_size.append(converter(file_info.st_size))
                        self.files_modi_time.append(date_)
                        break

if __name__ == '__main__':

    app = QApplication(sys.argv)
    screen_resolution = app.desktop().screenGeometry()
    width, height = screen_resolution.width(), screen_resolution.height()
    path=os.getcwd()
    ex=File_dialog(width,height,path)
    sys.exit(app.exec_())
