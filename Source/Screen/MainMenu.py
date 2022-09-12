import pygame, Config, Utility
from pygame import *
from Elements import Button

class Load:
    
    def __init__(self, WINDOW):
    
        self.id = "Main Menu"
        self.properties = {}
        self.menuButtonList = self.loadMenuButtonList(WINDOW)
        
        self.imageDict = self.loadImageDict()
        self.drawDict = {"All": True}
        self.drawRectList = []
        
        # Moving Background #
        self.backgroundCloudX = 0
        self.backgroundTick = 0
        
    # Initialization Functions #
    def loadMenuButtonList(self, WINDOW):
    
        menuButtonList = []
        
        newGameButton = Button.Load(WINDOW, "New Game Button", ["Center", 380], {"Label": "New Game", "Font": Config.FONT_ROMAN_42, "Size": [205, "Label"], "Hover Image": "Cursor Right", "Hover Image Offset": [-30, 15], "Draw Dict String": "All"})
        newGameButton.properties["Hover Active"] = True
        menuButtonList.append(newGameButton)

        loadGameButton = Button.Load(WINDOW, "Load Game Button", ["Center", 425], {"Label": "Load Game", "Font": Config.FONT_ROMAN_42, "Size": [205, "Label"], "Default Label Color": [70, 70, 70], "Hover Image": "Cursor Right", "Hover Image Offset": [-30, 15], "Draw Dict String": "All"})
        menuButtonList.append(loadGameButton)
        
        quitButton = Button.Load(WINDOW, "Quit Button", ["Center", 470], {"Label": "Quit", "Font": Config.FONT_ROMAN_42, "Size": [205, "Label"], "Hover Image": "Cursor Right", "Hover Image Offset": [-30, 15], "Draw Dict String": "All"})
        menuButtonList.append(quitButton)
        
        return menuButtonList
     
    def loadImageDict(self):
    
        imageDict = {}
        
        imageDict["Text Box"] = {}
        imageDict["Text Box"]["Corner"] = pygame.image.load("../Image/UI/TextBoxCorner.png").convert_alpha()
        imageDict["Text Box"]["Side"] = pygame.image.load("../Image/UI/TextBoxSide.png").convert()
        
        imageDict["Hover Image"] = {}
        imageDict["Hover Image"]["Cursor Right"] = pygame.image.load("../Image/UI/CursorRight.png").convert_alpha()
        
        imageDict["Clouds"] = pygame.image.load("../Image/Backgrounds/Clouds.png").convert_alpha()
        imageDict["Main Menu Text Box"] = Utility.createTextBox(imageDict["Text Box"], {"Size": [310, 215], "Color": [29, 29, 85]})
        
        return imageDict
     
    # Main Functions #
    def draw(self, WINDOW, MOUSE, KEYBOARD, PLAYER, SCREEN_LEVEL):
    
        # Update Background Timer/Location #
        self.backgroundTick += 1
        if self.backgroundTick >= 5:
            self.backgroundTick = 0
            self.backgroundCloudX += 1
            self.drawDict["All"] = True
            
            if self.backgroundCloudX >= self.imageDict["Clouds"].get_rect().width:
                self.backgroundCloudX = 0
    
        # Draw Screen #
        if "All" in self.drawDict:
            
            # Background #
            self.drawRectList.append(WINDOW.get_rect())
            WINDOW.fill([34, 34, 42])
            WINDOW.blit(self.imageDict["Clouds"], [self.backgroundCloudX, 200])
            WINDOW.blit(self.imageDict["Clouds"], [self.backgroundCloudX - self.imageDict["Clouds"].get_rect().width, 200])
    
            # Title Labels #
            Utility.write("Triple", [40, 50], [200, 200, 200], Config.FONT_ROMAN_116, WINDOW)
            Utility.write("Triad", [441, 50], [200, 200, 200], Config.FONT_ROMAN_116, WINDOW)
            Utility.write("TCG Adventure", [456, 155], [200, 200, 200], Config.FONT_ROMAN_42, WINDOW)
            pygame.draw.line(WINDOW, [200, 200, 200], [44, 148], [228, 148], 8)
            pygame.draw.line(WINDOW, [200, 200, 200], [264, 148], [752, 148], 8)
            
            # Main Menu Buttons #
            mainMenuTextBoxSize = self.imageDict["Main Menu Text Box"].get_rect().size
            mainMenuTextBoxLoc = [int((WINDOW.get_rect().width / 2) - (mainMenuTextBoxSize[0] / 2)), 335]
            WINDOW.blit(self.imageDict["Main Menu Text Box"], mainMenuTextBoxLoc)
            Utility.write(Config.VERSION, [492, 527], [200, 200, 200], Config.FONT_ROMAN_16, WINDOW)
            
            for menuButton in self.menuButtonList:
                menuButton.draw(WINDOW, self.imageDict["Hover Image"])
    
    # Class Functions # 
    def getCurrentHoverButton(self):
    
        targetButton = None
        for menuButton in self.menuButtonList:
            if "Hover Image" in menuButton.properties and menuButton.properties["Hover Active"]:
                targetButton = menuButton
                break
                
        return targetButton
             
    def keyPress(self, SCREEN_LEVEL, PLAYER, MOUSE, KEYBOARD, KEY):
        
        # Get Data #
        currentMenuIndex = 0
        for i, menuButton in enumerate(self.menuButtonList):
            if "Hover Image" in menuButton.properties and menuButton.properties["Hover Active"]:
                currentMenuIndex = i
                break
        
        # Arrow Keys - Up/Down (Change Menu Position) #
        if KEY in ["up", "down"]:
        
            # Get Index Data #
            newIndex = currentMenuIndex
            if KEY == "up" : newIndex -= 1
            elif KEY == "down" : newIndex += 1
            if newIndex == -1 : newIndex = len(self.menuButtonList) - 1
            elif newIndex == len(self.menuButtonList) : newIndex = 0
            
            # Set Button Properties #
            self.menuButtonList[currentMenuIndex].properties["Hover Active"] = False
            if "Hover Image" in self.menuButtonList[newIndex].properties:
                self.menuButtonList[newIndex].properties["Hover Active"] = True
                
            MOUSE.hoverElement = None
            self.drawDict["All"] = True
    
    def resetActiveHoverVariables(self, RESET_SUBSCREEN=True):
    
        for menuButton in self.menuButtonList:
            if "Hover Image" in menuButton.properties:
                menuButton.properties["Hover Active"] = False
    
    def getElementList(self, SCREEN_LEVEL):
    
        return self.menuButtonList
       