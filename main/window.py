from PyQt6 import QtCore, QtGui, QtWidgets
import speech_recognition as sr
from threading import Thread
import time


class Ui_MainWindow(object):
    r = sr.Recognizer()
    checkMicro = True

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(400, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(10, 10, 381, 251))
        self.textBrowser.setObjectName("textBrowser")

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(140, 400, 121, 41))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.pushButton_click)

        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(120, 460, 161, 22))
        self.comboBox.setObjectName("comboBox")


        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 400, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "начать запись"))

    def pushButton_click(self):
        Thread(target=self.changeButton).start()
        Thread(target=self.micro).start()

    def changeButton(self):
        self.pushButton.setEnabled(0)
        while self.checkMicro:
            for i in range(1, 4):
                if not self.checkMicro:
                    break
                self.pushButton.setText("идёт запись" + '.' * i)
                time.sleep(0.3)
        self.pushButton.setEnabled(1)
        self.pushButton.setText("начать запись")
        self.checkMicro = True

    def micro(self):
        with sr.Microphone() as mic:
            self.r.adjust_for_ambient_noise(source=mic, duration=0.5)
            data = self.r.listen(source=mic)
            try:
                text = self.r.recognize_google(audio_data=data, language='ru-RU').lower()
                self.textBrowser.append(text)
            except Exception:
                self.textBrowser.append('ошибка')

        self.checkMicro = False
