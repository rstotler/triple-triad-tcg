import pygame, Config, Utility
from pygame import *

class Load:

    def __init__(self, LABEL, LOCATION, PROPERTIES={}):
    
        self.label = LABEL
        self.location = LOCATION
        
        self.color = [200, 200, 200]
        if "Color" in PROPERTIES:
            self.color = PROPERTIES["Color"]
            
        self.font = Config.FONT_FF_54
        if "Font" in PROPERTIES:
            self.font = PROPERTIES["Font"]
            
        self.displayCharacters = 1
        self.writeSpeed = 3
        self.tick = 0
        
    def update(self):
        
        updateDataDict = {}
        if self.displayCharacters < len(self.label):
            self.tick += 1
            if self.tick >= self.writeSpeed:
                self.tick = 0
                self.displayCharacters += 1
                
                if self.label[self.displayCharacters - 1] == ' ':
                    self.displayCharacters += 1
                
                updateDataDict["Update Screen"] = True
                
        return updateDataDict
            
    def draw(self, WINDOW):
    
        drawLabel = self.label[0:self.displayCharacters]
        
        Utility.write(drawLabel, self.location, self.color, self.font, WINDOW)
        