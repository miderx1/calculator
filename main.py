
import sys
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QLabel
from main_window import MainWindow
from variables import ICON_PATH
import ctypes

if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = MainWindow()

    label = QLabel('Meu texto')
    label.setStyleSheet('font-size: 50px')

    icon = QIcon(str(ICON_PATH))
    window.setWindowIcon(icon)

    window.addVlayoutWidget(label)
    window.adjustFixedSize()
    window.show()
    app.exec()
