# Imports
# Qt modules for UI
import time
from PyQt6 import QtCore, QtWidgets
# Threading module
from threading import Thread

# Google Speech Recognition module
import speech_recognition as sr

# pyttsx3 module for text-to-voice transition
import pyttsx3 as ptsx


class Ui_MainWindow(object):
    recognizer = sr.Recognizer()
    check = True
    errorCheck = False

    def setupUi(self, MainWindow):
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        MainWindow.setWindowTitle("Speech Recognition")
        MainWindow.resize(400, 540)

        MainWindow.setCentralWidget(self.centralwidget)
        MainWindow.setFixedSize(MainWindow.width(), MainWindow.height())
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        styleButtons = "QPushButton {" \
                       "    color: white;" \
                       "    background-color: #322a27;" \
                       "    font: bold 16px;" \
                       "    border-radius: 10;" \
                       "}" \
                       "QPushButton:hover {" \
                       "    color: #322a27;" \
                       "    background-color: #b28a66;" \
                       "    border-radius: 10;" \
                       "}" \
                       "QPushButton:disabled {" \
                       "background-color: #b28a66;" \
                       "}"

        styleWindow = "QTextBrowser {" \
                      "    color: #322a27;" \
                      "    background-color: white;" \
                      "    font: 14px;" \
                      "    border-radius: 10;" \
                      "}"
        errorStyleWindow = "QTextBrowser {" \
                           "    color: #322a27;" \
                           "    background-color: #e7d8c5;" \
                           "    font: bold 16px;" \
                           "    border-radius: 10;" \
                           "}"

        self.mainText = QtWidgets.QTextBrowser(self.centralwidget)
        self.mainText.setGeometry(QtCore.QRect(10, 10, 380, 340))
        self.mainText.setStyleSheet(styleWindow)

        self.errorText = QtWidgets.QTextBrowser(self.centralwidget)
        self.errorText.setGeometry(QtCore.QRect(60, 60, 270, 230))
        self.errorText.setStyleSheet(errorStyleWindow)

        self.errorButton = QtWidgets.QPushButton(self.centralwidget)
        self.errorButton.setGeometry(QtCore.QRect(180, 240, 40, 40))
        self.errorButton.setStyleSheet(styleButtons)
        self.errorButton.setText("OK")
        self.errorButton.clicked.connect(self.hideError)
        self.errorButton.clicked.connect(self.errorText.clear)

        self.speechButton = QtWidgets.QPushButton(self.centralwidget)
        self.speechButton.setGeometry(QtCore.QRect(10, 360, 185, 80))
        self.speechButton.setStyleSheet(styleButtons)
        self.speechButton.setText("START RECORDING")
        self.speechButton.clicked.connect(self.speechButton_click)

        self.fileButton = QtWidgets.QPushButton(self.centralwidget)
        self.fileButton.setGeometry(QtCore.QRect(205, 360, 185, 80))
        self.fileButton.setStyleSheet(styleButtons)
        self.fileButton.setText("SELECT A FILE")
        self.fileButton.clicked.connect(self.fileButton_click)

        self.voiceButton = QtWidgets.QPushButton(self.centralwidget)
        self.voiceButton.setGeometry(QtCore.QRect(10, 450, 185, 80))
        self.voiceButton.setText("LISTEN")
        self.voiceButton.setStyleSheet(styleButtons)
        self.voiceButton.clicked.connect(self.voiceButton_click)

        self.clearTextButton = QtWidgets.QPushButton(self.centralwidget)
        self.clearTextButton.setGeometry(QtCore.QRect(205, 450, 185, 80))
        self.clearTextButton.setStyleSheet(styleButtons)
        self.clearTextButton.setText("CLEAR")
        self.clearTextButton.clicked.connect(self.mainText.clear)

        self.hideError()

    def voiceButton_click(self):
        self.hideOrShowButtons(0)
        Thread(target=self.changeVoiceButton).start()
        Thread(target=self.textToVoice).start()

    def changeVoiceButton(self):
        while self.check:
            for i in range(1, 4):
                if not self.check:
                    break
                self.voiceButton.setText("LISTENING" + '.' * i)
                time.sleep(0.3)
        self.hideOrShowButtons(1)
        self.voiceButton.setText("LISTEN")
        self.check = True

    def textToVoice(self):
        ttv = ptsx.init()
        ttv.setProperty("rate", 150)
        ttv.setProperty("volume", 1)
        ttv.setProperty('voice', 'ru')
        ttv.say(self.mainText.toPlainText())
        ttv.runAndWait()
        self.check = False

    def fileButton_click(self):
        self.hideOrShowButtons(0)
        Thread(target=self.changeFileButton).start()
        Thread(target=self.fileSpeechRecognition(self.centralwidget)).start()

    def changeFileButton(self):
        while self.check:
            for i in range(1, 4):
                if not self.check:
                    break
                self.fileButton.setText("AUDIO PROCESSING" + '.' * i)
                time.sleep(0.3)
        self.fileButton.setText("SELECT A FILE")
        if self.errorCheck:
            self.showError(2)
        else:
            self.hideOrShowButtons(1)
        self.check = True

    def fileSpeechRecognition(self, MainWindow):
        filename = QtWidgets.QFileDialog.getOpenFileName(QtWidgets.QWidget(MainWindow), "Open file", "~/Desktop",
                                                         "wav-files(*.wav)")[0]
        file = sr.AudioFile(filename)
        try:
            with file as source:
                data = self.recognizer.listen(source=source)
                try:
                    text = self.recognizer.recognize_google(data, language='ru-RU').lower()
                    self.mainText.append(text)
                except Exception:
                    self.errorCheck = True
        except Exception:
            self.errorCheck = True
        self.check = False

    def speechButton_click(self):
        self.hideOrShowButtons(0)
        Thread(target=self.changeSpeechButton).start()
        Thread(target=self.microphoneSpeechRecognition).start()

    def changeSpeechButton(self):
        while self.check:
            for i in range(1, 4):
                if not self.check:
                    break
                self.speechButton.setText("RECORDING" + '.' * i)
                time.sleep(0.3)
        self.speechButton.setText("START RECORDING")
        if self.errorCheck:
            self.showError(1)
        else:
            self.hideOrShowButtons(1)
        self.check = True

    def microphoneSpeechRecognition(self):
        try:
            with sr.Microphone() as mic:
                self.recognizer.pause_threshold = 0.5
                data = self.recognizer.listen(source=mic)
                try:
                    text = self.recognizer.recognize_google(audio_data=data, language='ru-RU').lower()
                    self.mainText.append(text)
                except Exception:
                    self.errorCheck = True
        except Exception:
            self.errorCheck = True
        self.check = False

    def hideOrShowButtons(self, x):
        if x:
            self.speechButton.setEnabled(True)
            self.fileButton.setEnabled(True)
            self.voiceButton.setEnabled(True)
            self.clearTextButton.setEnabled(True)
        else:
            self.speechButton.setEnabled(False)
            self.fileButton.setEnabled(False)
            self.voiceButton.setEnabled(False)
            self.clearTextButton.setEnabled(False)

    def hideError(self):
        self.errorButton.hide()
        self.errorText.hide()
        self.hideOrShowButtons(1)

    def showError(self, x):
        self.errorButton.show()
        self.errorText.show()
        self.hideOrShowButtons(0)
        self.errorCheck = False
        self.errorText.update()
        self.errorText.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        if x == 1:
            self.errorText.append('ERROR\n'
                                  '\nPOSSIBLE REASONS:'
                                  '\nNO INTERNET CONNECTION'
                                  '\nMICROPHONE NOT CONNECTED'
                                  '\nMICROPHONE IS DEFECTIVE'
                                  '\nMISPRONUNCIATION')
        if x == 2:
            self.errorText.append('ERROR\n'
                                  '\nPOSSIBLE REASONS:'
                                  '\nNO INTERNET CONNECTION'
                                  '\nWRONG FILE SELECTED'
                                  '\nWORDS IN WAV FILE NOT FOUND')
