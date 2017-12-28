from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import os,sys
from datetime import datetime

path=os.getcwd()
li=os.listdir(path)

def filter(inp):
    files=[]
    dirts=[]
    for i in inp:
        temp=os.path.join(path,i)
        if os.path.isfile(temp):
            files.append(i)
        else:
            dirts.append(i)
    return files,dirts

files,dirts=filter(li)
files_size=[]
modify_time_files=[]
dirts_size=[]
modify_time_dirts=[]

def getFolderSize(folder):
    """
        This function takes too much time, will try to make it work fast
    """
    total_size = os.path.getsize(folder)
    for item in os.listdir(folder):
        itempath = os.path.join(folder, item)
        if os.path.isfile(itempath):
            total_size += os.path.getsize(itempath)
        elif os.path.isdir(itempath):
            total_size += getFolderSize(itempath)
    return total_size

def convert_bytes(num):
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0

def file_size(file_path):
    if os.path.isfile(file_path):
        file_info = os.stat(file_path)
        return convert_bytes(file_info.st_size),(datetime.fromtimestamp(file_info.st_mtime)).date()
    else:
        file_info=os.stat(file_path)
        #return convert_bytes(getFolderSize(file_path)),(datetime.fromtimestamp(file_info.st_mtime)).date()
        return "NA",(datetime.fromtimestamp(file_info.st_mtime)).date()

for i in files:
    temp1,temp2=file_size(os.path.join(path,i))
    files_size.append(str(temp1))
    modify_time_files.append(str(temp2))

for i in dirts:
    temp1,temp2=file_size(os.path.join(path,i))
    dirts_size.append(str(temp1))
    modify_time_dirts.append(str(temp2))

class ImgWidget1(QLabel):

    def __init__(self, imagePath,parent=None):
        super(ImgWidget1, self).__init__(parent)
        pic = QPixmap(imagePath)
        self.setPixmap(pic)

class File_dialog(QDialog):

    def __init__(self,wi,he,parent=None):
        super(File_dialog,self).__init__(parent)
        self.initUI(wi,he)

    def initUI(self,wi,he):
        self.moveBack = QPushButton(self)
        self.moveBack.resize(35,30)
        self.moveBack.setIcon(QIcon('moveBack.png'))
        self.moveBack.setIconSize(QSize(35,30))
        self.moveBack.move(.17*wi,10)
        self.midbtn = QPushButton(" Cur",self)
        self.midbtn.resize(60,30)
        self.midbtn.move(.17*wi+35,10)
        self.moveNext = QPushButton(self)
        self.moveNext.resize(35,30)
        self.moveNext.setIcon(QIcon('moveNext.png'))
        self.moveNext.setIconSize(QSize(35,30))
        self.moveNext.move(.17*wi+95,10)

        self.checkBox = QCheckBox("Show hidden files/folders",self)
        self.checkBox.resize(200,30)
        self.checkBox.move(wi-500,he-130)

        self.btn = QPushButton("Select It",self)
        self.btn.resize(100,30)
        self.btn.move(wi-120,10)

        self.btn1 = QPushButton("Open Folder",self)
        self.btn1.resize(150,30)
        self.btn1.move(wi-300,10)

        self.cb = QComboBox(self)
        self.cb.addItem("All Supported Fomarts")
        self.cb.addItems(["MP3","FLAC","OGG","M4A","WMA","WAV","MP4","AAC","flv"])
        self.cb.resize(200,30)
        self.cb.move(wi-250,he-130)

        self.lineedit = QLineEdit("Search here",self)
        self.lineedit.resize(150,30)
        self.lineedit.move(wi-600,10)
        #self.lineedit.hide()
        self.helpbtn = QPushButton(self)
        self.helpbtn.resize(40,30)
        self.helpbtn.setIcon(QIcon('icon.png'))
        self.helpbtn.setIconSize(QSize(40,30))
        self.helpbtn.move(wi-445,10)
        #self.helpbtn.clicked.connect(self.lineedit.show)
        self.helpbtn.clicked.connect(self.search_update)


        lw=int(.15*wi)
        l1w=wi-lw
        self.listWidget = QListWidget(self)
        self.listWidget.resize(lw,he-150)
        self.listWidget.move(0,0)

        self.table = QTableWidget(self)
        self.table.horizontalHeader().setVisible(False)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setRowCount(len(dirts)+len(files)+1)
        self.table.setColumnCount(3)
        cw=int(.7*l1w)
        cw1=int(.14*l1w)
        cw2=int(.14*l1w)
        self.table.setColumnWidth(0,cw)
        self.table.setColumnWidth(1,cw1)
        self.table.setColumnWidth(2,cw2)
        self.table.setItem(0,0,QTableWidgetItem("                                   Name"))
        self.table.setItem(0,1,QTableWidgetItem("      Size"))
        self.table.setItem(0,2,QTableWidgetItem("      Modified"))

        for i in range(1,len(dirts)+1):
            self.table.setItem(i,0,QTableWidgetItem("      "+dirts[i-1]))
            self.table.setItem(i,1,QTableWidgetItem("      "+dirts_size[i-1]))
            self.table.setItem(i,2,QTableWidgetItem("      "+modify_time_dirts[i-1]))
            self.table.setCellWidget(i, 0, ImgWidget1("folder.png"))

        j=0
        if len(dirts)==0:
            start=1
            if len(files)!=0: end=len(files)+1
            else: end=0
        else:
            start=len(dirts)+1
            if len(files)==0: end=start
            else: end=start+len(files)

        for i in range(start,end):
            self.table.setItem(i,0,QTableWidgetItem("      "+files[j]))
            self.table.setItem(i,1,QTableWidgetItem("      "+files_size[j]))
            self.table.setItem(i,2,QTableWidgetItem("      "+modify_time_files[j]))
            self.table.setCellWidget(i, 0, ImgWidget1("music.png"))
            j=j+1

        self.table.resize(l1w,he-200)
        self.table.move(lw,50)
        self.table.setShowGrid(False)

        self.resize(wi,he)
        sys.exit(self.exec_())

    def search_update(self):
        print(self.lineedit.text())
        self.lineedit.setText("")


if __name__ == '__main__':

    app = QApplication(sys.argv)
    screen_resolution = app.desktop().screenGeometry()
    width, height = screen_resolution.width(), screen_resolution.height()
    ex=File_dialog(width,height)
    sys.exit(app.exec_())
