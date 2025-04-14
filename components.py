import math
from variables import BIG_FONT_SIZE,MEDIUM_FONT_SIZE,SMALL_FONT_SIZE,MINIMUM_WIDTH,TEXT_MARGIN

from utils import isNumberOrDot,isValidNumber,isEmpty,convertToNumber

from main_window import MainWindow

from PySide6.QtWidgets import QPushButton,QLineEdit,QLabel, QWidget,QGridLayout
from PySide6.QtCore import Qt, Slot,Signal
from PySide6.QtGui import QKeyEvent


class Display(QLineEdit):
    eqPressed = Signal()
    delPressed = Signal()
    escPressed = Signal()
    inputPressed = Signal(str)
    operatorPressed = Signal(str)

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configStyle()
    
    def configStyle(self):
        margins = [TEXT_MARGIN for _ in range(4)]
        self.setStyleSheet(f'font-size: {BIG_FONT_SIZE}px')
        self.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.setTextMargins(*margins)
        self.setMaximumHeight(BIG_FONT_SIZE *2)
        self.setMinimumWidth(MINIMUM_WIDTH)
    
    def keyPressEvent(self, event: QKeyEvent):
        text = event.text().strip()
        key = event.key()
        KEYS = Qt.Key
        
        isEnter = key in [KEYS.Key_Enter, KEYS.Key_Return, KEYS.Key_Equal]
        isDelete = key in [KEYS.Key_Delete, KEYS.Key_Backspace, KEYS.Key_D]
        isEscape = key in [KEYS.Key_Escape, KEYS.Key_C]
        isOperator = key in [
            KEYS.Key_Plus, KEYS.Key_Minus, KEYS.Key_Asterisk, KEYS.Key_Slash, KEYS.Key_P
        ]

        if isEnter:
            self.eqPressed.emit()
            return event.ignore()
        
        if isDelete:
            self.delPressed.emit()
            return event.ignore()
        
        if isEscape:
            self.escPressed.emit()
            return event.ignore()
        
        if isEmpty(text):
            return event.ignore()
        
        if isNumberOrDot(text):
            self.inputPressed.emit(text)
            return event.ignore()
        
        if isOperator:
            if 'p' in text:
                text = '^'
            self.operatorPressed.emit(text)
            return event.ignore()
    
        
class Info(QLabel):
    def __init__(self, text: str, parent: QWidget | None= None, *args, **kwargs):
        super().__init__(text,*args, **kwargs)
        self.configStyle()

    def configStyle(self):
        self.setStyleSheet(f'font-size: {SMALL_FONT_SIZE}px')
        self.setAlignment(Qt.AlignmentFlag.AlignRight)

class Button(QPushButton):
    def __init__(self,*args, **kwargs):
        super().__init__(*args,**kwargs)
        self.configStyle()

    def configStyle(self):
        font = self.font()
        font.setPixelSize(MEDIUM_FONT_SIZE)
        self.setFont(font)

        self.setMinimumSize(75,75)

class ButtonGrid(QGridLayout):
    def __init__(self,display: Display,info: Info,window: MainWindow, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._gridMask = [
             ['C', '◀', '^', '/'],
             ['7', '8', '9', '*'],
             ['4', '5', '6', '-'],
             ['1', '2', '3', '+'],
             ['N',  '0', '.', '='],
         ]

        self.display = display
        self.info = info
        self.window = window
        self._left = None
        self._right = None
        self._op = None
        self._equation = ''
        self._equationInitialValue = 'Sua conta'
        self.equation = self._equationInitialValue


    @property
    def equation(self):
        return self._equation
    
    @equation.setter
    def equation(self,value):
        self._equation = value
        self.info.setText(value)

    def _makeGrid(self):
        self.display.eqPressed.connect(self._eq)
        self.display.escPressed.connect(self._clear)
        self.display.delPressed.connect(self._backspace)
        self.display.inputPressed.connect(self._insertToDisplay)
        self.display.operatorPressed.connect(self._operatorClicked)

        for i,row in enumerate(self._gridMask):
            for j,buttonText in enumerate(row):
                button = Button(buttonText)
                if button.text():
                    if not isNumberOrDot(buttonText):
                        button.setProperty('cssClass', 'specialButton')
                        self._configSpecialButton(button)

                    self.addWidget(button, i, j)
                    
                    slot = self._makeSlot(self._insertToDisplay,buttonText)
                    self._connectButtonClicked(slot,button)

    def _connectButtonClicked(self,slot,button):
        button.clicked.connect(slot)

    def _configSpecialButton(self,button:Button):
        text = button.text()

        if text == 'C':
            button.clicked.connect(self._clear)
        
        if text in '/*-+^':
            button.clicked.connect(
                self._makeSlot(self._operatorClicked,text)
            )

        if text == 'N':
            button.clicked.connect(self._invertNumber)

        if text == '=':
            button.clicked.connect(self._eq)
        if text == '◀':
            button.clicked.connect(self.display.backspace)


    @Slot()
    def _makeSlot(self,func,*args, **kwargs):
        @Slot(bool)
        def realSlot(_):
            func(*args,**kwargs)
        return realSlot

    @Slot()
    def _insertToDisplay(self,text):
        newDisplayText = self.display.text() + text
        
        if not isValidNumber(newDisplayText):
            return
        
        self.display.insert(text)
        self.display.setFocus()

    @Slot()
    def _clear(self):
        self.display.clear()
        self.equation = self._equationInitialValue
        self._left = None
        self._right = None
        self._op = None
        self.display.setFocus()

    @Slot()
    def _operatorClicked(self,text):
        displayText = self.display.text()

        if not isValidNumber(displayText) and self._left is None:
            self._showError('Você não digitou nada')
            return

        if self._left is None:
            self._left = convertToNumber(displayText)
        
        self.display.clear()
        self._op = text
        self.equation = f'{self._left} {self._op} ??'
        self.display.setFocus()

    @Slot()
    def _eq(self):
        displayText = self.display.text()

        if not isValidNumber(displayText):
            self._showError('Digite o segundo valor')
            return
        
        if self._op is None:
            self._showError('Escolha um operador')
            return
        
        self._right = convertToNumber(displayText)
        self.equation = f'{self._left} {self._op} {self._right}'
        result = 'Error!'
        
        try:
            if '^' in self.equation and isinstance(self._left,float | int):
                result = math.pow(self._left,self._right)
            else:
                result = eval(self.equation)

        except ZeroDivisionError:
            self._showError('Não é possível dividir por zero')
        except OverflowError:
            self._showError('Número muito grande')

        self.display.clear()
        self.info.setText(f'{self.equation} = {result}' )
        self.display.setText(str(result))
        self._left = str(result)
        self._right = None
        self.display.setFocus()

        if result == 'Error!':
            self._left = None
    
    def _invertNumber(self):
        number = self.display.text()

        if number:
            newNumber = convertToNumber(number) *-1

        self.display.setText(str(newNumber))
    
    def _backspace(self):
        self.display.backspace()
        self.display.setFocus()
    
    def _showError(self,text):
        msgBox = self.window.makeMsgBox()
        msgBox.setText(text)
        msgBox.setIcon(msgBox.Icon.Critical)
        msgBox.exec()
        self.display.setFocus()