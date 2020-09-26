# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'form1.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form1(object):
    def setupUi(self, Form1):
        Form1.setObjectName("Form1")
        Form1.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(Form1)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(350, 370, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(380, 270, 47, 12))
        self.label.setObjectName("label")
        Form1.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Form1)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        Form1.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Form1)
        self.statusbar.setObjectName("statusbar")
        Form1.setStatusBar(self.statusbar)

        self.retranslateUi(Form1)
        QtCore.QMetaObject.connectSlotsByName(Form1)

    def retranslateUi(self, Form1):
        _translate = QtCore.QCoreApplication.translate
        Form1.setWindowTitle(_translate("Form1", "Form1"))
        self.pushButton.setText(_translate("Form1", "PushButton"))
        self.label.setText(_translate("Form1", "form1"))
