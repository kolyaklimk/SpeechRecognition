# Imports
# Qt modules for UI
import time
# Threading module
from threading import Thread

# Google Speech Recognition module
import speech_recognition as sr
from PyQt6 import QtCore, QtWidgets

# pyttsx3 module for text-to-voice transition
import pyttsx3 as ptsx


class Ui_MainWindow(object):
    r = sr.Recognizer()
    check = True

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(400, 560)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(10, 10, 380, 340))
        self.textBrowser.setObjectName("textBrowser")

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(140, 400, 121, 41))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.pushButton_click)

        self.pushButton1 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton1.setGeometry(QtCore.QRect(140, 360, 121, 41))
        self.pushButton1.setObjectName("pushButton1")
        self.pushButton1.clicked.connect(self.pushButton1_click)

        self.cleartext = QtWidgets.QPushButton(self.centralwidget)
        self.cleartext.setGeometry(QtCore.QRect(140, 480, 121, 41))
        self.cleartext.setObjectName("cleartext")
        self.cleartext.clicked.connect(self.textBrowser.clear)

        self.ttv = QtWidgets.QPushButton(self.centralwidget)
        self.ttv.setGeometry(QtCore.QRect(140, 440, 121, 41))
        self.ttv.setObjectName("texttovoice")
        self.ttv.clicked.connect(self.ttv_click)

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
        MainWindow.setWindowTitle("MainWindow")
        self.pushButton.setText(_translate("MainWindow", "Начать запись"))
        self.pushButton1.setText(_translate("MainWindow", "Выбрать файл"))
        self.cleartext.setText(_translate("MainWindow", "Очистить"))
        self.ttv.setText(_translate("MainWindow", "Озвучить"))

    def ttv_click(self):
        tts = ptsx.init('sapi5')
        rate = tts.getProperty('rate')  # Скорость произношения
        tts.setProperty('rate', rate - 40)

        volume = tts.getProperty('volume')  # Громкость голоса
        tts.setProperty('volume', volume + 0.9)

        voices = tts.getProperty('voices')

        # Задать голос по умолчанию
        tts.setProperty('voice', 'ru-RU')

        # Попробовать установить предпочтительный голос
        for voice in voices:
            if voice.name == 'Anna':
                tts.setProperty('voice', voice.id)

        tts.say(self.textBrowser.toPlainText())
        tts.runAndWait()

    def pushButton1_click(self):
        self.hideOrShowButton(0)
        Thread(target=self.changeButton1).start()
        Thread(target=self.fileRecognition(self.centralwidget)).start()

    def changeButton1(self):
        while self.check:
            for i in range(1, 4):
                if not self.check:
                    break
                self.pushButton1.setText("Обработка аудио" + '.' * i)
                time.sleep(0.3)
        self.hideOrShowButton(1)
        self.pushButton1.setText("Выбрать файл")
        self.check = True

    def fileRecognition(self, MainWindow):
        filename = QtWidgets.QFileDialog.getOpenFileName(QtWidgets.QWidget(MainWindow), "Open file", "~/Desktop",
                                                         "wav-files(*.wav)")[0]
        file = sr.AudioFile(filename)
        try:
            with file as source:
                data = self.r.listen(source=source)
                try:
                    text = self.r.recognize_google(data, language='ru-RU').lower()
                    self.textBrowser.append(text)
                except Exception:
                    pass
        except Exception:
            pass
        self.check = False

    def pushButton_click(self):
        self.hideOrShowButton(0)
        Thread(target=self.changeButton).start()
        Thread(target=self.micro).start()

    def changeButton(self):
        while self.check:
            for i in range(1, 4):
                if not self.check:
                    break
                self.pushButton.setText("Идёт запись" + '.' * i)
                time.sleep(0.3)
        self.hideOrShowButton(1)
        self.pushButton.setText("Начать запись")
        self.check = True

    def micro(self):
        try:
            with sr.Microphone() as mic:
                self.r.pause_threshold = 0.5
                self.r.adjust_for_ambient_noise(source=mic, duration=0.5)
                data = self.r.listen(source=mic)
                try:
                    text = self.r.recognize_google(audio_data=data, language='ru-RU').lower()
                    self.textBrowser.append(text)
                except Exception:
                    pass
        except Exception:
            pass
        self.check = False

    def hideOrShowButton(self, x):
        if x:
            self.pushButton.setEnabled(True)
            self.pushButton1.setEnabled(True)
            self.ttv.setEnabled(True)
            self.cleartext.setEnabled(True)
        else:
            self.pushButton.setEnabled(False)
            self.pushButton1.setEnabled(False)
            self.ttv.setEnabled(False)
            self.cleartext.setEnabled(False)
