import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon
from PyQt5 import uic

#load both ui file
UI_file_1 = 'form1.ui' #path
Ui_Form1, main_1 = uic.loadUiType(UI_file_1)

UI_file_2 = 'form2.ui'
Ui_Form2, main_2 = uic.loadUiType(UI_file_2)

class Main_one(main_1, Ui_Form1):
    def __init__(self):
        super(main_1,self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.change)

    def change(self):
        self.changePage = Main_two()
        self.changePage.show()
        self.close()

class Main_two(main_2, Ui_Form2):
    def __init__(self):
        super(main_2, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.change)

    def change(self):
        self.changePage = Main_one()
        self.changePage.show()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Main_one()
    window.show()
    sys.exit(app.exec_())
