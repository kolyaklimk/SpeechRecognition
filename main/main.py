import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from window import Ui_MainWindow

app = QApplication(sys.argv)
mainWindow = QMainWindow()

ui = Ui_MainWindow()
ui.setupUi(mainWindow)

mainWindow.show()
sys.exit(app.exec())