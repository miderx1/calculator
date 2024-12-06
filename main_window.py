from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout

class MainWindow(QMainWindow):
    def __init__(self, parent: QWidget | None = None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.central_widget = QWidget()
        self.v_layout = QVBoxLayout()

        self.central_widget.setLayout(self.v_layout)
        self.setCentralWidget(self.central_widget)
        self.setWindowTitle('Calculadora')
    
    def adjustFixedSize(self):
        self.adjustSize()
        self.setMaximumSize(self.width(),self.height())

    def addVlayoutWidget(self,widget: QWidget):
        self.v_layout.addWidget(widget)
