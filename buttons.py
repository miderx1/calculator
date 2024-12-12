from PySide6.QtWidgets import QPushButton, QGridLayout
from PySide6.QtCore import Slot
from variables import MEDIUM_FONT_SIZE
from utils import isNumberOrDot, isEmpty, isValidNumber
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from display import Display
    from info import Info

class Button(QPushButton):
    def __init__(self,*args,**kwargs):
        super().__init__(*args, **kwargs)
        self.configStyle()

    def configStyle(self):
        font = self.font()
        font.setPixelSize(MEDIUM_FONT_SIZE)
        self.setFont(font)
        self.setMinimumSize(75, 75)

class ButtonGrid(QGridLayout):
    def __init__(self, display: 'Display',info: 'Info', *args,**kwargs):
        super().__init__(*args,**kwargs)

        self._gridMask = [
        ['C', '◀', '^', '/'],
        ['7', '8', '9', '*'],
        ['4', '5', '6', '-'],
        ['1', '2', '3', '+'],
        ['',  '0', '.', '='],
        ]
        self.display = display
        self.info = info
        self._equation = ''
        self._equationInitial = 'Sua conta'
        self.equation = self._equationInitial
        self._left = None
        self._right = None
        self._op = None
        self._makeGrid()

    @property
    def equation(self):
        return self._equation
    
    @equation.setter
    def equation(self,value):
        self._equation = value
        self.info.setText(value)
    
    def _makeGrid(self):
        for rowIndex, row in enumerate(self._gridMask):
            for columnIndex, buttonText in enumerate(row):
                button = Button(buttonText)

                if not isNumberOrDot(buttonText):
                        button.setProperty('cssClass','specialButton')
                        self._configSpecialButton(button)
                        

                if buttonText == '0':
                    self.addWidget(button,rowIndex,columnIndex-1,1,2)
                elif isEmpty(buttonText):
                    continue
                else:
                    self.addWidget(button,rowIndex,columnIndex)

                slot = self._makeSlot(self._insertButtonTextToDisplay,button)
                button.clicked.connect(button,slot)

    def _connectButtonClicked(self,button:Button,slot):
        button.clicked.connect(slot)

    def _configSpecialButton(self,button:Button):
        text = button.text()

        if text == 'C':
            self._connectButtonClicked(button,self._clear)
        
        if text in '+-/*':
            slot = self._makeSlot(self._operatorClicked,button)
            self._connectButtonClicked(button,slot)

    def _makeSlot(self,func,*args,**kwargs):
        @Slot(bool)
        def realSlot():
            func(*args,**kwargs)
        return realSlot
    
    def _insertButtonTextToDisplay(self,button:Button):
        buttonText = button.text()
        newDisplayText = self.display.text() + buttonText

        if isValidNumber(newDisplayText):
            self.display.insert(buttonText)
        
    def _clear(self):
        print('Clear ativado')
        self.display.clear()

    def _operatorClicked(self,button:Button ):
        buttonText = button.text()
        displayText = self.display.text()
        self.display.clear()

        if not isValidNumber(displayText) and self._left is None:
            print('Não é válido')
            return
        
        if self._left is None:
            self._left = float(displayText)
        self._op = buttonText
        
        self.info.setText(f'{self._left} {self._op} ??')
