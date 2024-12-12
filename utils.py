import re

NUMBER_OR_DOT = re.compile(r'^[0-9.]$')

def isNumberOrDot(string: str):
    return bool(NUMBER_OR_DOT.search(string))

def isEmpty(string: str):
    return len(string) == 0

def isValidNumber(string: str):
    try:
        float(string)
        return True
    except:
        return False