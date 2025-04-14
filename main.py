import sys

from main_window import MainWindow
from variables import ICON_PATH

from components import Display, Info, ButtonGrid

from styles import setupTheme

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication


if __name__ == '__main__':
    app = QApplication(sys.argv)
    setupTheme(app)

    mainwindow = MainWindow()
    
    # Define o icone
    icon = QIcon(str(ICON_PATH))
    mainwindow.setWindowIcon(icon)
    app.setWindowIcon(icon)

    #Display
    info = Info('Sua conta')
    mainwindow.addWidgetToLayout(info)

    #Coloca o display
    display = Display()
    mainwindow.addWidgetToLayout(display)

    buttonGrid = ButtonGrid(display,info,mainwindow)
    mainwindow.vLayout.addLayout(buttonGrid)
    buttonGrid._makeGrid()

    mainwindow.setFixedSize()
    mainwindow.show()

    app.exec()