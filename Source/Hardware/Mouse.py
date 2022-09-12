import pygame, Utility
from pygame import *

class Load:

    def __init__(self):

        self.x = 0
        self.y = 0
        self.oldX = 0
        self.oldY = 0
        
        self.clickElement = None
        self.hoverElement = None
        self.hoverSubscreen = None
        
        self.properties = {}
        
    def update(self, SCREEN, SCREEN_LEVEL, PROPERTIES={}):
        
        # Get Hover Object Data #
        oldHoverElement = self.hoverElement
        oldHoverSubscreen = self.hoverSubscreen
        self.hoverElement = None
        self.hoverSubscreen = None
        
        # Update Mouse Hover Elements #
        for element in SCREEN.getElementList(SCREEN_LEVEL):
            if "Subscreen" in element.properties:
                if Utility.rectRectCollide([self.x, self.y], [element.rect.left, element.rect.top], [element.rect.width, element.rect.height]):
                    self.hoverSubscreen = element
               
            elif element.collideShape == "Rectangle":
                mouseLoc = [self.x, self.y]
                if "Use Offset" in element.properties and "Offset" in PROPERTIES:
                    mouseLoc[0] += PROPERTIES["Offset"][0]
                    mouseLoc[1] += PROPERTIES["Offset"][1]
                if Utility.rectRectCollide(mouseLoc, [element.rect.left, element.rect.top], [element.rect.width, element.rect.height]):
                    self.hoverElement = element
                
        # Update Hover Elements #
        if self.hoverElement != oldHoverElement or self.hoverSubscreen != oldHoverSubscreen:
            
            # Reset Active Hover Variables #
            if self.hoverElement != None:
                resetProperties = True
                if "No Hover-Stick" in self.hoverElement.properties:
                    resetProperties = False
                SCREEN.resetActiveHoverVariables(resetProperties)
            elif oldHoverElement != None and "No Hover-Stick" in oldHoverElement.properties:
                SCREEN.resetActiveHoverVariables(False)
            
            # Update Button Hover Images #
            if self.hoverElement != None and "Hover Image" in self.hoverElement.properties:
                self.hoverElement.properties["Hover Active"] = True
            if self.hoverElement != None and oldHoverElement != None and "Hover Image" in oldHoverElement.properties:
                oldHoverElement.properties["Hover Active"] = False
                
            # Update Draw Dict String #
            targetElement = self.hoverElement
            if oldHoverElement != None : targetElement = oldHoverElement
            if targetElement != None and "Draw Dict String" in targetElement.properties:
                updateDrawDictString = targetElement.properties["Draw Dict String"]
                SCREEN.drawDict[updateDrawDictString] = True
                
        if "Deck Name Area Hover Timer" in SCREEN.properties and self.hoverSubscreen == None:
            SCREEN.properties["Deck Name Area Hover Timer"] = None
            SCREEN.drawDict["All"] = True
                
    def updatePosition(self):
        
        self.oldX = self.x
        self.oldY = self.y
        self.x, self.y = pygame.mouse.get_pos()
            