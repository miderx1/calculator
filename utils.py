import re

NUM_OR_DOT = re.compile(r'^[0-9.]$')

def isNumberOrDot(string):
    return bool(NUM_OR_DOT.search(string))

def convertToNumber(text):
    number = float(text)

    if number.is_integer():
        number = int(number)
    
    return number

def isValidNumber(string):
    valid = False
    try:
        float(string)
        valid = True
    except ValueError:
        valid = False
    return valid

def isEmpty(string):
    return len(string) == 0