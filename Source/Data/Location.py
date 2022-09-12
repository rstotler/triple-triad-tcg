import pygame, random, Config, Utility
from pygame import *

class Load:

    def __init__(self, LOCATION):
    
        self.backgroundID = None
    
        if LOCATION in ["Zozo", "Jidoor", "S. Figaro", "Nikeah", "Tzen", "Vector", "Albrook", "Maranda"]:
            self.backgroundID = "Town_1"
    
        elif LOCATION in ["Kohlingen", "Mobliz", "Thamasa"]:
            self.backgroundID = "Town_2"
        
        elif LOCATION in ["Narshe"]:
            self.backgroundID = "Town_3"
            
        elif LOCATION in ["Cabin", "House C."]:
            self.backgroundID = "House_1"
            
        elif LOCATION in ["House A.", "House B."]:
            self.backgroundID = "House_2"
            
        elif LOCATION in ["Figaro"]:
            self.backgroundID = "Castle_1"
            
        elif LOCATION in ["Doma Castle"]:
            self.backgroundID = "Castle_2"
            
        elif LOCATION in ["Opera House"]:
            self.backgroundID = "Opera"
            
        elif LOCATION in ["Hideout"]:
            self.backgroundID = "Cave"
            