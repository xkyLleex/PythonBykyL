# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'form2.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form2(object):
    def setupUi(self, Form2):
        Form2.setObjectName("Form2")
        Form2.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(Form2)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(300, 360, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(320, 250, 47, 12))
        self.label.setObjectName("label")
        Form2.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Form2)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        Form2.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Form2)
        self.statusbar.setObjectName("statusbar")
        Form2.setStatusBar(self.statusbar)

        self.retranslateUi(Form2)
        QtCore.QMetaObject.connectSlotsByName(Form2)

    def retranslateUi(self, Form2):
        _translate = QtCore.QCoreApplication.translate
        Form2.setWindowTitle(_translate("Form2", "Form2"))
        self.pushButton.setText(_translate("Form2", "PushButton"))
        self.label.setText(_translate("Form2", "form2"))
