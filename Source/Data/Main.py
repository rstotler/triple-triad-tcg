import pygame, Config, Utility
from pygame import *
from Hardware import Mouse, Keyboard
from Screen import MainMenu, GameScreen, Battle
from Data import Game

class Load:

    def __init__(self, WINDOW):
        
        self.mouse = Mouse.Load()
        self.keyboard = Keyboard.Load()
        self.screen = MainMenu.Load(WINDOW)        
        self.game = Game.Load()
        
        # Debug Battle #
        #self.game.screenLevel = "Battle"
        #self.screen = Battle.Load(WINDOW, self.game.screenLevel)

    def updateMain(self, FPS, WINDOW):
    
        # Process User Input & Update Game #
        self.processInput(WINDOW)
        self.game.update(WINDOW, self.screen, self.mouse, self.keyboard)
        
        # Draw Screen #
        self.screen.draw(WINDOW, self.mouse, self.keyboard, self.game.playerData, self.game.screenLevel)
        
        # Display FPS #
        pygame.draw.rect(WINDOW, [0, 0, 0], [WINDOW.get_size()[0] - 46, 0, 46, 13])
        Utility.write(FPS, ["Right", 0], [200, 200, 200], Config.FONT_ROMAN_16, WINDOW)
        if "All" not in self.screen.drawDict:
            self.screen.drawRectList.append(pygame.Rect([WINDOW.get_size()[0] - 46, 0, 46, 13]))
        
        # Update Screen #
        pygame.display.update(self.screen.drawRectList)
        self.screen.drawDict = {}
        self.screen.drawRectList = []
        
    def processInput(self, WINDOW):
    
        returnData = {}
        self.mouse.updatePosition()
        if self.keyboard.backspace:
            self.keyboard.backspaceTimer += 1
        
        for event in pygame.event.get():
            
            # Mouse Events #
            if event.type == MOUSEBUTTONDOWN:
            
                # Update Mouse #
                mouseUpdateProperties = {}
                if self.screen.id == "Game Screen":
                    mouseUpdateProperties["Offset"] = self.screen.properties["Overworld Offset"]
                self.mouse.update(self.screen, self.game.screenLevel, mouseUpdateProperties)
            
                # Left Click #
                if event.button == 1:
                
                    # Update Mouse Click Element & Selected Buttons #
                    if True:
                        if not (self.mouse.hoverElement != None and ' '.join(self.mouse.hoverElement.id.split()[0:-1]) == "NPC Hand Button"):
                            self.mouse.clickElement = self.mouse.hoverElement
                        
                        if self.mouse.clickElement == None:
                            self.mouse.clickElement = self.mouse.hoverSubscreen    
                        if self.mouse.clickElement != None and "Selected" in self.mouse.clickElement.properties:
                            self.mouse.clickElement.properties["Selected"] = True
                    
                    # Main Menu #
                    if self.screen.id == "Main Menu":
                        if self.mouse.hoverElement != None:
                            if self.mouse.hoverElement.id == "New Game Button":
                                self.game.screenLevel = "Overworld"
                                self.screen = GameScreen.Load(WINDOW, self.game.screenLevel)
                                self.mouse.update(self.screen, self.game.screenLevel, {"Offset": self.screen.properties["Overworld Offset"]})
                                
                            elif self.mouse.hoverElement != None:
                                if self.mouse.hoverElement.id == "Quit Button":
                                    raise SystemExit
                                    
                    # Game Screen #
                    elif self.screen.id == "Game Screen":
                        returnData = self.screen.mouseClick(WINDOW, self.game.screenLevel, self.mouse)
                        alreadyClicked = False
                        
                        # Click - Side Menu, Overworld Locations #
                        if self.mouse.hoverElement != None:
                        
                            # Get Data #
                            sidescreenButtonSelectedCheck = False
                            for sideMenuButton in self.screen.sideMenuButtonList:
                                if "Selected" in sideMenuButton.properties and sideMenuButton.properties["Selected"]:
                                    sidescreenButtonSelectedCheck = True
                                    break
                                    
                            if sidescreenButtonSelectedCheck == False:
                                alreadyClicked = True
                                               
                                # Side Menu #
                                if self.mouse.hoverElement.id == "Back Button":
                                    self.screen.loadScreenData(WINDOW, self.mouse, self.game, "Back")
                                
                                elif self.mouse.hoverElement.id == "Travel Button":
                                    self.screen.loadScreenData(WINDOW, self.mouse, self.game, "Overworld")
                            
                                elif self.mouse.hoverElement.id == "Cards Button" and self.game.screenLevel != "Card Collection":
                                    self.screen.loadScreenData(WINDOW, self.mouse, self.game, "Card Collection")
                                
                                elif self.mouse.hoverElement.id == "Decks Button" and self.game.screenLevel != "Deck Editor":
                                    self.screen.loadScreenData(WINDOW, self.mouse, self.game, "Deck Editor")
                            
                                # Overworld Location #
                                elif "Overworld Location" in self.mouse.hoverElement.properties:
                                    self.screen.loadScreenData(WINDOW, self.mouse, self.game, "Town")
                                    
                                # Deck Editor #
                                elif self.mouse.hoverElement.id in ["Deck Editor Left Button", "Deck Editor Right Button"]:
                                    self.screen.loadScreenData(WINDOW, self.mouse, self.game, self.mouse.hoverElement.id)
                                    
                                elif self.mouse.hoverElement.id[0:23] == "Bottom Deck Card Button":
                                    self.screen.loadScreenData(WINDOW, self.mouse, self.game, self.mouse.hoverElement.id)
                                   
                        if returnData != {} and not alreadyClicked:
                            if "Load Battle" in returnData:
                                self.game.screenLevel = "Battle"
                                self.screen = Battle.Load(WINDOW, self.game.screenLevel)
                
                    # Battle #
                    elif self.screen.id == "Battle":
                        self.screen.mouseClick(WINDOW, self.mouse)
                
            elif event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    
                    # Game Screen #
                    if self.screen.id == "Game Screen":
                    
                        # Overworld - Set Map Velocity #
                        if self.mouse.clickElement != None and self.mouse.clickElement.id == "Overworld Screen":
                            self.screen.properties["Overworld Velocity"] = [self.mouse.oldX - self.mouse.x, self.mouse.oldY - self.mouse.y]
                            if self.screen.properties["Overworld Velocity"][0] > self.screen.properties["Max Overworld Velocity"] : self.screen.properties["Overworld Velocity"][0] = self.screen.properties["Max Overworld Velocity"]
                            elif self.screen.properties["Overworld Velocity"][0] < self.screen.properties["Max Overworld Velocity"] * -1 : self.screen.properties["Overworld Velocity"][0] = self.screen.properties["Max Overworld Velocity"] * -1
                            if self.screen.properties["Overworld Velocity"][1] > self.screen.properties["Max Overworld Velocity"] : self.screen.properties["Overworld Velocity"][1] = self.screen.properties["Max Overworld Velocity"]
                            elif self.screen.properties["Overworld Velocity"][1] < self.screen.properties["Max Overworld Velocity"] * -1 : self.screen.properties["Overworld Velocity"][1] = self.screen.properties["Max Overworld Velocity"] * -1
                    
                        # Deck Editor - Add Card To Deck #
                        elif self.mouse.clickElement != None and self.mouse.clickElement.id[0:20] == "Top Deck Card Button":
                            deckEditorIndex = self.screen.properties["Deck Editor Index"]
                            targetDeck = self.screen.properties["Player Deck List"][deckEditorIndex]
                            
                            if len(targetDeck) < self.game.playerData.getMaxDeckSize():
                                insertIndex = -1
                                if self.mouse.hoverElement != None and self.mouse.hoverElement.id[0:23] == "Bottom Deck Card Button":
                                    insertIndex = int(self.mouse.hoverElement.id.split()[-1])
                                elif self.mouse.hoverSubscreen != None and self.mouse.hoverSubscreen.id == "Deck Editor Deck Area Button" and "Deck Editor Index" in self.screen.properties:
                                    insertIndex = len(targetDeck)
                                    
                                if insertIndex != -1:
                                    cardIndexList = self.game.playerData.getSortedCollectionList({"Exclude Card List": targetDeck, "Card Collection Dict": self.screen.properties["Player Card Collection Dict"]})
                                    cardIndex = int(self.mouse.clickElement.id.split()[-1])
                                    insertCardIDNum = cardIndexList[cardIndex]
                                    targetDeck.insert(insertIndex, insertCardIDNum)
                                    
                                    # Reset Screen Buttons #
                                    self.screen.loadScreenData(WINDOW, self.mouse, self.game, "Load Deck Editor Buttons")
                            
                            if "Click Drag Card Offset" in self.mouse.properties:
                                del self.mouse.properties["Click Drag Card Offset"]
                            
                            self.screen.drawDict["All"] = True
                    
                    # Battle #
                    elif self.screen.id == "Battle":
                        self.screen.mouseClickUp(WINDOW, self.mouse)
                        
                    self.mouse.clickElement = None
                
            elif event.type == MOUSEMOTION:
            
                # Update Mouse #
                mouseUpdateProperties = {}
                if self.screen.id == "Game Screen":
                    mouseUpdateProperties["Offset"] = self.screen.properties["Overworld Offset"]
                self.mouse.update(self.screen, self.game.screenLevel, mouseUpdateProperties)
                
                # Game Screen #
                if self.screen.id == "Game Screen":
                    self.screen.mouseMove(self.game.screenLevel, self.mouse)
                    
                elif self.screen.id == "Battle":
                    self.screen.mouseMove(self.mouse)
                                    
            # Keyboard Events #
            elif event.type == KEYDOWN:
                keyName = pygame.key.name(event.key)
                
                # Return #
                if event.key == K_RETURN:
                    
                    # Main Menu #
                    if self.screen.id == "Main Menu":
                        currentHoverButton = self.screen.getCurrentHoverButton()
                        if currentHoverButton != None:
                            if currentHoverButton.id == "New Game Button":
                                self.game.screenLevel = "Overworld"
                                self.screen = GameScreen.Load(WINDOW, self.game.screenLevel)
                                self.mouse.update(self.screen, self.game.screenLevel, {"Offset": self.screen.properties["Overworld Offset"]})
                                
                            elif currentHoverButton.id == "Quit Button":
                                raise SystemExit
                                
                    elif self.screen.id == "Game Screen":
                        returnData = self.screen.keyPress(self.mouse, keyName)
                        if "Load Battle" in returnData:
                            self.game.screenLevel = "Battle"
                            self.screen = Battle.Load(WINDOW, self.game.screenLevel)
                    
                # Shift #
                elif event.key in [K_LSHIFT, K_RSHIFT]:
                    self.keyboard.shift = True
                    
                # Backspace #
                elif event.key == K_BACKSPACE:
                    self.keyboard.backspace = True
                    self.keyboard.backspaceTimer = -1
                    
                # Escape #
                elif event.key == K_ESCAPE:
                    raise SystemExit
                
                # Key Press #
                else:
                    self.screen.keyPress(self.game.screenLevel, self.game.playerData, self.mouse, self.keyboard, keyName)
               
            elif event.type == KEYUP:
            
                if event.key in [K_LSHIFT, K_RSHIFT]:
                    self.keyboard.shift = False
                
                elif event.key == K_BACKSPACE:
                    self.keyboard.backspace = False
               
            # Quit Event #
            elif event.type == QUIT:
                raise SystemExit
             