#!/usr/bin/python3
import sys
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QPlainTextEdit
from PyQt5 import QtGui
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.uic import loadUi
from uuid import uuid1

class LicenseValidation(QDialog):
    def __init__(self):
        super().__init__()
        loadUi('Main Login.ui',self)
        self.MachIdCopy.setText(str(uuid1()))
        self.NextPage.setEnabled(False)
        pixmap = QPixmap('chatboxlogo.jpg')
        self.Chatbox.setGeometry(QtCore.QRect(80,0,500, 175))
        self.Chatbox.setPixmap(pixmap)
        self.setWindowTitle('Licensing Page')
        self.ConfirmButton.clicked.connect(self.on_license_clicked)
    @pyqtSlot()
    def on_license_clicked(self):
        self.Status.setFont(QtGui.QFont('SansSerif', 16))
        self.Status.setText("Status: Valid")
        self.MachIdCopy.setReadOnly(True)
        self.NextPage.setEnabled(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = LicenseValidation()
    widget.show()
    sys.exit(app.exec_())