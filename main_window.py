from PySide6.QtWidgets import QVBoxLayout, QWidget, QMainWindow, QMessageBox

class MainWindow(QMainWindow):
    def __init__(self, parent: QWidget | None = None, *args, **kwargs):
        super().__init__(parent,*args, **kwargs)

        self.central_widget = QWidget()
        self.vLayout = QVBoxLayout()
        self.central_widget.setLayout(self.vLayout)
        self.setCentralWidget(self.central_widget)
        self.setWindowTitle("Calculadora")

    def setFixedSize(self):
        self.adjustSize()
        self.setMaximumSize(self.width(),self.height())
    
    def addWidgetToLayout(self,widget:QWidget):
        self.vLayout.addWidget(widget)
        self.setFixedSize()
    
    def makeMsgBox(self):
        return QMessageBox(self)
