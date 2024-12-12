import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from main_window import MainWindow
from display import Display
from info import Info
from styles import setupTheme
from buttons import ButtonGrid

from variables import ICON_PATH

if __name__ == '__main__':

    app = QApplication(sys.argv)
    setupTheme(app)
    window = MainWindow()

    icon = QIcon(str(ICON_PATH))
    window.setWindowIcon(icon)

    info = Info('')
    window.addWidgetToVLayout(info)

    display = Display()
    window.addWidgetToVLayout(display)

    buttonGrid = ButtonGrid(display,info)
    window.vLayout.addLayout(buttonGrid)

    window.adjustFixedSize()
    window.show()
    app.exec()
