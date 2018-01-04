from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit,
        QInputDialog, QApplication,QDialog,QListWidget,QHBoxLayout,QListWidgetItem, QGridLayout)
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtWidgets import *
import os,sys


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

class Example(QWidget):

    def __init__(self,wi,he):
        super().__init__()
        self.wi=wi
        self.he=he

        self.initUI()


    def initUI(self):

        self.btn = QPushButton('Add_files', self)
        self.btn.move(20, 20)
        self.btn.clicked.connect(self.show_me)

        self.setGeometry(300, 300, 290, 150)
        self.setWindowTitle('Input dialog')
        self.show()

    def show_me(self):
        d=File_dialog(self.wi,self.he)
        d.exec_()


class File_dialog(QDialog):
#class File_dialog(QDialog):
    def __init__(self,wi,he,parent=None):
        super(File_dialog,self).__init__(parent)
        self.initUI(wi,he)

    def initUI(self,wi,he):
        #tati=QDialog()
        #tati.resize(wi,he)
        #btn = QPushButton("First Button",tati)
        self.btn = QPushButton("First Button",self)
        self.btn.move(wi-100,0)

        #btn1 = QPushButton("second Button",tati)
        self.btn1 = QPushButton("second Button",self)
        x=100
        print(wi-100,he-x)
        self.btn1.move(wi-130,he-x)
        self.btn1.clicked.connect(self.tati1)

        lw=int(.2*wi)
        print(lw)
        l1w=wi-lw
        print(l1w)
        #listWidget = QListWidget(tati)
        self.listWidget = QListWidget(self)
        #listWidget1 = QListWidget(tati)
        self.listWidget.resize(lw,he-200)
        #listWidget1.resize(l1w,he-200)
        self.listWidget.move(0,50)
        #listWidget1.move(lw,50)
        for i in dirts:
            temp_item = QListWidgetItem(i)
            temp_item.setBackground(QColor('#7fc97f'))
            self.listWidget.addItem(temp_item)
        self.listWidget.addItems(files)
        #listWidget1.addItems(files)
        #self.table = QTableWidget(tati)
        self.table = QTableWidget(self)
        self.table.horizontalHeader().setVisible(False)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        self.table.setRowCount(40)
        self.table.setColumnCount(3)
        cw=int(.7*l1w)
        cw1=int(.14*l1w)
        cw2=int(.14*l1w)
        self.table.setColumnWidth(0,cw)
        self.table.setColumnWidth(1,cw1)
        self.table.setColumnWidth(2,cw2)
        self.table.setItem(0,0,QTableWidgetItem("Name"))
        self.table.setItem(0,1,QTableWidgetItem("Size"))
        self.table.setItem(0,2,QTableWidgetItem("Modified"))
        self.table.resize(l1w,he-200)
        self.table.move(lw,50)
        self.table.setShowGrid(False)

        sys.exit(self.exec_())


    def tati1(self):
        print("helo")


if __name__ == '__main__':

    app = QApplication(sys.argv)
    screen_resolution = app.desktop().screenGeometry()
    width, height = screen_resolution.width(), screen_resolution.height()
    print(width)
    print(height)
    #ex = Example(width,height)
    ex=File_dialog(width,height)
    sys.exit(app.exec_())
