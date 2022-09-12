import pygame, Config, Utility
from pygame import *

class Load:

    def __init__(self, WINDOW, ID, LOCATION, PROPERTIES):
        
        self.id = ID
        self.collideShape = "Rectangle"
        self.properties = PROPERTIES
        self.properties["Hover Active"] = False
        
        if "Selectable" in PROPERTIES:
            self.properties["Selected"] = False
    
        # Font & Label Size #
        self.font = Config.FONT_ROMAN_16
        if "Font" in PROPERTIES:
            self.font = PROPERTIES["Font"]
        labelSize = [0, 0]
        if "Label" in PROPERTIES:
            labelSize = self.font.size(PROPERTIES["Label"])
    
        # Surface Size #
        surfaceSize = [100, 100]
        if "Size" in PROPERTIES:
            if isinstance(PROPERTIES["Size"][0], int) : surfaceSize[0] = PROPERTIES["Size"][0]
            elif isinstance(PROPERTIES["Size"][0], str) and PROPERTIES["Size"][0] == "Label" and labelSize[0] != 0:
                surfaceSize[0] = labelSize[0]
            if isinstance(PROPERTIES["Size"][1], int) : surfaceSize[1] = PROPERTIES["Size"][1]
            elif isinstance(PROPERTIES["Size"][1], str) and PROPERTIES["Size"][1] == "Label" and labelSize[1] != 0:
                surfaceSize[1] = labelSize[1]
    
        # Surface Location #
        surfaceLocation = [0, 0]
        if isinstance(LOCATION[0], int) : surfaceLocation[0] = LOCATION[0]
        elif isinstance(LOCATION[0], str) and LOCATION[0] == "Center":
            surfaceLocation[0] = int((WINDOW.get_rect().size[0] / 2) - (surfaceSize[0] / 2))
        if isinstance(LOCATION[1], int) : surfaceLocation[1] = LOCATION[1]
        elif isinstance(LOCATION[1], str) and LOCATION[1] == "Center":
            surfaceLocation[1] = int((WINDOW.get_rect().size[1] / 2) - (surfaceSize[1] / 2))
    
        # Surface #
        self.surfaceDefault = None
        self.rect = pygame.rect.Rect(surfaceLocation, surfaceSize)
        if "Default Color" in PROPERTIES:
            self.surfaceDefault = pygame.Surface(surfaceSize)
            self.surfaceDefault.fill(PROPERTIES["Default Color"])
            if len(PROPERTIES["Default Color"]) == 4:
                self.surfaceDefault.set_alpha(PROPERTIES["Default Color"][3])
        
    def draw(self, WINDOW, HOVER_IMAGES=None, PROPERTIES={}):
    
        # Surface #
        buttonRect = self.rect
        displaySurface = self.surfaceDefault
        surfaceLoc = [self.rect.left, self.rect.top]
        if "Offset" in PROPERTIES:
            surfaceLoc[0] -= PROPERTIES["Offset"][0]
            surfaceLoc[1] -= PROPERTIES["Offset"][1]
        if displaySurface != None:
            if "Draw Rect" in self.properties:
                WINDOW.blit(displaySurface, surfaceLoc, self.properties["Draw Rect"])
            else : WINDOW.blit(displaySurface, surfaceLoc)
            
        # Image #
        if "Image" in self.properties:
            WINDOW.blit(self.properties["Image"], [self.rect.left, self.rect.top])

        # Label #
        labelColor = [200, 200, 200]
        if "Default Label Color" in self.properties:
            labelColor = self.properties["Default Label Color"]
        if "Label" in self.properties:
            labelLoc = [self.rect.left, self.rect.top]
            if "Label Offset" in self.properties:
                labelLoc = [self.rect.left + self.properties["Label Offset"][0], self.rect.top + self.properties["Label Offset"][1]]
            Utility.write(self.properties["Label"], labelLoc, labelColor, self.font, WINDOW)

        # Hover Image Properties #
        if True:
            hoverImage = None
            if "Selected" in self.properties and self.properties["Selected"] == True:
                if "Selected Image" in self.properties and self.properties["Selected Image"] in HOVER_IMAGES:
                    hoverImage = HOVER_IMAGES[self.properties["Selected Image"]]
            
            if "Hide Hover Image" not in PROPERTIES:
                if hoverImage == None and "Hover Image" in self.properties and self.properties["Hover Active"]:
                    if self.properties["Hover Image"] in HOVER_IMAGES:
                        hoverImage = HOVER_IMAGES[self.properties["Hover Image"]]
                    
            if hoverImage != None:
                hoverImageLoc = [self.rect.left, self.rect.top]
                hoverImageSize = hoverImage.get_rect().size
                if "Hover Image Offset" in self.properties:
                    totalSize = [self.rect.width, self.rect.height]
                    location = [self.rect.left, self.rect.top]
                    
                    if isinstance(self.properties["Hover Image Offset"][0], int):
                        hoverImageLoc[0] += self.properties["Hover Image Offset"][0]
                        if self.properties["Hover Image Offset"][0] < 0:
                            totalSize[0] += abs(self.properties["Hover Image Offset"][0])
                            location[0] += self.properties["Hover Image Offset"][0]
                        elif self.properties["Hover Image Offset"][0] + hoverImageSize[0] > self.rect.width:
                            totalSize[0] += (hoverImageSize[0] + self.properties["Hover Image Offset"][0]) - self.rect.width
                            if "Label Offset" in self.properties:
                                totalSize[0] += self.properties["Label Offset"][0]
                            
                    elif isinstance(self.properties["Hover Image Offset"][0], str) and self.properties["Hover Image Offset"][0] == "Center":
                        hoverImageLoc[0] += int((self.rect.width / 2) - (hoverImageSize[0] / 2))
                    
                    if isinstance(self.properties["Hover Image Offset"][1], int):
                        hoverImageLoc[1] += self.properties["Hover Image Offset"][1]
                        if self.properties["Hover Image Offset"][1] < 0:
                            totalSize[1] += abs(self.properties["Hover Image Offset"][1])
                            location[1] += self.properties["Hover Image Offset"][1]
                        elif self.properties["Hover Image Offset"][1] + hoverImageSize[1] > self.rect.height:
                            totalSize[1] += (hoverImageSize[1] + self.properties["Hover Image Offset"][1]) - self.rect.height
                            if "Label Offset" in self.properties:
                                totalSize[1] += self.properties["Label Offset"][1]
                            
                    elif isinstance(self.properties["Hover Image Offset"][1], str) and self.properties["Hover Image Offset"][1] == "Center":
                        hoverImageLoc[1] += int((self.rect.height / 2) - (hoverImageSize[1] / 2))
                    
                    buttonRect = [location[0], location[1], totalSize[0], totalSize[1]]
                
                if "Label Offset" in self.properties:
                    hoverImageLoc = [hoverImageLoc[0] + self.properties["Label Offset"][0], hoverImageLoc[1] + self.properties["Label Offset"][1]]
                WINDOW.blit(hoverImage, hoverImageLoc)
                
        return buttonRect
