import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from window import Ui_MainWindow

app = QApplication(sys.argv)
mainWindow = QMainWindow()

mainWindow.setStyleSheet("QMainWindow{"
                         "background-color:#e7d8c5;"
                         "}")

ui = Ui_MainWindow()
ui.setupUi(mainWindow)

mainWindow.show()
sys.exit(app.exec())
