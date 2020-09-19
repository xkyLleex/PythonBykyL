import sys,socket,re
from PyQt5.QtWidgets import QMainWindow,QApplication,QMessageBox,QShortcut
from PyQt5.QtGui import QKeySequence
from NAT_Message_UI import Ui_MainWindow
from PyQt5.QtCore import QThread,pyqtSignal

#socket.setdefaulttimeout(1)
'''
用QThread是因為如果用threading會與Qt的線程或訊號對不上
雖然當時有錯誤但還是能正常運行，錯誤代碼為：
QObject::connect: Cannot queue arguments of type 'QTextCursor'
(Make sure 'QTextCursor' is registered using qRegisterMetaType().)
後來就用QThread跟pyqtSignal來向UI發送訊號
'''
class recv_thread(QThread):
    emit_text = pyqtSignal(str)

    def __init__(self, parent=None):
        super(recv_thread, self).__init__(parent)

    def run(self):
        net_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        net_socket.bind(("0.0.0.0",2345))
        net_socket.listen(1)
        print('start listen recv')
        while True:
            try:
                client,address = net_socket.accept()
                data = client.recv(1024)
                text = data.decode()
                print("{}:{}".format(address,text))
                self.emit_text.emit("{}:{}".format(address,text))
                client.close()
            except socket.timeout:
                pass
            except Exception as e:
                print("error_server",str(e))

class MainWindow(QMainWindow, Ui_MainWindow): 

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        
        self.Send_Button.clicked.connect(self.send)
        self.enter = QShortcut(QKeySequence("Enter"),self)
        self.enter.activated.connect(self.send)
        self.enter_return = QShortcut(QKeySequence("Return"),self)
        self.enter_return.activated.connect(self.send)

        self.statusbar.showMessage('Your IP Address:{}'.format(socket.gethostbyname(socket.gethostname())))
        '''原執行緒，雖然會出現上面開始講的錯誤，但還是可以正常運行...
        recv = threading.Thread(target=self.recv)
        recv.start()
        '''
        self.recv_text_thread = recv_thread()
        self.recv_text_thread.start()
        self.recv_text_thread.emit_text.connect(self.recv_text)

    def closeEvent(self, event):
        wantquit = QMessageBox.question(
            self,"System","是否關閉程式？",QMessageBox.Yes|QMessageBox.No,QMessageBox.No)
        if wantquit == QMessageBox.Yes:
            self.recv_text_thread.quit()
            event.accept() #accept close event
        else:
            event.ignore() #ignore close event
            
    def send(self):
        try:
            net_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            address = self.LE_Address.text()
            if re.match('^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$',address) != None:
                net_socket.connect((address,2345))
                text = self.LE_Text.toPlainText()
                net_socket.send(text.encode())
                net_socket.close()
                self.Message_send.insertPlainText('{}:{}\n'.format(address,text))
                self.LE_Text.clear()
            else:
                print('unknow address')
        except Exception as e:
            print('Error:',str(e))

    def recv_text(self,data):
        self.Message_from.insertPlainText('{}\n'.format(data))

    '''原執行緒代碼，雖會出現一開始講的錯誤，但還是可以正常運行...
    def recv(self):
        net_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        net_socket.bind(("0.0.0.0",2345))
        net_socket.listen(1)
        print('start listen recv')
        while True and not self.closecheck:
            try:
                client,address = net_socket.accept()
                data = client.recv(1024)
                text = data.decode()
                print("{}:{}".format(address,text))
                self.Message_from.insertPlainText('{}:{}\n'.format(address,text))
                QtCore.QMetaType.type
                client.close()
            except socket.timeout:
                pass
            except Exception as e:
                print("error_server",str(e))
    '''

###--- Main ---###
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())