from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPainter, QColor, QPen
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
    def __init__(self,wi,he,parent=None):
        super(File_dialog,self).__init__(parent)
        self.initUI(wi,he)

    def initUI(self,wi,he):
        self.setFixedSize(wi,he)
        self.setWindowTitle(path)
        #layout = QHBoxLayout()
        grid = QGridLayout()
        self.listWidget = QListWidget()
        self.listWidget.setGeometry(10, 10, 19, 50)
        #self.listWidget.setSize(sizeHint())
        self.listWidget.show()

        for i in dirts:
            temp_item = QListWidgetItem(i)
            temp_item.setBackground(QColor('#7fc97f'))
            self.listWidget.addItem(temp_item)
        self.listWidget.addItems(files)

        self.btn0 = QPushButton()
        self.btn1 = QPushButton()
        self.btn2 = QPushButton()
        grid.addWidget(self.listWidget,1,0)
        grid.addWidget(self.btn2,2,0)
        #grid.addWidget(self.listWidget,1,1)
        grid.addWidget(self.btn0,0,0)
        #grid.addWidget(self.btn1,1,0)

        #layout.addWidget(self.listWidget)
        #self.setLayout(layout)
        self.setLayout(grid)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    screen_resolution = app.desktop().screenGeometry()
    width, height = screen_resolution.width(), screen_resolution.height()
    ex = Example(width,height)
    #ex=File_dialog()
    sys.exit(app.exec_())
