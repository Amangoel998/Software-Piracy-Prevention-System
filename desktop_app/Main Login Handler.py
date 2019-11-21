#!/usr/bin/python3
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QPlainTextEdit, QMainWindow, QDesktopWidget
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.uic import loadUi
import uuid, socket, requests, hashlib
from datetime import *

# uifile_1 = 'UI/openPage.ui'
# form_1, base_1 = uic.loadUiType(uifile_1)
# super(base_1,self).__init__()
UNAME = ''
PWORD = ''

class SuccessValidation(QtWidgets.QWidget):
    def __init__(self, already=False):
        super().__init__()
        self.setupUI(already)
        self.show()
    def setupUI(self, already):
        loadUi('Activation.ui',self)
        pixmap = QPixmap('chatboxlogo.jpg')
        self.Chatbox.setGeometry(QtCore.QRect(80,0,500, 175))
        self.Chatbox.setPixmap(pixmap)
        self.setWindowTitle('Successfully Activated')
        # geometry of the main window
        qr = self.frameGeometry()

        # center point of screen
        cp = QDesktopWidget().availableGeometry().center()

        # move rectangle's center point to screen's center point
        qr.moveCenter(cp)

        # top left of rectangle becomes top left of window centering it
        self.move(qr.topLeft())
        if already:
            self.SuccessText.setText("You have already Activated")
        else:
            self.SuccessText.setText("You have Successfully Activated")
        self.StartApp.clicked.connect(self.startApp)
    def startApp(self):
        self.next = StartApp()
        self.next.show()
        self.close()

class StartApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()
        self.show()
    def setupUI(self):
        loadUi('ChatBox.ui',self)
        self.setWindowTitle('Chat Box')
        # geometry of the main window
        qr = self.frameGeometry()

        # center point of screen
        cp = QDesktopWidget().availableGeometry().center()

        # move rectangle's center point to screen's center point
        qr.moveCenter(cp)

        # top left of rectangle becomes top left of window centering it
        self.move(qr.topLeft())

class LicenseValidation(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()
        self.show

    def setupUI(self):
       
        loadUi('License Widget.ui',self)
        
        # geometry of the main window
        qr = self.frameGeometry()

        # center point of screen
        cp = QDesktopWidget().availableGeometry().center()

        # move rectangle's center point to screen's center point
        qr.moveCenter(cp)

        # top left of rectangle becomes top left of window centering it
        self.move(qr.topLeft())
        self.MachineID.setText(str(uuid.UUID(int=uuid.getnode())))
        self.StartApp.setEnabled(False)
        self.setWindowTitle('Licensing Page')
        self.MachineID.setReadOnly(True)
        self.ConfirmLicense.clicked.connect(self.checkLicense)
        self.StartApp.clicked.connect(self.startApp)

    def checkLicense(self):
        if not self.ActivationKey.text():
            alerting(self, 'Alert!',"Activation Key cannot be empty")
            return
        resp = self.complete_validation()
        if resp==1:
            self.StartApp.setEnabled(True)
            alerting(self, 'Success!',"You have Activated your License")
        else:
            alerting(self, 'Alert!',resp)
            self.close()
    
    def complete_validation(self):
        global UNAME
        global PWORD
        url = 'http://127.0.0.1:8000/api/activation-validation/'
        
        machm = self.MachineID.text().strip().lstrip().rstrip()
        keym = self.ActivationKey.text().strip().lstrip().rstrip()

        myobj = {'user': UNAME, 'password': PWORD,'auth_machine': machm,
            'Key': keym,'TimeStamp': str(datetime.now())}
        try:
            x = requests.post(url, data = myobj)
        except:
            alerting(self, "Alert!", "You must connect to Internet to Proceed")
            return
        response_message = UNAME+machm+keym+datetime.now().strftime('%M')
        hashed_message = hashlib.sha256(response_message.encode())
        if x.text[1:-1]==str(hashed_message.hexdigest()):
            return 1
        else:
            return x.text[1:-1]

    def startApp(self):
        self.next = SuccessValidation()
        self.next.show()
        self.close()

class LoginWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle('Login Page')
        loadUi('Login.ui',self)
        qr = self.frameGeometry()

        # center point of screen
        cp = QDesktopWidget().availableGeometry().center()

        # move rectangle's center point to screen's center point
        qr.moveCenter(cp)

        # top left of rectangle becomes top left of window centering it
        self.move(qr.topLeft())
        self.Login.clicked.connect(self.checkValidation)

    def checkValidation(self):
        global UNAME
        global PWORD
        UNAME = self.Username.text().strip().lstrip().rstrip()
        PWORD = self.Password.text().strip().lstrip().rstrip()
        if not UNAME or not PWORD:
            alerting(self, "Alert!", "Password and Email Required!")
            return
        coparer = self.complete_validation()
        if coparer == 1:
            self.next = LicenseValidation()
            self.next.show()
            self.close()
        elif coparer == 2:
            self.next = SuccessValidation(True)
            self.next.show()
            self.close()
        else:
            alerting(self, "Alert!", coparer)

    def complete_validation(self):
        url = 'http://127.0.0.1:8000/api/user-validation/'
        myobj = {'user': UNAME, 'password': PWORD}
        try:
            x = requests.post(url, data = myobj)
        except:
            alerting(self, "Alert!", "You must connect to Internet to Proceed")
            return
        i=0
        while i<3:
            response_message = 'You are Now Very Much Authenticated'+datetime.now().strftime('%M')
            hashed_message = hashlib.sha256(response_message.encode())
            ans_1 = hashed_message.hexdigest()

            response_message = 'You were Very Much Authenticated'+datetime.now().strftime('%M')
            hashed_message = hashlib.sha256(response_message.encode())
            ans_2 = hashed_message.hexdigest()
            if x.text[1:-1]==ans_1:
                return 1
            elif x.text[1:-1]==ans_2:
                return 2
            i+=1
        return x.text[1:-1]

def alerting(self, title, message):
    QtWidgets.QMessageBox.question(self, title,message, QtWidgets.QMessageBox.Ok,QtWidgets.QMessageBox.Ok)

def is_connected():
    try:
        socket.create_connection(("127.0.0.1", 8000))
        return True
    except OSError:
        pass
    return False

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = LoginWindow()
    widget.show()
    sys.exit(app.exec_())
