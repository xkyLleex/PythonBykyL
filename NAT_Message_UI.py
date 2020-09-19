# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'NAT_Message.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(390, 453)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Send_Button = QtWidgets.QPushButton(self.centralwidget)
        self.Send_Button.setGeometry(QtCore.QRect(280, 310, 101, 101))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        self.Send_Button.setFont(font)
        self.Send_Button.setAutoDefault(False)
        self.Send_Button.setDefault(False)
        self.Send_Button.setObjectName("Send_Button")
        self.LE_Address = QtWidgets.QLineEdit(self.centralwidget)
        self.LE_Address.setGeometry(QtCore.QRect(130, 310, 141, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        self.LE_Address.setFont(font)
        self.LE_Address.setObjectName("LE_Address")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 310, 131, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.LE_Text = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.LE_Text.setGeometry(QtCore.QRect(10, 340, 261, 71))
        self.LE_Text.setObjectName("LE_Text")
        self.Message_send = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.Message_send.setGeometry(QtCore.QRect(200, 30, 181, 271))
        self.Message_send.setReadOnly(True)
        self.Message_send.setObjectName("Message_send")
        self.Message_from = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.Message_from.setGeometry(QtCore.QRect(10, 30, 181, 271))
        self.Message_from.setReadOnly(True)
        self.Message_from.setObjectName("Message_from")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 0, 161, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(200, 0, 181, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 390, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.LE_Address, self.LE_Text)
        MainWindow.setTabOrder(self.LE_Text, self.Send_Button)
        MainWindow.setTabOrder(self.Send_Button, self.Message_send)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "NAT_Message"))
        self.Send_Button.setText(_translate("MainWindow", "Send\n"
"Message"))
        self.label.setText(_translate("MainWindow", "IP_Address:"))
        self.label_2.setText(_translate("MainWindow", "Message for you"))
        self.label_3.setText(_translate("MainWindow", "Message you send"))
