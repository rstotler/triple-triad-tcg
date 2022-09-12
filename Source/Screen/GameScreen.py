import pygame, random, Config, Utility
from pygame import *
from Elements import Button, DrawText, Card

class Load:
    
    def __init__(self, WINDOW, SCREEN_LEVEL):
    
        self.id = "Game Screen"
        self.properties = {}
        
        # Load Initial Properties #
        self.properties["Last Screen"] = None
        self.properties["Last Town ID"] = None
        self.properties["Deck Name Area Hover Timer"] = None
        
        self.properties["Overworld Offset"] = [0, 0]
        self.properties["Overworld Velocity"] = [0, 0]
        self.properties["Overworld Velocity Timer"] = [0, 0]
        self.properties["Max Overworld Velocity"] = 6
        self.properties["Min Portrait X"] = 170
        
        self.imageDict = self.loadImageDict()
        self.drawDict = {"All": True}
        self.drawRectList = [WINDOW.get_rect()]
        
        self.overworldButtonList = self.loadOverworldButtonList(WINDOW)
        self.sideMenuButtonList = self.loadSideMenuButtonList(WINDOW, SCREEN_LEVEL)
        self.subscreenButtonDict = self.loadSubscreenButtonDict(WINDOW)
        
        WINDOW.fill([0, 0, 0])
    
    # Initialization Functions #
    def loadSubscreenButtonDict(self, WINDOW):
    
        subscreenButtonDict = {}
    
        overworldScreenSize = self.imageDict["Overworld Screen Border"].get_rect().size
        overworldScreenButton = Button.Load(WINDOW, "Overworld Screen", [0, 0], {"Size": overworldScreenSize, "Subscreen": True})
        subscreenButtonDict["Overworld"] = overworldScreenButton
    
        minimapSize = self.imageDict["Minimap FF6"].get_rect().size
        minimapLoc = [Config.SCREEN_SIZE[0] - minimapSize[0] - Config.BORDER_INDENT, Config.BORDER_INDENT]
        overworldMinimapButton = Button.Load(WINDOW, "Overworld Minimap", minimapLoc, {"Size": minimapSize, "Subscreen": True})
        subscreenButtonDict["Minimap"] = overworldMinimapButton
        
        subscreenButtonDict["Card Collection Button List"] = []
        
        subscreenButtonDict["Deck Editor Deck Area Button"] = None
        subscreenButtonDict["Deck Editor Deck Name Area Button"] = None
        subscreenButtonDict["Deck Editor Button List"] = []
        subscreenButtonDict["Deck Editor Top Card Button List"] = []
        subscreenButtonDict["Deck Editor Bottom Card Button List"] = []
                
        return subscreenButtonDict
        
    def loadSideMenuButtonList(self, WINDOW, SCREEN_LEVEL):
    
        sideMenuButtonList = []
        sideMenuButtonSize = [145, 25]
        sideMenuButtonLabelOffset = [0, -21]
        yLoc = 225
        
        if SCREEN_LEVEL == "Town":
            travelButton = Button.Load(WINDOW, "Travel Button", [640, yLoc], {"Label": "Travel", "Font": Config.FONT_FF_54, "Size": sideMenuButtonSize, "Label Offset": sideMenuButtonLabelOffset, "Hover Image": "Cursor Right", "Hover Image Offset": [-30, 31], "No Hover-Stick": True, "Draw Dict String": "Side Screen"})
            sideMenuButtonList.append(travelButton)
            yLoc += sideMenuButtonSize[1]

            talkButton = Button.Load(WINDOW, "Talk Button", [640, yLoc], {"Label": "Talk", "Font": Config.FONT_FF_54, "Size": sideMenuButtonSize, "Label Offset": sideMenuButtonLabelOffset, "Hover Image": "Cursor Right", "Hover Image Offset": [-30, 31], "No Hover-Stick": True, "Draw Dict String": "Side Screen"})
            sideMenuButtonList.append(talkButton)
            yLoc += sideMenuButtonSize[1]

            duelButton = Button.Load(WINDOW, "Duel Button", [640, yLoc], {"Label": "Duel", "Font": Config.FONT_FF_54, "Size": sideMenuButtonSize, "Label Offset": sideMenuButtonLabelOffset, "Hover Image": "Cursor Right", "Hover Image Offset": [-30, 31], "Selectable": True, "Selected Image": "Cursor Alpha Right", "No Hover-Stick": True, "Draw Dict String": "Side Screen"})
            sideMenuButtonList.append(duelButton)
            yLoc += sideMenuButtonSize[1]
        
        cardsButton = Button.Load(WINDOW, "Cards Button", [640, yLoc], {"Label": "Cards", "Font": Config.FONT_FF_54, "Size": sideMenuButtonSize, "Label Offset": sideMenuButtonLabelOffset, "Hover Image": "Cursor Right", "Hover Image Offset": [-30, 31], "No Hover-Stick": True, "Draw Dict String": "Side Screen"})
        sideMenuButtonList.append(cardsButton)
        yLoc += sideMenuButtonSize[1]
        
        deckButton = Button.Load(WINDOW, "Decks Button", [640, yLoc], {"Label": "Decks", "Font": Config.FONT_FF_54, "Size": sideMenuButtonSize, "Label Offset": sideMenuButtonLabelOffset, "Hover Image": "Cursor Right", "Hover Image Offset": [-30, 31], "No Hover-Stick": True, "Draw Dict String": "Side Screen"})
        sideMenuButtonList.append(deckButton)
        yLoc += sideMenuButtonSize[1]
        
        if SCREEN_LEVEL in ["Card Collection", "Deck Editor"]:
            backButton = Button.Load(WINDOW, "Back Button", [640, yLoc], {"Label": "Back", "Font": Config.FONT_FF_54, "Size": sideMenuButtonSize, "Label Offset": sideMenuButtonLabelOffset, "Hover Image": "Cursor Right", "Hover Image Offset": [-30, 31], "No Hover-Stick": True, "Draw Dict String": "Side Screen"})
            sideMenuButtonList.append(backButton)
            yLoc += sideMenuButtonSize[1]
        
        return sideMenuButtonList
        
    def loadOverworldButtonList(self, WINDOW):
    
        overworldButtonList = []
        
        for townName in ["House A.", "Kohlingen", "Narshe", "Zozo", "Jidoor", "Opera House", "Figaro", "S. Figaro", \
                         "Cabin", "Hideout", "Nikeah", "House B.", "Doma Castle", "Mobliz", "Thamasa", "Tzen", \
                         "Vector", "Albrook", "House C.", "Maranda"]:
            townDrawRect = [0, 0, 100, 100]
            
            if townName == "House A." : townLocation = [495, 100]
            elif townName == "Kohlingen" : townLocation = [390, 585]
            elif townName == "Narshe" : townLocation = [1307, 490]
            elif townName == "Zozo" : townLocation = [315, 1444]
            elif townName == "Jidoor" : townLocation = [395, 2053]
            elif townName == "Opera House" : townLocation = [687, 2425]
            elif townName == "Figaro" : townLocation = [1000, 1170]
            elif townName == "S. Figaro" : townLocation = [1335, 1750]
            elif townName == "Cabin" : townLocation = [1410, 1540]
            elif townName == "Hideout" : townLocation = [1627, 985]
            elif townName == "Nikeah" : townLocation = [1848, 940]
            elif townName == "House B." : townLocation = [2611, 520]
            elif townName == "Doma Castle" : townLocation = [2465, 1300]
            elif townName == "Mobliz" : townLocation = [3485, 1800]
            elif townName == "Thamasa" : townLocation = [3965, 2010]
            elif townName == "Tzen" : townLocation = [1877, 2340]
            elif townName == "Vector" : townLocation = [1891, 2950]
            elif townName == "Albrook" : townLocation = [2180, 3213]
            elif townName == "House C." : townLocation = [2610, 3065]
            elif townName == "Maranda" : townLocation = [1020, 3587]
            
            townOverworldButton = Button.Load(WINDOW, townName + " Overworld Button", townLocation, {"Size": [townDrawRect[2], townDrawRect[3]], "Draw Dict String": "Overworld", "Use Offset": True, "Overworld Location": True, "Draw Rect": townDrawRect, "Town Name": townName})
            overworldButtonList.append(townOverworldButton)
        
        return overworldButtonList
        
    def loadImageDict(self):
    
        imageDict = {}
        
        # Default Images #
        imageDict["Text Box"] = {}
        imageDict["Text Box"]["Corner"] = pygame.image.load("../Image/UI/TextBoxCorner.png").convert_alpha()
        imageDict["Text Box"]["Side"] = pygame.image.load("../Image/UI/TextBoxSide.png").convert()
        imageDict["Text Box"]["Bubble Bottom Left"] = pygame.image.load("../Image/UI/TextBoxBubble.png").convert_alpha()
        imageDict["Text Box"]["Bubble Bottom Right"] = pygame.transform.flip(imageDict["Text Box"]["Bubble Bottom Left"], True, False)
        imageDict["Text Box"]["Bubble Top Left"] = pygame.transform.flip(imageDict["Text Box"]["Bubble Bottom Left"], False, True)
        imageDict["Text Box"]["Bubble Top Right"] = pygame.transform.flip(imageDict["Text Box"]["Bubble Bottom Right"], False, True)
        
        imageDict["Hover Image"] = {}
        imageDict["Hover Image"]["Cursor Right"] = pygame.image.load("../Image/UI/CursorRight.png").convert_alpha()
        imageDict["Hover Image"]["Cursor Alpha Right"] = pygame.image.load("../Image/UI/CursorRight.png").convert_alpha()
        imageDict["Hover Image"]["Cursor Alpha Right"].set_alpha(100)
        imageDict["Hover Image"]["Arrow Left"] = pygame.image.load("../Image/UI/Arrow_Left.png").convert_alpha()
        imageDict["Hover Image"]["Arrow Left"].fill([70, 70, 70], None, pygame.BLEND_RGB_SUB)
        imageDict["Hover Image"]["Arrow Right"] = pygame.transform.flip(imageDict["Hover Image"]["Arrow Left"], True, False)
        
        # Overworld Images #
        imageDict["Overworld FF6"] = pygame.image.load("../Image/Backgrounds/Overworld_FF6.png").convert()
        imageDict["Minimap FF6"] = pygame.image.load("../Image/Backgrounds/Map_FF6.png").convert()
        miniMapSize = imageDict["Minimap FF6"].get_rect().size
        miniMapBorderSize = [miniMapSize[0] + (Config.BORDER_INDENT * 2), miniMapSize[1] + (Config.BORDER_INDENT * 2)]
        mainScreenBorderSize = [Config.SCREEN_SIZE[0] - miniMapBorderSize[0] + 1, 446]
        imageDict["Overworld Screen Border"] = Utility.createTextBox(imageDict["Text Box"], {"Size": [mainScreenBorderSize[0], Config.SCREEN_SIZE[1]]})
        
        imageDict["Overworld Location Text Box"] = Utility.createTextBox(imageDict["Text Box"], {"Size": [218, 91], "Color": [29, 29, 85]})
        Utility.write("Cards:", [44, 30], [200, 200, 200], Config.FONT_FF_32, imageDict["Overworld Location Text Box"])
        Utility.write("Travel:", [37, 50], [200, 200, 200], Config.FONT_FF_32, imageDict["Overworld Location Text Box"])
        imageDict["Card Icon"] = pygame.image.load("../Image/UI/Card_Icon.png").convert_alpha()
        imageDict["Overworld Location Text Box"].blit(imageDict["Card Icon"], [12, 37])
            
        imageDict["Card Back Small"] = pygame.image.load("../Image/Cards/Back_Small.png").convert_alpha()
        imageDict["Underscore"] = pygame.Surface([14, 2])
        imageDict["Underscore"].fill([200, 200, 200])
        
        # Cards & Decks Screen Images #
        imageDict["Cards Screen"] = None
        imageDict["Decks Screen"] = None
        
        imageDict["Cards"] = {}
        imageDict["Cards Small"] = {}
        
        # Town Images #
        imageDict["Duel Text Box"] = None
        imageDict["Portraits"] = {}
        imageDict["Portraits"]["Girl"] = None
        
        imageDict["Town Name Text Box"] = None
        imageDict["Town Background"] = None
        imageDict["Town Top Screen Border"] = None
        imageDict["Town Bottom Screen"] = None
        imageDict["Town Bottom Screen Border"] = None
            
        # Minimap Images #
        if True:
            imageDict["Minimap Border"] = Utility.createTextBox(imageDict["Text Box"], {"Size": miniMapBorderSize})
            imageDict["Side Screen Border"] = Utility.createTextBox(imageDict["Text Box"], {"Size": [miniMapBorderSize[0], Config.SCREEN_SIZE[1] - miniMapBorderSize[1] + 1], "Color": [29, 29, 85]})
            
            # Minimap Reticle #
            overworldScreenSizeTuple = imageDict["Overworld Screen Border"].get_rect().size
            overworldScreenSize = [0, 0]
            overworldScreenSize[0] = overworldScreenSizeTuple[0] - (Config.BORDER_INDENT * 2)
            overworldScreenSize[1] = overworldScreenSizeTuple[1] - (Config.BORDER_INDENT * 2)
            overworldSize = imageDict["Overworld FF6"].get_rect().size
            
            mapReticleSize = [0, 0]
            overworldScreenPercentage = overworldScreenSize[0] / overworldSize[0]
            mapReticleSize[0] = int(overworldScreenPercentage * miniMapSize[0])
            mapReticleSize[1] = int(overworldScreenPercentage * miniMapSize[1])
            self.properties["Minimap Reticle Size"] = mapReticleSize
        
        return imageDict
        
    # Main Functions #
    def draw(self, WINDOW, MOUSE, KEYBOARD, PLAYER, SCREEN_LEVEL):
        
        # Screen Updates #
        if True:
            if SCREEN_LEVEL == "Overworld":
            
                # Update Map Velocity #
                if self.properties["Overworld Velocity"][0] != 0 or self.properties["Overworld Velocity"][1] != 0:
                    self.properties["Overworld Offset"][0] += self.properties["Overworld Velocity"][0]
                    self.properties["Overworld Offset"][1] += self.properties["Overworld Velocity"][1]
                
                    overworldSize = self.imageDict["Overworld FF6"].get_rect().size
                    overworldScreenSize = self.imageDict["Overworld Screen Border"].get_rect().size
                    overworldScreenSize = [overworldScreenSize[0] - (Config.BORDER_INDENT * 2), overworldScreenSize[1] - (Config.BORDER_INDENT * 2)]
                    if self.properties["Overworld Offset"][0] < 0:
                        self.properties["Overworld Offset"][0] = 0
                        self.properties["Overworld Velocity"][0] *= -1
                    elif self.properties["Overworld Offset"][0] > overworldSize[0] - overworldScreenSize[0]:
                        self.properties["Overworld Offset"][0] = overworldSize[0] - overworldScreenSize[0]
                        self.properties["Overworld Velocity"][0] *= -1
                    if self.properties["Overworld Offset"][1] < 0:
                        self.properties["Overworld Offset"][1] = 0
                        self.properties["Overworld Velocity"][1] *= -1
                    elif self.properties["Overworld Offset"][1] > overworldSize[1] - overworldScreenSize[1]:
                        self.properties["Overworld Offset"][1] = overworldSize[1] - overworldScreenSize[1]
                        self.properties["Overworld Velocity"][1] *= -1
                        
                    # Slowdown Timers #
                    for i in range(len(self.properties["Overworld Velocity Timer"])):
                        if self.properties["Overworld Velocity"][i] != 0:
                            self.properties["Overworld Velocity Timer"][i] += 1
                            if self.properties["Overworld Velocity Timer"][i] >= 37:
                                self.properties["Overworld Velocity Timer"][i] = 0
                                if self.properties["Overworld Velocity"][i] < 0:
                                    self.properties["Overworld Velocity"][i] += 1
                                elif self.properties["Overworld Velocity"][i] > 0:
                                    self.properties["Overworld Velocity"][i] -= 1
                            
                    if "All" not in self.drawDict:
                        self.drawDict["Overworld"] = True
                        self.drawDict["Minimap"] = True
                        
                    MOUSE.updatePosition()
                    MOUSE.update(self, SCREEN_LEVEL, {"Offset": self.properties["Overworld Offset"]})
                      
            elif SCREEN_LEVEL == "Town":
            
                # Update Expanding Text Box #
                if "Duel Text Box Size Timer" in self.properties:
                    if self.properties["Duel Text Box Size Timer"] < self.properties["Duel Text Box Size Timer Max"]:
                        self.properties["Duel Text Box Size Timer"] += 1
                        
                        self.drawDict["Town"] = True
            
                # Update Portrait Location #
                if "Portrait X" in self.properties:
                    self.properties["Portrait X"] -= 12
                    if self.properties["Portrait X"] < self.properties["Min Portrait X"]:
                        del self.properties["Portrait X"]
                    
                    self.drawDict["Town"] = True
                    
                # DrawText Object #
                if "Duel DrawText" in self.properties:
                    if not ("Duel Text Box Size Timer" in self.properties and self.properties["Duel Text Box Size Timer"] < self.properties["Duel Text Box Size Timer Max"]):
                        updateDataDict = self.properties["Duel DrawText"].update()
                        
                        if "Update Screen" in updateDataDict and "Town" not in self.drawDict:
                            self.drawDict["Town"] = True
               
        # Draw Rect #
        if "All" in self.drawDict:
            self.drawRectList.append(WINDOW.get_rect())
    
        # Get Data #
        windowSize = WINDOW.get_rect().size
        minimapBorderSize = self.imageDict["Minimap Border"].get_rect().size
        
        # Minimap Screen #
        if "All" in self.drawDict or "Minimap" in self.drawDict:
            overworldSize = self.imageDict["Overworld FF6"].get_rect().size
            minimapSize = self.imageDict["Minimap FF6"].get_rect().size
            minimapLoc = [windowSize[0] - minimapSize[0] - Config.BORDER_INDENT, Config.BORDER_INDENT]
            reticleLoc = [minimapLoc[0], minimapLoc[1]]
            reticleLoc[0] += (self.properties["Overworld Offset"][0] / overworldSize[0]) * minimapSize[0]
            reticleLoc[1] += (self.properties["Overworld Offset"][1] / overworldSize[1]) * minimapSize[1]
            
            WINDOW.blit(self.imageDict["Minimap FF6"], minimapLoc)
            pygame.draw.rect(WINDOW, [150, 0, 0], [reticleLoc[0], reticleLoc[1], self.properties["Minimap Reticle Size"][0], self.properties["Minimap Reticle Size"][1]], 1)
            WINDOW.blit(self.imageDict["Minimap Border"], [windowSize[0] - minimapBorderSize[0], 0])
            if "All" not in self.drawDict:
                self.drawRectList.append([minimapLoc[0], minimapLoc[1], minimapSize[0], minimapSize[1]])
        
        # Side Screen #
        if "All" in self.drawDict or "Side Screen" in self.drawDict:
            WINDOW.blit(self.imageDict["Side Screen Border"], [windowSize[0] - minimapBorderSize[0], minimapBorderSize[1] - 1])
            
            buttonSelectedCheck = False
            for sideMenuButton in self.sideMenuButtonList:
                if "Selected" in sideMenuButton.properties and sideMenuButton.properties["Selected"] == True:
                    buttonSelectedCheck = True
                    break
            for sideMenuButton in self.sideMenuButtonList:
                buttonProperties = {}
                if buttonSelectedCheck:
                    buttonProperties["Hide Hover Image"] = True
                sideMenuButton.draw(WINDOW, self.imageDict["Hover Image"], buttonProperties)
            
            if "All" not in self.drawDict:
                self.drawRectList.append([windowSize[0] - minimapBorderSize[0] + Config.BORDER_INDENT, minimapBorderSize[1] + Config.BORDER_INDENT, minimapBorderSize[0] - (Config.BORDER_INDENT * 2), windowSize[1] - minimapBorderSize[1] - (Config.BORDER_INDENT * 2)])
        
        # Main Screen #
        if SCREEN_LEVEL == "Overworld":
            if "All" in self.drawDict or "Overworld" in self.drawDict:
                overworldScreenBorderSize = self.imageDict["Overworld Screen Border"].get_rect().size
                overworldDisplayRect = [self.properties["Overworld Offset"][0], self.properties["Overworld Offset"][1], overworldScreenBorderSize[0] - (Config.BORDER_INDENT * 2), overworldScreenBorderSize[1] - (Config.BORDER_INDENT * 2)]
                WINDOW.blit(self.imageDict["Overworld FF6"], [Config.BORDER_INDENT, Config.BORDER_INDENT], overworldDisplayRect)
                
                # Overworld Text Box #
                if MOUSE.hoverSubscreen != None and MOUSE.hoverSubscreen.id == "Overworld Screen":
                    if MOUSE.hoverElement != None and "Overworld Location" in MOUSE.hoverElement.properties:
                        overworldScreenSize = self.imageDict["Overworld Screen Border"].get_rect().size
                        overworldTextBoxSize = self.imageDict["Overworld Location Text Box"].get_rect().size
                        overworldTextBoxLocation = [0, 0]
                        overworldTextBoxLocation[0] = MOUSE.hoverElement.rect.left - self.properties["Overworld Offset"][0] + MOUSE.hoverElement.rect.width - 20
                        overworldTextBoxLocation[1] = MOUSE.hoverElement.rect.top - self.properties["Overworld Offset"][1] - 35
                        
                        overworldBubbleLocation = [overworldTextBoxLocation[0] - 13, overworldTextBoxLocation[1] + 68]
                        textBoxBubbleImage = self.imageDict["Text Box"]["Bubble Bottom Left"]
                        
                        # Side Checks #
                        if overworldTextBoxLocation[0] < 50:
                            overworldTextBoxLocation[0] = 50
                            overworldBubbleLocation[0] = 50 - 13
                        elif overworldTextBoxLocation[0] + overworldTextBoxSize[0] > overworldScreenSize[0] - 20:
                            overworldTextBoxLocation[0] = MOUSE.hoverElement.rect.left - overworldTextBoxSize[0] - self.properties["Overworld Offset"][0]
                            if overworldTextBoxLocation[0] + overworldTextBoxSize[0] > overworldScreenSize[0] - 50:
                                overworldTextBoxLocation[0] = overworldScreenSize[0] - overworldTextBoxSize[0] - 50
                            overworldBubbleLocation = [overworldTextBoxLocation[0] + overworldTextBoxSize[0] - 8, overworldTextBoxLocation[1] + 68]
                            textBoxBubbleImage = self.imageDict["Text Box"]["Bubble Bottom Right"]
                        
                        if overworldTextBoxLocation[1] < 20:
                            overworldTextBoxLocation[1] = 20
                            overworldBubbleLocation[1] = 20
                            if textBoxBubbleImage == self.imageDict["Text Box"]["Bubble Bottom Right"]:
                                textBoxBubbleImage = self.imageDict["Text Box"]["Bubble Top Right"]
                            else : textBoxBubbleImage = self.imageDict["Text Box"]["Bubble Top Left"]
                        elif overworldTextBoxLocation[1] + overworldTextBoxSize[1] > overworldScreenSize[1] - 50:
                            overworldTextBoxLocation[1] = overworldScreenSize[1] - overworldTextBoxSize[1] - 50
                            overworldBubbleLocation[1] = overworldTextBoxLocation[1] + 68
                        
                        WINDOW.blit(self.imageDict["Overworld Location Text Box"], overworldTextBoxLocation)
                        WINDOW.blit(textBoxBubbleImage, overworldBubbleLocation)
                        
                        Utility.write(MOUSE.hoverElement.properties["Town Name"], [overworldTextBoxLocation[0] + 15, overworldTextBoxLocation[1] - 10], [200, 200, 200], Config.FONT_FF_54, WINDOW)
                        
                WINDOW.blit(self.imageDict["Overworld Screen Border"], [0, 0])
                
                if "All" not in self.drawDict:
                    self.drawRectList.append([Config.BORDER_INDENT, Config.BORDER_INDENT, overworldScreenBorderSize[0] - (Config.BORDER_INDENT * 2), overworldScreenBorderSize[1] - (Config.BORDER_INDENT * 2)])
            
        elif SCREEN_LEVEL == "Town":
            if "All" in self.drawDict or "Town" in self.drawDict:
                
                # Town Background #
                WINDOW.blit(self.imageDict["Town Background"], [Config.BORDER_INDENT, Config.BORDER_INDENT])
                
                # Town Name #
                if "Town Name Text Box Timer" in self.properties:
                    WINDOW.blit(self.imageDict["Town Name Text Box"], [20, 20])
                
                # Duel Text Box #
                if "Duel Text Box" in self.properties:
                    
                    duelTextBoxImage = self.imageDict["Duel Text Box"]
                    duelTextBoxImageRect = duelTextBoxImage.get_rect()
                    if self.properties["Duel Text Box Size Timer"] < self.properties["Duel Text Box Size Timer Max"]:
                        textBoxImageSizePercent = self.properties["Duel Text Box Size Timer"] / self.properties["Duel Text Box Size Timer Max"]
                        duelTextBoxImage = pygame.transform.scale(duelTextBoxImage, [duelTextBoxImageRect.width, duelTextBoxImageRect.height * textBoxImageSizePercent])
                
                    duelTextBoxX = int((self.imageDict["Town Top Screen Border"].get_rect().width - self.imageDict["Duel Text Box"].get_rect().width) / 2)
                    duelTextBoxY = self.imageDict["Town Top Screen Border"].get_rect().height - self.imageDict["Duel Text Box"].get_rect().height - duelTextBoxX + ((self.imageDict["Duel Text Box"].get_rect().height - duelTextBoxImage.get_rect().height) / 2)
                    duelTextBoxLoc = [duelTextBoxX, duelTextBoxY]
                    portraitX = self.properties["Min Portrait X"]
                    if "Portrait X" in self.properties:
                        portraitX = self.properties["Portrait X"]
                        
                    mainScreenBorderSize = self.imageDict["Town Top Screen Border"].get_rect().size
                    portraitDisplaySize = [mainScreenBorderSize[0] - portraitX, mainScreenBorderSize[1]]
                    portraitDisplayRect = [0, 0, portraitDisplaySize[0], portraitDisplaySize[1]]
                    WINDOW.blit(self.imageDict["Portraits"]["Girl"], [portraitX, 38], portraitDisplayRect)
                    WINDOW.blit(duelTextBoxImage, duelTextBoxLoc)
                    
                    if not ("Duel Text Box Size Timer" in self.properties and self.properties["Duel Text Box Size Timer"] < self.properties["Duel Text Box Size Timer Max"]):
                        if "Duel DrawText" in self.properties:
                            self.properties["Duel DrawText"].draw(WINDOW)
                        
                        if "Duel Text Box Button List" in self.properties:
                            for duelTextBoxButton in self.properties["Duel Text Box Button List"]:
                                duelTextBoxButton.draw(WINDOW, self.imageDict["Hover Image"])
                        
                WINDOW.blit(self.imageDict["Town Top Screen Border"], [0, 0])
                
                # Town Under Section #
                lowerScreenBorderSize = self.imageDict["Town Bottom Screen Border"].get_rect().size
                WINDOW.blit(self.imageDict["Town Bottom Screen"], [Config.BORDER_INDENT, windowSize[1] - lowerScreenBorderSize[1] + Config.BORDER_INDENT])
                WINDOW.blit(self.imageDict["Town Bottom Screen Border"], [0, windowSize[1] - lowerScreenBorderSize[1]])
            
                if "All" not in self.drawDict:
                    overworldScreenBorderSize = self.imageDict["Overworld Screen Border"].get_rect().size
                    self.drawRectList.append([Config.BORDER_INDENT, Config.BORDER_INDENT, overworldScreenBorderSize[0] - (Config.BORDER_INDENT * 2), overworldScreenBorderSize[1] - (Config.BORDER_INDENT * 2)])
            
        elif SCREEN_LEVEL == "Card Collection":
        
            # Background & Labels #
            WINDOW.blit(self.imageDict["Cards Screen"], [0, 0])
            
            # Card Collection (Top) #
            cardLoc = [31, 53]
            for idNum, cardButton in enumerate(self.subscreenButtonDict["Card Collection Button List"]):
                
                # Get Card Image #
                idNum += 1
                if (idNum) in PLAYER.cardCollectionDict:
                    cardID = Card.Load((idNum), "Player").id
                    if cardID in self.imageDict["Cards Small"]:
                        cardImage = self.imageDict["Cards Small"][cardID]
                    else : cardImage = self.imageDict["Card Back Small"]
                    WINDOW.blit(cardImage, cardLoc)
                else : WINDOW.blit(self.imageDict["Card Back Small"], cardLoc)
                
                cardLoc[0] += 68
                if (idNum) % 8 == 0:
                    cardLoc[0] = 31
                    cardLoc[1] += 96
                    
            # Hover Card (Bottom) #
            if MOUSE.hoverElement != None and MOUSE.hoverElement.id[0:22] == "Card Collection Button":
                hoverCardIDNum = int(MOUSE.hoverElement.id.split(' ')[-1]) + 1
                if hoverCardIDNum in PLAYER.cardCollectionDict:
                    hoverCardData = Card.Load(hoverCardIDNum, "Player")
                    WINDOW.blit(self.imageDict["Cards"][hoverCardData.id], [16, 412])
                    Utility.write(hoverCardData.id, [145, 400], [200, 200, 200], Config.FONT_FF_54, WINDOW)
            
        elif SCREEN_LEVEL == "Deck Editor":
            WINDOW.blit(self.imageDict["Decks Screen"], [0, 0])
            
            # Card Collection (Top) #
            if True:
                targetDeck = self.properties["Player Deck List"][self.properties["Deck Editor Index"]]
                topCardLocation = [31, 53]
                
                smallHeightSpace = 97
                playerCardCount = PLAYER.getTotalCardCount({"Exclude Card List": targetDeck, "Card Collection Dict": self.properties["Player Card Collection Dict"]})
                if playerCardCount > 16:
                    smallHeightSpace = int(200 / (int(playerCardCount / 8) + 1)) 
                
                cardIndexList = PLAYER.getSortedCollectionList({"Exclude Card List": targetDeck, "Card Collection Dict": self.properties["Player Card Collection Dict"]})
                for cardIndex, cardButton in enumerate(self.subscreenButtonDict["Deck Editor Top Card Button List"]):
                    targetCardIDNum = cardIndexList[cardIndex]
                    targetCard = Card.Load(targetCardIDNum, "Player")
                    cardImage = self.imageDict["Cards Small"][targetCard.id]
                    WINDOW.blit(cardImage, topCardLocation)
                    
                    topCardLocation[0] += 68
                    if (cardIndex + 1) % 8 == 0:
                        topCardLocation[0] = 31
                        topCardLocation[1] += smallHeightSpace
                    
            # Deck (Bottom) #
            insertingCheck = False
            deckCardLocation = [16, 412]
            for i, deckCardID in enumerate(targetDeck):
                if len(targetDeck) < PLAYER.getMaxDeckSize() and insertingCheck == False and MOUSE.clickElement != None and MOUSE.clickElement.id[0:20] == "Top Deck Card Button" and MOUSE.hoverElement != None and MOUSE.hoverElement.id[0:23] == "Bottom Deck Card Button" and int(MOUSE.hoverElement.id.split()[-1]) == i:
                    deckCardLocation[0] += 52
                    insertingCheck = True
            
                targetCard = Card.Load(deckCardID, "Player")
                deckCardImage = self.imageDict["Cards"][targetCard.id]
                WINDOW.blit(deckCardImage, deckCardLocation)
                deckCardLocation[0] += 52
                
            # Deck Hover Card #
            if MOUSE.hoverElement != None and MOUSE.hoverElement.id[0:23] == "Bottom Deck Card Button":
                if not (MOUSE.clickElement != None and MOUSE.clickElement.id[0:20] == "Top Deck Card Button"):
                    targetHoverCardDeckIndex = int(MOUSE.hoverElement.id.split()[-1])
                    targetHoverCardIndex = targetDeck[targetHoverCardDeckIndex]
                    targetHoverCard = Card.Load(targetHoverCardIndex, "Player")
                    hoverCardImage = self.imageDict["Cards"][targetHoverCard.id]
                    WINDOW.blit(hoverCardImage, [MOUSE.hoverElement.rect.left, MOUSE.hoverElement.rect.top])
            
            # Deck Arrow Buttons #
            for button in self.subscreenButtonDict["Deck Editor Button List"]:
                button.draw(WINDOW, self.imageDict["Hover Image"])
              
            # Deck Name & Max Size #
            if True:
                deckNameString = PLAYER.deckNameList[self.properties["Deck Editor Index"]]
                deckNameStringSize = Utility.write(deckNameString, [71, 343], [200, 200, 200], Config.FONT_FF_54, WINDOW)
                deckSizeSize = str(len(targetDeck)) + "/" + str(PLAYER.getMaxDeckSize())
                deckSizeColor = [200, 200, 200]
                if len(targetDeck) < 5 : deckSizeColor = [200, 20, 20]
                deckSizeStringSize = Utility.write(deckSizeSize, [523, 343], deckSizeColor, Config.FONT_FF_54, pygame.Surface([10, 10,]))
                Utility.write(deckSizeSize, [585 - deckSizeStringSize[2], 343], deckSizeColor, Config.FONT_FF_54, WINDOW)
            
            # Deck Editor Underscore #
            if "Deck Name Area Hover Timer" in self.properties and self.properties["Deck Name Area Hover Timer"] != None:
                if self.properties["Deck Name Area Hover Timer"] in range(0, 60):
                    WINDOW.blit(self.imageDict["Underscore"], [deckNameStringSize[2] + 71, 382])
            
            # Click-Drag Card #
            if MOUSE.clickElement != None and MOUSE.clickElement.id[0:20] == "Top Deck Card Button":
                buttonIndex = int(MOUSE.clickElement.id.split()[-1])
                clickCardIndex = cardIndexList[buttonIndex]
                clickCard = Card.Load(clickCardIndex, "Player")
                clickCardImage = self.imageDict["Cards Small"][clickCard.id]
                clickCardLoc = [MOUSE.x, MOUSE.y]
                if "Click Drag Card Offset" in MOUSE.properties:
                    clickCardLoc[0] -= MOUSE.properties["Click Drag Card Offset"][0]
                    clickCardLoc[1] -= MOUSE.properties["Click Drag Card Offset"][1]
                WINDOW.blit(clickCardImage, clickCardLoc)
            
    def mouseClick(self, WINDOW, SCREEN_LEVEL, MOUSE):
    
        returnData = {}
        
        if SCREEN_LEVEL == "Overworld":
            self.properties["Overworld Velocity"] = [0, 0]
            self.properties["Overworld Velocity Timer"] = [0, 0]
        
            if MOUSE.hoverSubscreen != None:
                
                # Adjust Map Reticle Location From Minimap #
                if MOUSE.hoverSubscreen.id == "Overworld Minimap":
                    overworldMapSize = self.imageDict["Overworld FF6"].get_rect().size
                    overworldScreenSize = self.imageDict["Overworld Screen Border"].get_rect().size
                    overworldScreenSize = [overworldScreenSize[0] - (Config.BORDER_INDENT * 2), overworldScreenSize[1] - (Config.BORDER_INDENT * 2)]
                    minimapClickLocation = [MOUSE.x - MOUSE.hoverSubscreen.rect.left, MOUSE.y - MOUSE.hoverSubscreen.rect.top]
                    minimapClickPercent = [minimapClickLocation[0] / MOUSE.hoverSubscreen.rect.width, minimapClickLocation[1] / MOUSE.hoverSubscreen.rect.height]
                    newMapOffset = [int((overworldMapSize[0] * minimapClickPercent[0]) - (overworldScreenSize[0] / 2)), \
                                    int((overworldMapSize[1] * minimapClickPercent[1]) - (overworldScreenSize[1] / 2))]
                    
                    self.properties["Overworld Offset"] = newMapOffset
                    
                    # Scroll Over Edge Check #
                    if self.properties["Overworld Offset"][0] < 0 : self.properties["Overworld Offset"][0] = 0
                    elif self.properties["Overworld Offset"][0] + overworldScreenSize[0] > overworldMapSize[0]:
                        self.properties["Overworld Offset"][0] = overworldMapSize[0] - overworldScreenSize[0]
                    if self.properties["Overworld Offset"][1] < 0 : self.properties["Overworld Offset"][1] = 0
                    elif self.properties["Overworld Offset"][1] + overworldScreenSize[1] > overworldMapSize[1]:
                        self.properties["Overworld Offset"][1] = overworldMapSize[1] - overworldScreenSize[1]
                    
                    self.drawDict["All"] = True
        
        elif SCREEN_LEVEL == "Deck Editor":
            if MOUSE.clickElement != None and MOUSE.clickElement.id[0:20] == "Top Deck Card Button":
                clickDragCardOffset = [MOUSE.x - MOUSE.clickElement.rect.left, MOUSE.y - MOUSE.clickElement.rect.top]
                MOUSE.properties["Click Drag Card Offset"] = clickDragCardOffset
                
        elif SCREEN_LEVEL == "Town":
            if MOUSE.hoverElement != None:
                
                # Click Duel Side Menu Button (Load Duel Menu) #
                if MOUSE.hoverElement.id == "Duel Button" and "Duel Text Box" not in self.properties:
                    
                    # Text Box & Portrait X Location #
                    self.properties["Duel Text Box"] = True
                    self.properties["Portrait X"] = self.imageDict["Town Top Screen Border"].get_rect().width
                    self.properties["Duel Text Box Size Timer"] = 0
                    self.properties["Duel Text Box Size Timer Max"] = 6
                    
                    # Text Box DrawText Message #
                    duelTextBoxX = int((self.imageDict["Town Top Screen Border"].get_rect().width - self.imageDict["Duel Text Box"].get_rect().width) / 2)
                    duelTextBoxY = self.imageDict["Town Top Screen Border"].get_rect().height - self.imageDict["Duel Text Box"].get_rect().height - duelTextBoxX
                    self.properties["Duel DrawText"] = DrawText.Load("Want to play some cards?", [43, duelTextBoxY - 4])
                    
                    # Text Box Buttons #
                    buttonSize = [55, 25]
                    buttonLabelOffset = [0, -21]
                    buttonYLoc = duelTextBoxY + 78
                    self.properties["Duel Text Box Button List"] = []
                    yesButton = Button.Load(WINDOW, "Duel Text Box Yes Button", [70, buttonYLoc], {"Label": "Yes", "Font": Config.FONT_FF_54, "Size": buttonSize, "Label Offset": buttonLabelOffset, "Hover Image": "Cursor Right", "Hover Image Offset": [-30, 31], "Draw Dict String": "Town"})
                    yesButton.properties["Hover Active"] = True
                    self.properties["Duel Text Box Button List"].append(yesButton)
                    buttonYLoc += buttonSize[1]
                    noButton = Button.Load(WINDOW, "Duel Text Box No Button", [70, buttonYLoc], {"Label": "No", "Font": Config.FONT_FF_54, "Size": buttonSize, "Label Offset": buttonLabelOffset, "Hover Image": "Cursor Right", "Hover Image Offset": [-30, 31], "Draw Dict String": "Town"})
                    self.properties["Duel Text Box Button List"].append(noButton)
                    
                    self.drawDict["Town"] = True
                    self.drawDict["Side Screen"] = True
                
                elif MOUSE.hoverElement.id == "Duel Text Box No Button":
                    self.resetDuelProperties()
                    self.drawDict["Town"] = True
                    self.drawDict["Side Screen"] = True
                    
                elif MOUSE.hoverElement.id == "Duel Text Box Yes Button":
                    returnData["Load Battle"] = True
                
        return returnData
            
    def mouseMove(self, SCREEN_LEVEL, MOUSE):
        
        if SCREEN_LEVEL == "Overworld":
            if MOUSE.clickElement != None:
                
                # Scroll Overworld #
                if MOUSE.clickElement.id == "Overworld Screen":
                    scrollOffset = [MOUSE.oldX - MOUSE.x, MOUSE.oldY - MOUSE.y]
                    self.properties["Overworld Offset"][0] += scrollOffset[0]
                    self.properties["Overworld Offset"][1] += scrollOffset[1]
                    
                    overworldSize = self.imageDict["Overworld FF6"].get_rect().size
                    overworldScreenSize = self.imageDict["Overworld Screen Border"].get_rect().size
                    overworldScreenSize = [overworldScreenSize[0] - (Config.BORDER_INDENT * 2), overworldScreenSize[1] - (Config.BORDER_INDENT * 2)]
                    if self.properties["Overworld Offset"][0] < 0 : self.properties["Overworld Offset"][0] = 0
                    elif self.properties["Overworld Offset"][0] > overworldSize[0] - overworldScreenSize[0] : self.properties["Overworld Offset"][0] = overworldSize[0] - overworldScreenSize[0]
                    if self.properties["Overworld Offset"][1] < 0 : self.properties["Overworld Offset"][1] = 0
                    elif self.properties["Overworld Offset"][1] > overworldSize[1] - overworldScreenSize[1] : self.properties["Overworld Offset"][1] = overworldSize[1] - overworldScreenSize[1]
                    
                    if self.properties["Overworld Velocity"][0] > self.properties["Max Overworld Velocity"] : self.properties["Overworld Velocity"][0] = self.properties["Max Overworld Velocity"]
                    elif self.properties["Overworld Velocity"][0] < self.properties["Max Overworld Velocity"] * -1 : self.properties["Overworld Velocity"][0] = self.properties["Max Overworld Velocity"] * -1
                    if self.properties["Overworld Velocity"][1] > self.properties["Max Overworld Velocity"] : self.properties["Overworld Velocity"][1] = self.properties["Max Overworld Velocity"]
                    elif self.properties["Overworld Velocity"][1] < self.properties["Max Overworld Velocity"] * -1 : self.properties["Overworld Velocity"][1] = self.properties["Max Overworld Velocity"] * -1
            
                    if "All" not in self.drawDict:
                        self.drawDict["Overworld"] = True
                        self.drawDict["Minimap"] = True
    
                # Scroll Minimap #
                elif MOUSE.clickElement.id == "Overworld Minimap" and MOUSE.hoverSubscreen != None and MOUSE.hoverSubscreen.id == "Overworld Minimap":
                    
                    overworldMapSize = self.imageDict["Overworld FF6"].get_rect().size
                    overworldScreenSize = self.imageDict["Overworld Screen Border"].get_rect().size
                    overworldScreenSize = [overworldScreenSize[0] - (Config.BORDER_INDENT * 2), overworldScreenSize[1] - (Config.BORDER_INDENT * 2)]
                    minimapClickLocation = [0, 0]
                    minimapClickPercent = [0, 0]
                    if MOUSE.hoverSubscreen != None:
                        minimapClickLocation = [MOUSE.x - MOUSE.hoverSubscreen.rect.left, MOUSE.y - MOUSE.hoverSubscreen.rect.top]
                        minimapClickPercent = [minimapClickLocation[0] / MOUSE.hoverSubscreen.rect.width, minimapClickLocation[1] / MOUSE.hoverSubscreen.rect.height]
                    newMapOffset = [int((overworldMapSize[0] * minimapClickPercent[0]) - (overworldScreenSize[0] / 2)), \
                                    int((overworldMapSize[1] * minimapClickPercent[1]) - (overworldScreenSize[1] / 2))]
                    
                    self.properties["Overworld Offset"] = newMapOffset
                    self.properties["Overworld Velocity"] = [0, 0]
                    
                    # Scroll Over Edge Check #
                    if self.properties["Overworld Offset"][0] < 0 : self.properties["Overworld Offset"][0] = 0
                    elif self.properties["Overworld Offset"][0] + overworldScreenSize[0] > overworldMapSize[0]:
                        self.properties["Overworld Offset"][0] = overworldMapSize[0] - overworldScreenSize[0]
                    if self.properties["Overworld Offset"][1] < 0 : self.properties["Overworld Offset"][1] = 0
                    elif self.properties["Overworld Offset"][1] + overworldScreenSize[1] > overworldMapSize[1]:
                        self.properties["Overworld Offset"][1] = overworldMapSize[1] - overworldScreenSize[1]
                    
                    self.drawDict["All"] = True
    
        elif SCREEN_LEVEL == "Deck Editor":
            
            # Click-Drag Card Update #
            if MOUSE.clickElement != None and MOUSE.clickElement.id[0:20] == "Top Deck Card Button":
                self.drawDict["All"] = True
                
            # Activate Change Deck Name #
            elif MOUSE.hoverSubscreen != None and MOUSE.hoverSubscreen.id == "Deck Editor Deck Name Area Button" and "Deck Name Area Hover Timer" in self.properties and self.properties["Deck Name Area Hover Timer"] == None:
                self.properties["Deck Name Area Hover Timer"] = 0
                self.drawDict["All"] = True
    
    # Utility Functions #
    def loadScreenData(self, WINDOW, MOUSE, GAME_DATA, TARGET_SCREEN, PROPERTIES={}):
    
        # Get Data #
        miniMapSize = self.imageDict["Minimap FF6"].get_rect().size
        miniMapBorderSize = [miniMapSize[0] + (Config.BORDER_INDENT * 2), miniMapSize[1] + (Config.BORDER_INDENT * 2)]
                
        # Save Deck Editor Data #
        if "Save Deck Check" in self.properties and self.properties["Save Deck Check"] == False and TARGET_SCREEN not in ["Deck Editor", "Load Deck Editor Buttons", "Deck Editor Left Button", "Deck Editor Right Button"] and TARGET_SCREEN[0:23] != "Bottom Deck Card Button":
            self.properties["Save Deck Check"] = True
            for dNum, deck in enumerate(self.properties["Player Deck List"]):
                if len(deck) >= 5:
                    GAME_DATA.playerData.deckDataList[dNum] = deck.copy()
                
        # Load Screen Data #
        if TARGET_SCREEN == "Back":
            self.loadScreenData(WINDOW, MOUSE, GAME_DATA, self.properties["Last Screen"], {"Player Pressed Back Button": True})
    
        elif TARGET_SCREEN == "Overworld":
            GAME_DATA.screenLevel = "Overworld"
            self.resetProperties(["Town", "Player Card Collection", "Deck Editor"])
            
            self.overworldButtonList = self.loadOverworldButtonList(WINDOW)
            self.sideMenuButtonList = self.loadSideMenuButtonList(WINDOW, GAME_DATA.screenLevel)
            
            self.drawDict["All"] = True
            WINDOW.fill([0, 0, 0])
            
        elif TARGET_SCREEN == "Town":
            GAME_DATA.screenLevel = "Town"
            self.resetProperties(["Overworld", "Player Card Collection", "Deck Editor"])
            
            # Get Last Town Data #
            if "Player Pressed Back Button" in PROPERTIES:
                lastTownID = GAME_DATA.lastTownID
            else:
                lastTownID = ' '.join(MOUSE.hoverElement.id.split()[0:-2])
                GAME_DATA.lastTownID = lastTownID
            
            self.sideMenuButtonList = self.loadSideMenuButtonList(WINDOW, GAME_DATA.screenLevel)
            
            if "Player Pressed Back Button" not in PROPERTIES:
                townNameSurfaceSize = Utility.write(lastTownID, [20, -13], [200, 200, 200], Config.FONT_FF_54, pygame.Surface([10, 10]))
                self.imageDict["Town Name Text Box"] = Utility.createTextBox(self.imageDict["Text Box"], {"Size": [townNameSurfaceSize[2] + 35, 40], "Color": [29, 29, 85, 225]})
                townNameSurfaceSize = Utility.write(lastTownID, [20, -13], [200, 200, 200], Config.FONT_FF_54, self.imageDict["Town Name Text Box"])
                self.properties["Town Name Text Box Timer"] = 300
            
            mainScreenBorderSize = [Config.SCREEN_SIZE[0] - miniMapBorderSize[0] + 1, 446]
            backgroundID = GAME_DATA.locationDataDict[lastTownID].backgroundID
            self.imageDict["Town Background"] = pygame.image.load("../Image/Backgrounds/" + backgroundID + ".png").convert_alpha()
            self.imageDict["Town Top Screen Border"] = Utility.createTextBox(self.imageDict["Text Box"], {"Size": mainScreenBorderSize})
            self.imageDict["Town Bottom Screen"] = pygame.image.load("../Image/Backgrounds/Underscreen.png").convert()
            self.imageDict["Town Bottom Screen Border"] = Utility.createTextBox(self.imageDict["Text Box"], {"Size": [mainScreenBorderSize[0], Config.SCREEN_SIZE[1] - mainScreenBorderSize[1] + 1]})
            self.imageDict["Portraits"]["Girl"] = pygame.image.load("../Image/Portraits/Girl.png").convert_alpha()
            self.imageDict["Duel Text Box"] = Utility.createTextBox(self.imageDict["Text Box"], {"Size": [550, 150], "Color": [29, 29, 85, 225]})
            
            self.drawDict["All"] = True
            WINDOW.fill([0, 0, 0])
            
        elif TARGET_SCREEN == "Card Collection":
        
            # Set Last Screen Data #
            if GAME_DATA.screenLevel in ["Overworld", "Town"]:
                self.properties["Last Screen"] = GAME_DATA.screenLevel
            if self.properties["Last Screen"] != None:
                self.resetProperties([self.properties["Last Screen"]] + ["Deck Editor"])
            GAME_DATA.screenLevel = "Card Collection"
            
            self.imageDict["Cards"] = {}
            self.imageDict["Cards Small"] = {}
            
            # Load Background Image #
            if True:
                cardsScreenSize = [Config.SCREEN_SIZE[0] - miniMapBorderSize[0] + 1, Config.SCREEN_SIZE[1]]
                self.imageDict["Cards Screen"] = pygame.Surface(cardsScreenSize)
                cardsTitleScreen = Utility.createTextBox(self.imageDict["Text Box"], {"Size": [cardsScreenSize[0], 41], "Color": [29, 29, 85, 255]})
                cardsTopScreen = Utility.createTextBox(self.imageDict["Text Box"], {"Size": [cardsScreenSize[0], cardsScreenSize[1] - 41 - 202], "Color": [29, 29, 85, 255]})
                cardsBottomScreen = Utility.createTextBox(self.imageDict["Text Box"], {"Size": [cardsScreenSize[0], 204], "Color": [29, 29, 85, 255]})
                
                self.imageDict["Cards Screen"].blit(cardsTitleScreen, [0, 0])
                self.imageDict["Cards Screen"].blit(cardsTopScreen, [0, 40])
                self.imageDict["Cards Screen"].blit(cardsBottomScreen, [0, cardsScreenSize[1] - 204])
                
                Utility.write("Card Collection", [20, -13], [200, 200, 200], Config.FONT_FF_54, self.imageDict["Cards Screen"])
                cardCountString = str(GAME_DATA.playerData.getTotalCardCount()) + "/13"
                Utility.write(cardCountString, [499, -13], [200, 200, 200], Config.FONT_FF_54, self.imageDict["Cards Screen"])
            
            # Load Card Images #
            for idNum in GAME_DATA.playerData.cardCollectionDict:
                cardData = Card.Load(idNum, "Player")
                if GAME_DATA.playerData.cardCollectionDict[idNum] == 0:
                    self.imageDict["Cards"][cardData.id] = cardData.getImage()
                    self.imageDict["Cards Small"][cardData.id] = cardData.getImage({"Small": True, "Alpha": 30})
                else:
                    self.imageDict["Cards"][cardData.id] = cardData.getImage()
                    self.imageDict["Cards Small"][cardData.id] = cardData.getImage({"Small": True})
            
            # Load Button List #
            self.subscreenButtonDict["Card Collection Button List"] = []
            cardButtonLoc = [31, 53]
            for i in range(Config.CARD_COUNT):
                cardButton = Button.Load(WINDOW, "Card Collection Button " + str(i), cardButtonLoc, {"Size": [60, 87], "Draw Dict String": "All"})
                self.subscreenButtonDict["Card Collection Button List"].append(cardButton)
                
                cardButtonLoc[0] += 68
                if (i + 1) % 8 == 0:
                    cardButtonLoc[0] = 31
                    cardButtonLoc[1] += 96
            
            self.drawDict["All"] = True
            self.sideMenuButtonList = self.loadSideMenuButtonList(WINDOW, GAME_DATA.screenLevel)
            WINDOW.fill([0, 0, 0])
            
        elif TARGET_SCREEN == "Deck Editor":
        
            # Last Screen Data #
            if GAME_DATA.screenLevel in ["Overworld", "Town"]:
                self.properties["Last Screen"] = GAME_DATA.screenLevel
            if self.properties["Last Screen"] != None:
                self.resetProperties([self.properties["Last Screen"]] + ["Player Card Collection"])
            GAME_DATA.screenLevel = "Deck Editor"
            
            # Load Background Image #
            if True:
                decksScreenSize = [Config.SCREEN_SIZE[0] - miniMapBorderSize[0] + 1, Config.SCREEN_SIZE[1]]
                self.imageDict["Decks Screen"] = pygame.Surface(decksScreenSize)
                decksTitleScreen = Utility.createTextBox(self.imageDict["Text Box"], {"Size": [decksScreenSize[0], 41], "Color": [29, 29, 85, 255]})
                decksTopScreen = Utility.createTextBox(self.imageDict["Text Box"], {"Size": [decksScreenSize[0], 317], "Color": [29, 29, 85, 255]})
                decksSelectScreen = Utility.createTextBox(self.imageDict["Text Box"], {"Size": [54, 41], "Color": [29, 29, 85, 255]})
                decksNameScreen = Utility.createTextBox(self.imageDict["Text Box"], {"Size": [545, 41], "Color": [29, 29, 85, 255]})
                decksBottomScreen = Utility.createTextBox(self.imageDict["Text Box"], {"Size": [decksScreenSize[0], 204], "Color": [29, 29, 85, 255]})
                
                self.imageDict["Decks Screen"].blit(decksTitleScreen, [0, 0])
                self.imageDict["Decks Screen"].blit(decksTopScreen, [0, 40])
                self.imageDict["Decks Screen"].blit(decksSelectScreen, [0, 40 + 316])
                self.imageDict["Decks Screen"].blit(decksNameScreen, [52, 40 + 316])
                self.imageDict["Decks Screen"].blit(decksBottomScreen, [0, decksScreenSize[1] - 204])
                Utility.write("Deck Editor", [20, -13], [200, 200, 200], Config.FONT_FF_54, self.imageDict["Decks Screen"])
                
            # Load Button Data #
            deckEditorDeckAreaButton = Button.Load(WINDOW, "Deck Editor Deck Area Button", [7, 403], {"Size": [585, 192], "Subscreen": True})
            self.subscreenButtonDict["Deck Editor Deck Area Button"] = deckEditorDeckAreaButton
            deckEditorDeckNameAreaButton = Button.Load(WINDOW, "Deck Editor Deck Name Area Button", [58, 362], {"Size": [533, 29], "Subscreen": True})
            self.subscreenButtonDict["Deck Editor Deck Name Area Button"] = deckEditorDeckNameAreaButton
            
            self.subscreenButtonDict["Deck Editor Button List"] = []
            imageArrowLeft = pygame.image.load("../Image/UI/Arrow_Left.png").convert_alpha()
            imageArrowRight = pygame.transform.flip(imageArrowLeft, True, False)
            leftArrowButton = Button.Load(WINDOW, "Deck Editor Left Button", [14, 369], {"Size": [9, 15], "Image": imageArrowLeft, "Hover Image": "Arrow Left", "No Hover-Stick": True, "Draw Dict String": "All"})
            rightArrowButton = Button.Load(WINDOW, "Deck Editor Right Button", [31, 369], {"Size": [9, 15], "Image": imageArrowRight, "Hover Image": "Arrow Right", "No Hover-Stick": True, "Draw Dict String": "All"})
            self.subscreenButtonDict["Deck Editor Button List"].append(leftArrowButton)
            self.subscreenButtonDict["Deck Editor Button List"].append(rightArrowButton)
            
            # Load Properties #
            self.properties["Save Deck Check"] = False
            self.properties["Deck Editor Index"] = 0
            self.properties["Player Card Collection Dict"] = {}
            for card in GAME_DATA.playerData.cardCollectionDict:
                self.properties["Player Card Collection Dict"][card] = GAME_DATA.playerData.cardCollectionDict[card]
            self.properties["Player Deck List"] = []
            for deck in GAME_DATA.playerData.deckDataList:
                self.properties["Player Deck List"].append(deck.copy())
                
            self.loadScreenData(WINDOW, MOUSE, GAME_DATA, "Load Deck Editor Buttons")
            
            # Load Card Images #
            self.imageDict["Cards"] = {}
            self.imageDict["Cards Small"] = {}
            for idNum in self.properties["Player Card Collection Dict"]:
                cardData = Card.Load(idNum, "Player")
                if self.properties["Player Card Collection Dict"][idNum] > 0:
                    self.imageDict["Cards"][cardData.id] = cardData.getImage()
                    self.imageDict["Cards Small"][cardData.id] = cardData.getImage({"Small": True})
            
            self.drawDict["All"] = True
            self.sideMenuButtonList = self.loadSideMenuButtonList(WINDOW, GAME_DATA.screenLevel)
            WINDOW.fill([0, 0, 0])
            
        elif TARGET_SCREEN == "Load Deck Editor Buttons":
            
            self.subscreenButtonDict["Deck Editor Top Card Button List"] = []
            self.subscreenButtonDict["Deck Editor Bottom Card Button List"] = []
            
            targetDeck = self.properties["Player Deck List"][self.properties["Deck Editor Index"]]
            
            # Load Top Card Button List #
            if True:
                topCardLocation = [31, 53]
                heightSpace = 97 ; smallHeightSpace = 97
                BUTTON_HEIGHT = 87
                playerCardCount = GAME_DATA.playerData.getTotalCardCount({"Exclude Card List": targetDeck, "Card Collection Dict": self.properties["Player Card Collection Dict"]})
                if playerCardCount > 16:
                    smallHeightSpace = int(200 / (int(playerCardCount / 8) + 1))                    
                
                for topCardNum in range(playerCardCount):
                    if topCardNum in range(playerCardCount - 8, playerCardCount):
                        buttonHeight = BUTTON_HEIGHT
                    else:
                        buttonHeight = smallHeightSpace
                
                    topDeckCardButton = Button.Load(WINDOW, "Top Deck Card Button " + str(topCardNum), topCardLocation, {"Size": [60, buttonHeight], "Default Color": [random.randrange(255),random.randrange(255),random.randrange(255)], "Draw Dict String": "All"})
                    self.subscreenButtonDict["Deck Editor Top Card Button List"].append(topDeckCardButton)
                    
                    topCardLocation[0] += 68
                    if (topCardNum + 1) % 8 == 0:
                        topCardLocation[0] = 31
                        topCardLocation[1] += smallHeightSpace
            
            # Load Bottom Card Button List #
            deckCardLocation = [16, 412]
            buttonWidth = 52
            for bottomCardNum in range(len(targetDeck)):
                if bottomCardNum == len(targetDeck) - 1:
                    buttonWidth = 118
                bottomDeckCardButton = Button.Load(WINDOW, "Bottom Deck Card Button " + str(bottomCardNum), deckCardLocation, {"Size": [buttonWidth, 172], "Default Color": [random.randrange(255),random.randrange(255),random.randrange(255)], "Draw Dict String": "All"})
                self.subscreenButtonDict["Deck Editor Bottom Card Button List"].append(bottomDeckCardButton)
                deckCardLocation[0] += 52
            
        elif TARGET_SCREEN in ["Deck Editor Left Button", "Deck Editor Right Button"]:
            if TARGET_SCREEN == "Deck Editor Left Button":
                self.properties["Deck Editor Index"] -= 1
                if self.properties["Deck Editor Index"] < 0:
                    self.properties["Deck Editor Index"] = len(GAME_DATA.playerData.deckNameList) - 1
                
            elif TARGET_SCREEN == "Deck Editor Right Button":
                self.properties["Deck Editor Index"] += 1
                if self.properties["Deck Editor Index"] >= len(GAME_DATA.playerData.deckNameList):
                    self.properties["Deck Editor Index"] = 0
                    
            self.loadScreenData(WINDOW, MOUSE, GAME_DATA, "Load Deck Editor Buttons")
            self.drawDict["All"] = True
            
        elif TARGET_SCREEN[0:23] == "Bottom Deck Card Button":
            targetDeck = self.properties["Player Deck List"][self.properties["Deck Editor Index"]]
            targetDeckCardIndex = int(TARGET_SCREEN.split()[-1])
            del targetDeck[targetDeckCardIndex]
            
            # Reload Bottom Card Button List #
            self.loadScreenData(WINDOW, MOUSE, GAME_DATA, "Load Deck Editor Buttons")
            MOUSE.update(self, GAME_DATA.screenLevel)
            self.drawDict["All"] = True
            
    def resetProperties(self, RESET_LIST):
        
        if "Overworld" in RESET_LIST:
            self.overworldButtonList = []
    
        if "Town" in RESET_LIST:
            self.imageDict["Town Name Text Box"] = None
            self.imageDict["Town Background"] = None
            self.imageDict["Town Top Screen Border"] = None
            self.imageDict["Town Bottom Screen"] = None
            self.imageDict["Town Bottom Screen Border"] = None
            self.imageDict["Portraits"]["Girl"] = None
            self.imageDict["Duel Text Box"] = None
            
            if "Town Name Text Box Timer" in self.properties:
                del self.properties["Town Name Text Box Timer"]
            
        if "Player Card Collection" in RESET_LIST:
            self.imageDict["Cards Screen"] = None
            self.imageDict["Cards"] = {}
            self.imageDict["Cards Small"] = {}
            self.subscreenButtonDict["Card Collection Button List"] = []
        
        if "Deck Editor" in RESET_LIST:
            self.properties["Deck Name Area Hover Timer"] = None
            self.properties["Player Card Collection Dict"] = {}
            self.properties["Player Deck List"] = []
            self.imageDict["Decks Screen"] = None
            self.imageDict["Cards"] = {}
            self.imageDict["Cards Small"] = {}
            self.subscreenButtonDict["Deck Editor Deck Area Button"] = None
            self.subscreenButtonDict["Deck Editor Deck Name Area Button"] = None
            self.subscreenButtonDict["Deck Editor Button List"] = []
            self.subscreenButtonDict["Deck Editor Top Card Button List"] = []
            self.subscreenButtonDict["Deck Editor Bottom Card Button List"] = []
    
    def resetDuelProperties(self):
     
        propertyList = ["Duel Text Box",
                        "Portrait X",
                        "Duel DrawText",
                        "Duel Text Box Button List",
                        "Duel Text Box Size Timer",
                        "Duel Text Box Size Timer Max"]
     
        for targetProperty in propertyList:
            if targetProperty in self.properties:
                del self.properties[targetProperty]
                
        for sideMenuButton in self.sideMenuButtonList:
            if "Selected" in sideMenuButton.properties and sideMenuButton.properties["Selected"] == True:
                sideMenuButton.properties["Selected"] = False
    
    # Class Functions #    
    def getCurrentHoverButton(self):
    
        targetButton = None
        
        if "Duel Text Box Button List" in self.properties:
            for menuButton in self.properties["Duel Text Box Button List"]:
                if "Hover Image" in menuButton.properties and menuButton.properties["Hover Active"]:
                    targetButton = menuButton
                    break
                
        return targetButton
    
    def keyPress(self, SCREEN_LEVEL, PLAYER, MOUSE, KEYBOARD, KEY):
        
        returnData = {}
        
        # Arrow Keys - Up/Down #
        if KEY in ["up", "down"]:
        
            # Change Menu Position #
            if "Duel Text Box Button List" in self.properties:
                
                # Get Data #
                currentMenuIndex = 0
                for i, menuButton in enumerate(self.properties["Duel Text Box Button List"]):
                    if "Hover Image" in menuButton.properties and menuButton.properties["Hover Active"]:
                        currentMenuIndex = i
                        break
                        
                # Change Menu Position #
                if KEY in ["up", "down"]:
                
                    # Get Index Data #
                    newIndex = currentMenuIndex
                    if KEY == "up" : newIndex -= 1
                    elif KEY == "down" : newIndex += 1
                    if newIndex == -1 : newIndex = len(self.properties["Duel Text Box Button List"]) - 1
                    elif newIndex == len(self.properties["Duel Text Box Button List"]) : newIndex = 0
                    
                    # Set Button Properties #
                    self.properties["Duel Text Box Button List"][currentMenuIndex].properties["Hover Active"] = False
                    if "Hover Image" in self.properties["Duel Text Box Button List"][newIndex].properties:
                        self.properties["Duel Text Box Button List"][newIndex].properties["Hover Active"] = True
                        
                    MOUSE.hoverElement = None
                    self.drawDict["Town"] = True
            
        # Return Key #
        elif KEY == "return":
            currentHoverButton = self.getCurrentHoverButton()
            if currentHoverButton != None:
                if currentHoverButton.id == "Duel Text Box No Button":
                    self.resetDuelProperties()
                    self.drawDict["Town"] = True
                    self.drawDict["Side Screen"] = True
                    
                elif currentHoverButton.id == "Duel Text Box Yes Button":
                    returnData["Load Battle"] = True
               
        # Other Input Keys #
        else:
        
            # Change Deck Name #
            if SCREEN_LEVEL == "Deck Editor":
                if len(PLAYER.deckNameList[self.properties["Deck Editor Index"]]) < 24:
                    if MOUSE.hoverSubscreen != None and MOUSE.hoverSubscreen.id == "Deck Editor Deck Name Area Button":
                        inputKey = None
                        if KEYBOARD.shift == False and KEY in KEYBOARD.inputKeyDict:
                            inputKey = KEYBOARD.inputKeyDict[KEY]
                        elif KEY in KEYBOARD.inputKeyShiftDict:
                            inputKey = KEYBOARD.inputKeyShiftDict[KEY]
                        
                        if inputKey != None:
                            PLAYER.deckNameList[self.properties["Deck Editor Index"]] = PLAYER.deckNameList[self.properties["Deck Editor Index"]] + inputKey
                            self.drawDict["All"] = True
                    
        return returnData
               
    def resetActiveHoverVariables(self, RESET_SUBSCREEN=True):
        
        for menuButton in self.sideMenuButtonList:
            if "Hover Image" in menuButton.properties:
                menuButton.properties["Hover Active"] = False
                
        if "Deck Editor Button List" in self.subscreenButtonDict:
            for deckEditorButton in self.subscreenButtonDict["Deck Editor Button List"]:
                if "Hover Image" in deckEditorButton.properties:
                    deckEditorButton.properties["Hover Active"] = False
    
        if RESET_SUBSCREEN:
            if "Duel Text Box Button List" in self.properties:
                for duelTextBoxButton in self.properties["Duel Text Box Button List"]:
                    if "Hover Image" in duelTextBoxButton.properties:
                        duelTextBoxButton.properties["Hover Active"] = False
                    
    def getElementList(self, SCREEN_LEVEL):
    
        elementList = []
    
        if SCREEN_LEVEL == "Overworld":
            elementList.append(self.subscreenButtonDict["Overworld"])
            elementList.append(self.subscreenButtonDict["Minimap"])
            for element in self.overworldButtonList:
                elementList.append(element)
        
        elif SCREEN_LEVEL == "Card Collection":
            for cardButton in self.subscreenButtonDict["Card Collection Button List"]:
                elementList.append(cardButton)
                
        elif SCREEN_LEVEL == "Deck Editor":
            elementList.append(self.subscreenButtonDict["Deck Editor Deck Area Button"])
            elementList.append(self.subscreenButtonDict["Deck Editor Deck Name Area Button"])
            
            for button in self.subscreenButtonDict["Deck Editor Button List"]:
                elementList.append(button)
            for button in self.subscreenButtonDict["Deck Editor Top Card Button List"]:
                elementList.append(button)
            for button in self.subscreenButtonDict["Deck Editor Bottom Card Button List"]:
                elementList.append(button)
        
        for element in self.sideMenuButtonList:
            elementList.append(element)
        
        if "Duel Text Box Button List" in self.properties:
            for element in self.properties["Duel Text Box Button List"]:
                elementList.append(element)
        
        return elementList
        