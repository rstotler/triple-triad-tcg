import pygame
from pygame import *

class Load:

    def __init__(self):

        self.shift = False
        self.backspace = False
        self.backspaceTimer = -1
        self.backspaceSpeed = 6
        
        self.inputKeyDict = {"a":"a", "b":"b", "c":"c", "d":"d", "e":"e", "f":"f", "g":"g", "h":"h", \
                             "i":"i", "j":"j", "k":"k", "l":"l", "m":"m", "n":"n", "o":"o", "p":"p", \
                             "q":"q", "r":"r", "s":"s", "t":"t", "u":"u", "v":"v", "w":"w", "x":"x", \
                             "y":"y", "z":"z", "space":" ", "1":"1", "2":"2", "3":"3", "4":"4", "5":"5", \
                             "6":"6", "7":"7", "8":"8", "9":"9", "0":"0"}
                             
        self.inputKeyShiftDict = {"a":"A", "b":"B", "c":"C", "d":"D", "e":"E", "f":"F", "g":"G", "h":"H", \
                                  "i":"I", "j":"J", "k":"K", "l":"L", "m":"M", "n":"N", "o":"O", "p":"P", \
                                  "q":"Q", "r":"R", "s":"S", "t":"T", "u":"U", "v":"V", "w":"W", "x":"X", \
                                  "y":"Y", "z":"Z", "space":" "}
