import os
import sys
import numpy as np
from venv import create
from webbrowser import get
from PyQt5 import QtWidgets, uic, Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QCheckBox, QPushButton, QAbstractButton, QMessageBox, QLabel, QDialog
from PyQt5.QtCore import QDate, QDateTime, QThreadPool
from sqlalchemy import create_engine, text, String, Integer, Float, Column, Boolean, null, delete, update, select, MetaData, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import exists
from datetime import datetime

from PyQt5.QtCore import QDir, QPoint, QRect, QSize, Qt
from PyQt5.QtGui import QImage, QImageWriter, QPainter, QPen, qRgb
from PyQt5.QtWidgets import (QAction, QApplication, QColorDialog, QFileDialog,
                             QInputDialog, QMainWindow, QMenu, QMessageBox, QWidget)
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter

from networking.client import Client

path = os.path.dirname(__file__)
qtCreatorFile = "\\integrationbee.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(path+qtCreatorFile)

username = input("username: ")


class IntegrationBee(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(IntegrationBee, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.menubar.triggered.connect(self.menubarTriggered)
        self.ui.pushButton_2.clicked.connect(self.expandScribbleArea)
        self.ui.lineEdit.textChanged.connect(self.textChanged)
        self.ui.pushButton.clicked.connect(self.pushButton)
        self.text = ""

        self.client = Client("172.16.10.196:8000", username)

        self.client.signals.message.connect(self.callback)

        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" %
              self.threadpool.maxThreadCount())
        self.threadpool.start(self.client)

    def callback(self, username, msg):
        print(username, msg)
        QMessageBox.about(self, username, msg)

    def textChanged(self, text):
        self.text = text

    def checkAnswer(self) -> bool:
        pass

    def pushButton(self):
        self.client.send(self.text)

    def penColor(self):
        newColor = QColorDialog.getColor(self.ui.ScribbleArea.penColor())
        if newColor.isValid():
            self.ui.ScribbleArea.setPenColor(newColor)

    def penWidth(self):
        newWidth, ok = QInputDialog.getInt(self, "Scribble",
                                           "Select pen width:", self.ui.ScribbleArea.penWidth(), 1, 50, 1)
        if ok:
            self.ui.ScribbleArea.setPenWidth(newWidth)

    def expandScribbleArea(self):
        path = os.path.dirname(__file__)
        self.dialog = uic.loadUi(path+"\\expandedScribbleArea.ui")
        self.dialog.show()

    def menubarTriggered(self, trigger):
        if trigger.text() == 'Pen color':
            self.penColor()
        if trigger.text() == 'Pen width':
            self.penWidth()
        if trigger.text() == 'Clear all':
            self.ui.ScribbleArea.clearImage()


app = QApplication(sys.argv)
window = IntegrationBee()
window.show()
app.exec()
