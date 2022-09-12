import pygame, copy, random, Config, Utility
import math as SystemMath
from pygame import *
from Elements import Button, Card

class Load:
    
    def __init__(self, WINDOW, SCREEN_LEVEL):
    
        self.id = "Battle"
        self.properties = {}
        
        # Load Initial Properties #
        self.properties["Player List"] = ["Player", "NPC 1", "NPC 2"] # Determines Turn Order
        self.properties["Current Turn"] = self.properties["Player List"][0]
        self.properties["Max Hand Size"] = 10
        self.properties["Board"] = [None, None, None, None, None, None, None, None, None]
        
        self.properties["Flip Animation Data List"] = []
        self.properties["Rule Label Animation Data"] = None
        self.properties["Combo Label Activated"] = False
        self.properties["FONT_TIMES_B_30"] = pygame.font.Font("../Font/TimesB.ttf", 30)
        self.properties["FONT_TIMES_BI_30"] = pygame.font.Font("../Font/TimesBI.ttf", 30)
        
        # Load Rule Properties - (Choices: Open, Elemental, Same, Plus, Combo, Same Wall, Plus Wall) #
        self.properties["Rule List"] = ["Open", "Same", "Plus", "Combo"]
        self.properties["Game Phase"] = "Deck Select"
        
        # Load Elemental Board Properties #
        if "Elemental" in self.properties["Rule List"]:
            self.properties["Board Element List"] = [None, None, None, None, None, None, None, None, None]
            for i in range(len(self.properties["Board Element List"])):
                if random.randrange(3) == 0:
                    self.properties["Board Element List"][i] = random.choice(["Earth", "Fire", "Holy", "Ice", "Lightning", "Poison", "Water", "Wind"])
        
        # Load Choose Deck Screen #
        if True:
            self.properties["Deck Select Text Box Button List"] = []
            buttonYLoc = 267
            for i in range(5):
                buttonSize = [230, 13]
                buttonLabelOffset = [35, -13]
                deckMenuButton = Button.Load(WINDOW, "Deck Select Menu Button " + str(i), [285, buttonYLoc], {"Label": "Custom Deck " + str(i + 1), "Font": Config.FONT_FF_32, "Size": buttonSize, "Label Offset": buttonLabelOffset, "Hover Image": "Cursor Right", "Hover Image Offset": [-30, 18], "Draw Dict String": "All"})
                if i == 0 : deckMenuButton.properties["Hover Active"] = True
                self.properties["Deck Select Text Box Button List"].append(deckMenuButton)
                buttonYLoc += buttonSize[1]
                
        # Load Player Hands #
        self.properties["Player Hand"] = None
        self.properties["NPC 1 Hand"] = self.loadHand("NPC 1", self.properties["Max Hand Size"])
        if "NPC 2" in self.properties["Player List"]:
            self.properties["NPC 2 Hand"] = self.loadHand("NPC 2", self.properties["Max Hand Size"])
        
        # Load Turn Variables #
        firstNPCTurnID = "NPC 1"
        if "NPC 2" in self.properties["Player List"] and self.properties["Player List"].index("NPC 2") < self.properties["Player List"].index("NPC 1"):
            firstNPCTurnID = "NPC 2"
        self.properties["NPC Hand Display ID"] = firstNPCTurnID + " Hand"
        
        # Other Variables #
        self.imageDict = self.loadImageDict()
        self.drawDict = {"All": True}
        self.drawRectList = [WINDOW.get_rect()]
        
        self.boardButtonList = self.loadBoardButtonList(WINDOW)
        self.playerHandButtonList = None
        self.npcHandButtonList = self.loadHandButtonList(firstNPCTurnID, WINDOW)
    
    # Initialization Functions #
    def loadImageDict(self):
    
        imageDict = {}
        
        imageDict["Text Box"] = {}
        imageDict["Text Box"]["Corner"] = pygame.image.load("../Image/UI/TextBoxCorner.png").convert_alpha()
        imageDict["Text Box"]["Side"] = pygame.image.load("../Image/UI/TextBoxSide.png").convert()
        
        imageDict["Main Screen Border"] = Utility.createTextBox(imageDict["Text Box"], {"Size": Config.SCREEN_SIZE})
        
        imageDict["Hover Image"] = {}
        imageDict["Hover Image"]["Cursor Right"] = pygame.image.load("../Image/UI/CursorRight.png").convert_alpha()
        imageDict["Hover Image"]["Cursor Left"] = pygame.transform.flip(imageDict["Hover Image"]["Cursor Right"], True, False)
        
        imageDict["Deck Select Text Box"] = Utility.createTextBox(imageDict["Text Box"], {"Size": [244, 122], "Color": [29, 29, 85]})
        
        imageDict["Element Icon"] = {}
        for elementID in ["Earth", "Fire", "Holy", "Ice", "Lightning", "Poison", "Water", "Wind"]:
            imageDict["Element Icon"][elementID] = pygame.image.load("../Image/UI/" + elementID + "Element.png").convert_alpha()
        
        imageDict["Plus 1"] = Utility.writeOutline("+1", self.properties["FONT_TIMES_BI_30"])
        imageDict["Minus 1"] = Utility.writeOutline("-1", self.properties["FONT_TIMES_BI_30"])
        
        imageDict["Same Label"] = pygame.image.load("../Image/UI/SameRule.png").convert_alpha()
        imageDict["Plus Label"] = pygame.image.load("../Image/UI/PlusRule.png").convert_alpha()
        imageDict["Combo Label"] = pygame.image.load("../Image/UI/ComboRule.png").convert_alpha()
        
        imageDict["Shine Top"] = pygame.image.load("../Image/Cards/ShineTop.png").convert_alpha()
        imageDict["Shine Bottom"] = pygame.image.load("../Image/Cards/ShineBottom.png").convert_alpha()
        imageDict["Shine Mask"] = pygame.image.load("../Image/Cards/Mask.png").convert_alpha()
    
        # Card Back & Template #
        imageDict["Cards"] = {}
        cardBase = pygame.Surface([118, 172], pygame.SRCALPHA)
        cardBorder = pygame.image.load("../Image/Cards/Border.png").convert_alpha()
        pygame.draw.rect(cardBase, [0, 255, 0], [2, 2, 114, 168], 0)
        imageDict["Cards"]["Back"] = pygame.image.load("../Image/Cards/Back.png").convert_alpha()
        imageDict["Cards"]["Template"] = pygame.Surface([118, 172], pygame.SRCALPHA)
        imageDict["Cards"]["Template"].blit(cardBase, [0, 0])
        imageDict["Cards"]["Template"].blit(cardBorder, [0, 0])
    
        # Load Cards #
        for i in range(Config.CARD_COUNT):
            cardIDNum = i + 1
            tempCard = Card.Load(cardIDNum, "Player")
            imageDict["Cards"][tempCard.id] = {}
            for cardTarget in ["Player", "NPC 1", "NPC 2"]:
                card = Card.Load(cardIDNum, cardTarget)
                imageDict["Cards"][tempCard.id][cardTarget] = card.getImage()
    
        # Main Screen Background #
        if True:
            imageDict["Main Screen Background"] = pygame.Surface(Config.SCREEN_SIZE)
            pygame.draw.rect(imageDict["Main Screen Background"], [80, 80, 120], [Config.BORDER_INDENT, Config.BORDER_INDENT, Config.SCREEN_SIZE[0] - (Config.BORDER_INDENT * 2), Config.SCREEN_SIZE[1] - (Config.BORDER_INDENT * 2)])
            
            backgroundAlpha = pygame.image.load("../Image/Backgrounds/Town_1.png").convert()
            backgroundAlpha = pygame.transform.scale(backgroundAlpha, [Config.SCREEN_SIZE[0] - (Config.BORDER_INDENT * 2), Config.SCREEN_SIZE[1] - (Config.BORDER_INDENT * 2)])
            backgroundAlpha.set_alpha(30)
            imageDict["Main Screen Background"].blit(backgroundAlpha, [Config.BORDER_INDENT, Config.BORDER_INDENT])
            
            backgroundPortraitGirl = pygame.image.load("../Image/Portraits/Girl.png").convert_alpha()
            backgroundPortraitGirl = pygame.transform.flip(backgroundPortraitGirl, True, False)
            backgroundPortraitGirl = pygame.transform.rotozoom(backgroundPortraitGirl, 0, .82)
            backgroundPortraitGirl.set_alpha(50)
            imageDict["Portrait Girl"] = backgroundPortraitGirl
            
            backgroundPortraitBoy = pygame.image.load("../Image/Portraits/Boy.png").convert_alpha()
            backgroundPortraitBoy = pygame.transform.flip(backgroundPortraitBoy, True, False)
            backgroundPortraitBoy = pygame.transform.rotozoom(backgroundPortraitBoy, 0, .82)
            backgroundPortraitBoy.set_alpha(50)
            imageDict["Portrait Boy"] = backgroundPortraitBoy
            
        return imageDict
        
    def loadBoardButtonList(self, WINDOW):
    
        boardButtonList = []
        buttonStartLocation = [199, 18]
        buttonLocation = [buttonStartLocation[0], buttonStartLocation[1]]
        buttonSize = [134, 188]
        buttonColor1 = [110, 20, 20]
        buttonColor2 = [85, 30, 85]
        
        for i in range(9):
            if i != 0 and i % 3 == 0:
                buttonLocation[0] = buttonStartLocation[0]
                buttonLocation[1] += buttonSize[1]
            buttonColor = buttonColor2
            if i % 2 == 0 : buttonColor = buttonColor1
        
            boardButton = Button.Load(WINDOW, "Board Slot Button " + str(i), buttonLocation, {"Size": buttonSize, "Default Color": buttonColor})
            boardButtonList.append(boardButton)
            
            buttonLocation[0] += buttonSize[0]
            
        return boardButtonList
        
    def loadHandButtonList(self, TARGET_PLAYER, WINDOW):
        
        handButtonList = []
        
        cardSize = self.imageDict["Cards"]["Template"].get_rect().size
        handButtonLocation = [Config.SCREEN_SIZE[0] - cardSize[0] - 30, 30]
        if TARGET_PLAYER[0:3] == "NPC":
            handButtonLocation[0] = 30
        
        handCardSpaceHeight = int(270 / self.properties["Max Hand Size"])
        handButtonSize = [cardSize[0], handCardSpaceHeight]
        
        targetHand = self.properties["Player Hand"]
        if TARGET_PLAYER[0:3] == "NPC":
            targetHandID = TARGET_PLAYER + " Hand"
            if targetHandID in self.properties:
                targetHand = self.properties[targetHandID]
        
        for i in range(len(targetHand)):
            if i == len(targetHand) - 1 : handButtonSize = cardSize
            handButton = Button.Load(WINDOW, TARGET_PLAYER.split()[0] + " Hand Button " + str(i), handButtonLocation, {"Size": handButtonSize, "Draw Dict String": "All"})
            handButtonList.append(handButton)
            handButtonLocation[1] += handCardSpaceHeight
            
        return handButtonList
        
    def loadHand(self, TARGET_PLAYER, HAND_SIZE):
    
        newHand = []
        
        for i in range(HAND_SIZE):
            newCard = Card.Load(random.randrange(Config.CARD_COUNT) + 1, TARGET_PLAYER)
            newHand.append(newCard)
        
        return newHand
        
    # Main Functions #
    def draw(self, WINDOW, MOUSE, KEYBOARD, PLAYER, SCREEN_LEVEL):
        
        # Get Data #
        if True:
        
            windowSize = WINDOW.get_rect().size
            cardSize = self.imageDict["Cards"]["Template"].get_rect().size
            handCardSpaceHeight = int(270 / self.properties["Max Hand Size"])
            hoverCard = None
            handIndex = -1
            clickIndex = -1
            hoverTargetPlayer = None
            
            if MOUSE.hoverElement != None and ' '.join(MOUSE.hoverElement.id.split()[1:-1]) == "Hand Button":
                if MOUSE.hoverElement.id.split()[-1].isdigit():
                    handIndex = int(MOUSE.hoverElement.id.split()[-1])
                    targetHand = self.properties["Player Hand"]
                    hoverTargetPlayer = MOUSE.hoverElement.id.split()[0]
                    if MOUSE.hoverElement.id.split()[0] == "NPC":
                        npcHandID = self.properties["NPC Hand Display ID"]
                        if npcHandID in self.properties:
                            targetHand = self.properties[npcHandID]
                    if handIndex > -1 and handIndex < len(targetHand):
                        hoverCard = targetHand[handIndex]
                        
            if MOUSE.clickElement != None and MOUSE.clickElement.id[0:18] == "Player Hand Button" and MOUSE.clickElement.id.split()[-1].isdigit():
                clickIndex = int(MOUSE.clickElement.id.split()[-1])
        
            ruleAnimationPercent = 0.0
            shineMaskCopy = None
            if self.properties["Rule Label Animation Data"] != None:
                shineMaskCopy = self.imageDict["Shine Mask"].copy()
                shineMaskCopy.set_colorkey([255, 255, 255])
                if self.properties["Rule Label Animation Data"]["Animation Timer Count"] == 0:
                    shineImage = self.imageDict["Shine Top"]
                else : shineImage = self.imageDict["Shine Bottom"]
                shineWidth = shineImage.get_rect().width
                ruleAnimationPercent = self.properties["Rule Label Animation Data"]["Animation Timer"] / self.properties["Rule Label Animation Data"]["Animation Timer Max"]
                shineXLoc = 0
                if self.properties["Rule Label Animation Data"]["Animation Timer Count"] == 0:
                    shineXLoc = -(shineWidth - cardSize[0]) + (shineWidth * ruleAnimationPercent)
                elif self.properties["Rule Label Animation Data"]["Animation Timer Count"] == 1:
                    shineXLoc = -shineWidth + ((shineWidth + cardSize[0]) * ruleAnimationPercent)
                shineMaskCopy.blit(shineImage, [shineXLoc, 0], None, pygame.BLEND_RGBA_MULT)
                       
        # Draw Rect #
        if "All" in self.drawDict:
            self.drawRectList.append(WINDOW.get_rect())
        
        # Background #
        if "All" in self.drawDict:
            WINDOW.blit(self.imageDict["Main Screen Background"], [0, 0])
            
            if self.properties["NPC Hand Display ID"] == "NPC 1 Hand":
                portraitImage = self.imageDict["Portrait Girl"]
            else:
                portraitImage = self.imageDict["Portrait Boy"]
                
            backgroundPortraitLoc = [0, 0]
            backgroundPortraitLoc[0] = 112 - int(portraitImage.get_rect().width / 2)
            backgroundPortraitLoc[1] = Config.SCREEN_SIZE[1] - Config.BORDER_INDENT - portraitImage.get_rect().height
                
            WINDOW.blit(portraitImage, backgroundPortraitLoc)
            WINDOW.blit(self.imageDict["Main Screen Border"], [0, 0])
           
        # Board #
        if "All" in self.drawDict:
            cardFlipIndexList = []
            if "Flip Animation Data List" in self.properties:
                for flipAnimationData in self.properties["Flip Animation Data List"]:
                    cardFlipIndexList.append(flipAnimationData["Board Slot"])
        
            cardSize = self.imageDict["Cards"]["Template"].get_rect().size
            for i, boardButton in enumerate(self.boardButtonList):
                boardButton.draw(WINDOW)
                if i < len(self.properties["Board"]) and self.properties["Board"][i] != None:
                    boardCard = self.properties["Board"][i]
                    
                    # Flip Animation #
                    if i in cardFlipIndexList:
                        flipAnimationData = self.properties["Flip Animation Data List"][cardFlipIndexList.index(i)]
                        flipCardSize = flipAnimationData["Card Flip Image"].get_rect().size
                        flipCardLocation = [boardButton.rect.left + 8, boardButton.rect.top + 8]
                        flipCardLocation[0] += ((cardSize[0] - flipCardSize[0]) / 2)
                        
                        animationPercent = flipAnimationData["Animation Timer"] / flipAnimationData["Animation Timer Max"]
                        animationPercentFlip = animationPercent / 2
                        if flipAnimationData["Animation Timer Count"] == 1:
                            animationPercentFlip += .5
                        yMod = SystemMath.sin(SystemMath.radians(animationPercentFlip * 180)) * -12
                        flipCardLocation[1] += yMod
                        
                        WINDOW.blit(flipAnimationData["Card Flip Image"], flipCardLocation)
                        
                    # Not Flip Animation #
                    else:
                        WINDOW.blit(self.imageDict["Cards"][boardCard.id][boardCard.targetPlayer], [boardButton.rect.left + 8, boardButton.rect.top + 8])
                        if "Board Element List" in self.properties and self.properties["Board Element List"][i] != None:
                            elementLabelLocation = [boardButton.rect.left, boardButton.rect.top]
                            if self.properties["Board Element List"][i] == boardCard.element:
                                elementLabelImage = self.imageDict["Plus 1"]
                            else : elementLabelImage = self.imageDict["Minus 1"]
                            elementLabelImageRect = elementLabelImage.get_rect()
                            elementLabelLocation[0] += (boardButton.rect.width / 2) - (elementLabelImageRect.width / 2)
                            elementLabelLocation[1] += (boardButton.rect.height / 2) - (elementLabelImageRect.height / 2)
                            WINDOW.blit(elementLabelImage, elementLabelLocation)
                            
                        if self.properties["Rule Label Animation Data"] != None and i in self.properties["Rule Label Animation Data"]["Shine Index List"]:
                            WINDOW.blit(shineMaskCopy, [boardButton.rect.left + 8, boardButton.rect.top + 8])
                                
                # Board Element Icons #
                elif "Board Element List" in self.properties and self.properties["Board Element List"][i] != None:
                    elementID = self.properties["Board Element List"][i]
                    if elementID in self.imageDict["Element Icon"]:
                        elementImage = self.imageDict["Element Icon"][elementID]
                        elementImageRect = elementImage.get_rect()
                        elementImageLoc = [boardButton.rect.left, boardButton.rect.top]
                        elementImageLoc[0] += (boardButton.rect.width / 2) - (elementImageRect.width / 2)
                        elementImageLoc[1] += (boardButton.rect.height / 2) - (elementImageRect.height / 2)
                        WINDOW.blit(elementImage, elementImageLoc)
          
        # Dealing Cards Game Phase #
        if self.properties["Game Phase"] == "Deal Cards" and "Deal Cards Animation Data" in self.properties:
            
            # Get Data #
            currentPlayer = self.properties["Deal Cards Animation Data"]["Current Player"]
            handIndex = self.properties["Deal Cards Animation Data"]["Current Card Index"]
            if currentPlayer == "Player":
                targetHandButtonList = self.playerHandButtonList
                dealingCardData = self.properties["Player Hand"][handIndex]
            else:
                targetHandButtonList = self.npcHandButtonList
                dealingCardData = self.properties[currentPlayer + " Hand"][handIndex]
                
            endLocation = [targetHandButtonList[handIndex].rect.left, targetHandButtonList[handIndex].rect.top]
            startLocation = [(windowSize[0] / 2) - (cardSize[0] / 2), (windowSize[1] / 2) - (cardSize[1] / 2)]
            currentLocation = [endLocation[0] - startLocation[0], endLocation[1] - startLocation[1]]
            animationPercent = self.properties["Deal Cards Animation Data"]["Card Animation Timer"] / self.properties["Deal Cards Animation Data"]["Card Animation Timer Max"]
            currentLocation[0] = startLocation[0] + (currentLocation[0] * animationPercent)
            currentLocation[1] = startLocation[1] + (currentLocation[1] * animationPercent)
            
            # Display Cards Already Dealt #
            for i, targetPlayer in enumerate(self.properties["Deal Cards Animation Data"]["Player List"]):
                if targetPlayer == "Player" : targetHandButtonList = self.playerHandButtonList
                else : targetHandButtonList = self.npcHandButtonList
                currentPlayerIndex = self.properties["Deal Cards Animation Data"]["Player List"].index(self.properties["Deal Cards Animation Data"]["Current Player"])
                
                if i <= currentPlayerIndex:
                    dealtHandEndIndex = handIndex
                    if i < currentPlayerIndex and targetPlayer[0:3] != "NPC":
                        dealtHandEndIndex = self.properties["Deal Cards Animation Data"]["Hand Size"]
                    for dealtHandIndex, handButton in enumerate(targetHandButtonList[0:dealtHandEndIndex]):
                        dealtCardImage = self.imageDict["Cards"]["Back"]
                        if targetPlayer == "Player" or "Open" in self.properties["Rule List"]:
                            dealtCardData = self.properties[targetPlayer + " Hand"][dealtHandIndex]
                            dealtCardImage = self.imageDict["Cards"][dealtCardData.id][dealtCardData.targetPlayer]
                        WINDOW.blit(dealtCardImage, [handButton.rect.left, handButton.rect.top])
            
            # Display Center Card #
            if not (self.properties["Deal Cards Animation Data"]["Player List"].index(currentPlayer) == len(self.properties["Deal Cards Animation Data"]["Player List"]) - 1 and handIndex == len(targetHandButtonList) - 1):
                WINDOW.blit(self.imageDict["Cards"]["Back"], startLocation)
            
            # Display Cards Being Dealt #
            if "Open" in self.properties["Rule List"] or self.properties["Deal Cards Animation Data"]["Current Player"] == "Player" and dealingCardData.id in self.imageDict["Cards"]:
               dealingCardImage = self.imageDict["Cards"][dealingCardData.id][dealingCardData.targetPlayer]
            else : dealingCardImage = self.imageDict["Cards"]["Back"]
            WINDOW.blit(dealingCardImage, currentLocation)
          
        # Player Hand #
        if self.properties["Game Phase"] == "Playing":
            playerCardLocation = [Config.SCREEN_SIZE[0] - cardSize[0] - 30, 30]
            for i, playerCard in enumerate(self.properties["Player Hand"]):
                if not (hoverTargetPlayer == "Player" and clickIndex == -1 and hoverCard != None and handIndex == i) and clickIndex != i and not ("Flying Card" in self.properties and self.properties["Flying Card"]["Hand Index"] == i):
                    if playerCard.id in self.imageDict["Cards"]:
                        WINDOW.blit(self.imageDict["Cards"][playerCard.id][playerCard.targetPlayer], playerCardLocation)
                playerCardLocation[1] += handCardSpaceHeight
            
        # NPC Hand #
        if self.properties["Game Phase"] == "Playing":
            npcCardLocation = [30, 30]
            npcHandID = self.properties["NPC Hand Display ID"]
            if npcHandID in self.properties:
                for i, npcCard in enumerate(self.properties[npcHandID]):
                    if not (hoverTargetPlayer == "NPC" and clickIndex == -1 and hoverCard != None and handIndex == i and self.properties["Current Turn"] == "Player" and "Open" in self.properties["Rule List"]) \
                    and not ("NPC Turn" in self.properties and self.properties["NPC Turn"]["Current Card Choice Index"] == i):
                        if npcCard.id in self.imageDict["Cards"]:
                            npcCardImage = self.imageDict["Cards"]["Back"]
                            if "Open" in self.properties["Rule List"]:
                                npcCardImage = self.imageDict["Cards"][npcCard.id][npcCard.targetPlayer]
                            WINDOW.blit(npcCardImage, npcCardLocation)
                    npcCardLocation[1] += handCardSpaceHeight
                    
        # NPC Current Card Choice #
        if "All" in self.drawDict:
            if "NPC Turn" in self.properties and self.properties["NPC Turn"]["Animation State"] != "Drag Card":
                if self.properties["NPC Turn"]["Current Card Choice Index"] < len(self.properties["NPC 1 Hand"]) and self.properties["NPC Turn"]["Current Card Choice Index"] < len(self.npcHandButtonList):
                    npcHandID = self.properties["NPC Hand Display ID"]
                    npcChoiceCard = self.properties[npcHandID][self.properties["NPC Turn"]["Current Card Choice Index"]]
                    if npcChoiceCard.id in self.imageDict["Cards"]:
                        npcChoiceButtonRect = self.npcHandButtonList[self.properties["NPC Turn"]["Current Card Choice Index"]].rect
                        npcChoiceCardLocation = [npcChoiceButtonRect.left + 20, npcChoiceButtonRect.top]
                        npcChoiceCardImage = self.imageDict["Cards"]["Back"]
                        if "Open" in self.properties["Rule List"]:
                            npcChoiceCardImage = self.imageDict["Cards"][npcChoiceCard.id][npcChoiceCard.targetPlayer]
                        WINDOW.blit(npcChoiceCardImage, npcChoiceCardLocation)
                        WINDOW.blit(self.imageDict["Hover Image"]["Cursor Left"], [npcChoiceCardLocation[0] + 125, npcChoiceCardLocation[1]])
            
        # NPC Moving Card To Board #
        if "All" in self.drawDict:
            if "NPC Turn" in self.properties and self.properties["NPC Turn"]["Animation State"] == "Drag Card":
                targetCardIndex = self.properties["NPC Turn"]["Final Card Choice Index"]
                npcHandID = self.properties["NPC Hand Display ID"]
                if targetCardIndex < len(self.properties[npcHandID]):
                    targetCard = self.properties[npcHandID][targetCardIndex]
                    if targetCard.id in self.imageDict["Cards"]:
                        targetCardImage = self.imageDict["Cards"][targetCard.id][targetCard.targetPlayer]
                        if targetCardIndex < len(self.npcHandButtonList):
                            targetHandButtonRect = self.npcHandButtonList[targetCardIndex].rect
                            targetCardLocation = [targetHandButtonRect.left + 20, targetHandButtonRect.top]
                            targetBoardSlot = self.properties["NPC Turn"]["Board Choice Index"]
                            if targetBoardSlot < len(self.boardButtonList):
                                boardSlotButton = self.boardButtonList[targetBoardSlot]
                                dragPercent = self.properties["NPC Turn"]["Drag Card Timer"] / self.properties["NPC Turn"]["Drag Card Timer Max"]
                                yOffset = SystemMath.sin(SystemMath.radians(dragPercent * 180)) * -40
                                targetCardLocation[0] += (boardSlotButton.rect.left - targetCardLocation[0] + 8) * dragPercent
                                targetCardLocation[1] += ((boardSlotButton.rect.top - targetCardLocation[1] + 8) * dragPercent) + yOffset
                                WINDOW.blit(targetCardImage, targetCardLocation)
                        
        # Mouse Hover Card #
        if self.properties["Game Phase"] == "Playing":
            if hoverCard != None and not (MOUSE.clickElement != None and ' '.join(MOUSE.clickElement.id.split()[1:-1]) == "Hand Button") \
            and not (self.properties["Current Turn"][0:3] == "NPC" and MOUSE.hoverElement != None and MOUSE.hoverElement.id[0:15] == "NPC Hand Button") \
            and not ("Open" not in self.properties["Rule List"] and MOUSE.hoverElement != None and MOUSE.hoverElement.id[0:15] == "NPC Hand Button"):
                if hoverCard.id in self.imageDict["Cards"]:
                    hoverCardX = Config.SCREEN_SIZE[0] - cardSize[0] - 50
                    if MOUSE.hoverElement.id.split()[0] == "NPC":
                        hoverCardX = 50
                    WINDOW.blit(self.imageDict["Cards"][hoverCard.id][hoverCard.targetPlayer], [hoverCardX, MOUSE.hoverElement.rect.top])
           
        # Player Selected Card (Click & Drag) #
        if MOUSE.clickElement != None and MOUSE.clickElement.id[0:18] == "Player Hand Button":
            if MOUSE.clickElement.id.split()[-1].isdigit():
                clickHandIndex = int(MOUSE.clickElement.id.split()[-1])
                if clickHandIndex > -1 and clickHandIndex < len(self.properties["Player Hand"]):
                    clickCard = self.properties["Player Hand"][clickHandIndex]
                    if clickCard.id in self.imageDict["Cards"]:
                        clickCardLocation = [MOUSE.x - 20, MOUSE.y]
                        if "Click Drag Card Offset" in MOUSE.properties:
                            clickCardLocation[0] -= MOUSE.properties["Click Drag Card Offset"][0]
                            clickCardLocation[1] -= MOUSE.properties["Click Drag Card Offset"][1]
                        WINDOW.blit(self.imageDict["Cards"][clickCard.id][clickCard.targetPlayer], clickCardLocation)
            
        # Card Flying Back To Player Hand (Click, Drag & Release Card) #
        if "Flying Card" in self.properties and "Card Data" in self.properties["Flying Card"] and self.properties["Flying Card"]["Card Data"].id in self.imageDict["Cards"]:
            if self.properties["Flying Card"]["Move Timer"] == 0 : movePercent = 0
            else : movePercent = self.properties["Flying Card"]["Move Timer"] / self.properties["Flying Card"]["Move Timer Max"]
            flyingCardLocation = [self.properties["Flying Card"]["Start Location"][0], self.properties["Flying Card"]["Start Location"][1]]
            flyingCardLocation[0] += self.properties["Flying Card"]["Travel Distance"][0] * movePercent
            flyingCardLocation[1] += self.properties["Flying Card"]["Travel Distance"][1] * movePercent
            flyingCardData = self.properties["Flying Card"]["Card Data"]
            WINDOW.blit(self.imageDict["Cards"][flyingCardData.id][flyingCardData.targetPlayer], flyingCardLocation)
            
        # Rule Labels #
        if "All" in self.drawDict:
            labelImage = None
            if self.properties["Rule Label Animation Data"] != None:
                labelID = self.properties["Rule Label Animation Data"]["Label ID"]
                if labelID in self.imageDict:
                    labelImage = self.imageDict[labelID]
                    labelImageRect = labelImage.get_rect()
              
            if labelImage != None:
                ruleLabelLocation = [0, 0]
                
                tempRuleAnimationPercent = 0.0
                if "Rule Label Animation Data" in self.properties:
                    tempRuleAnimationPercent = self.properties["Rule Label Animation Data"]["Animation Timer"] / (self.properties["Rule Label Animation Data"]["Animation Timer Max"] - 20)
                    if tempRuleAnimationPercent > 1.0 : tempRuleAnimationPercent = 1.0
                ruleLabelLocation[0] = (Config.SCREEN_SIZE[0] / 2) - (labelImageRect.width / 2)
                if self.properties["Rule Label Animation Data"]["Animation Timer Count"] == 0:
                    ruleLabelLocation[0] += (1 - tempRuleAnimationPercent) * (Config.SCREEN_SIZE[0] - ruleLabelLocation[0])
                elif self.properties["Rule Label Animation Data"]["Animation Timer Count"] == 1:
                    ruleLabelLocation[0] -= (tempRuleAnimationPercent) * (Config.SCREEN_SIZE[0] - ruleLabelLocation[0])
                ruleLabelLocation[1] = (Config.SCREEN_SIZE[1] / 2) - (labelImageRect.height / 2)
                WINDOW.blit(labelImage, ruleLabelLocation)
            
        # Deck Choice Menu #
        if self.properties["Game Phase"] == "Deck Select":
            deckChoiceMenuLoc = [0, 0]
            deckSelectionTextBoxRect = self.imageDict["Deck Select Text Box"].get_rect()
            deckChoiceMenuLoc[0] = (Config.SCREEN_SIZE[0] / 2) - (deckSelectionTextBoxRect.width / 2)
            deckChoiceMenuLoc[1] = (Config.SCREEN_SIZE[1] / 2) - (deckSelectionTextBoxRect.height / 2)
            WINDOW.blit(self.imageDict["Deck Select Text Box"], deckChoiceMenuLoc)
            
            if "Deck Select Text Box Button List" in self.properties:
                for deckSelectButton in self.properties["Deck Select Text Box Button List"]:
                    deckSelectButton.draw(WINDOW, self.imageDict["Hover Image"])
            
    def mouseClick(self, WINDOW, MOUSE):
    
        if MOUSE.clickElement != None:
            
            # Click Deck Select Button #
            if MOUSE.clickElement.id[0:23] == "Deck Select Menu Button":
                self.properties["Player Hand"] = self.loadHand("Player", self.properties["Max Hand Size"])
                self.playerHandButtonList = self.loadHandButtonList("Player", WINDOW)
                del self.properties["Deck Select Text Box Button List"]
                
                dealCardsAnimationData = {}
                dealCardsAnimationData["Card Animation Timer"] = 0
                dealCardsAnimationData["Card Animation Timer Max"] = 10
                dealCardsAnimationData["Current Card Index"] = 0
                dealCardsAnimationData["Hand Size"] = self.properties["Max Hand Size"]
                dealCardsAnimationData["Player List"] = self.properties["Player List"]
                dealCardsAnimationData["Current Player"] = self.properties["Current Turn"]
                
                self.properties["Deal Cards Animation Data"] = dealCardsAnimationData
                self.properties["Game Phase"] = "Deal Cards"
            
            # Click Player Hand #
            elif MOUSE.clickElement.id[0:18] == "Player Hand Button":
                MOUSE.properties["Click Drag Card Offset"] = [0, 0]
                MOUSE.properties["Click Drag Card Offset"][0] = MOUSE.x - MOUSE.clickElement.rect.left
                MOUSE.properties["Click Drag Card Offset"][1] = MOUSE.y - MOUSE.clickElement.rect.top
                
            # Click Card On Board (Deactivated) #
            elif False and MOUSE.clickElement.id[0:17] == "Board Slot Button":
                targetBoardSlot = None
                if MOUSE.clickElement.id.split()[-1].isdigit() and int(MOUSE.clickElement.id.split()[-1]) < len(self.properties["Board"]):
                    targetBoardSlot = int(MOUSE.clickElement.id.split()[-1])
                    if self.properties["Board"][targetBoardSlot] != None:
                        
                        # Get Data #
                        cardFlipIndexList = []
                        if "Flip Animation Data List" in self.properties:
                            for flipAnimationData in self.properties["Flip Animation Data List"]:
                                cardFlipIndexList.append(flipAnimationData["Board Slot"])
                        
                        # Initiate Flip Animation #
                        if targetBoardSlot not in cardFlipIndexList:
                            if "Flip Animation Data List" not in self.properties:
                                self.properties["Flip Animation Data List"] = []
                                
                            targetCard = self.properties["Board"][targetBoardSlot]
                            cardFlipImage = self.imageDict["Cards"]["Template"]
                            if targetCard.id in self.imageDict["Cards"]:
                                cardFlipImage = self.imageDict["Cards"][targetCard.id][targetCard.targetPlayer]
                            flipAnimationData = {"Board Slot": targetBoardSlot, "Card Flip Image": cardFlipImage, "Card Flip Image Base": cardFlipImage, "Animation Timer": 0, "Animation Timer Max": 12, "Animation Timer Count": 0}
                            self.properties["Flip Animation Data List"].append(flipAnimationData)
            
    def mouseClickUp(self, WINDOW, MOUSE):
        
        # Pick Up Card From Hand #
        if MOUSE.clickElement != None and MOUSE.clickElement.id[0:18] == "Player Hand Button":
            targetBoardSlot = None
            if MOUSE.hoverElement != None and MOUSE.hoverElement.id[0:17] == "Board Slot Button" and MOUSE.hoverElement.id.split()[-1].isdigit() and int(MOUSE.hoverElement.id.split()[-1]) < len(self.properties["Board"]):
                targetBoardSlot = int(MOUSE.hoverElement.id.split()[-1])
            
            # Place Card On Board #
            if self.properties["Current Turn"] == "Player" and targetBoardSlot != None and self.properties["Board"][targetBoardSlot] == None:
                handIndex = int(MOUSE.clickElement.id.split()[-1])
                if handIndex < len(self.properties["Player Hand"]):
                    
                    # Add Card To Board #
                    dropCard = self.properties["Player Hand"][handIndex]
                    self.properties["Board"][targetBoardSlot] = dropCard
                    
                    # Remove Card From Hand #
                    del self.properties["Player Hand"][handIndex]
                    self.playerHandButtonList = self.loadHandButtonList("Player", WINDOW)
                    
                    # Card Flips OR Update Turn Status #
                    if self.initiateCardFlips(targetBoardSlot) == False:
                        self.loadNextTurn(WINDOW)
                
            # Fly Card Back To Hand #
            else:
            
                # Get Slope (Currently Unused) #
                xx = MOUSE.clickElement.rect.left - (MOUSE.x - MOUSE.properties["Click Drag Card Offset"][0])
                yy = MOUSE.clickElement.rect.top - (MOUSE.y - MOUSE.properties["Click Drag Card Offset"][1])
                if yy == 0 : slope = 0
                else : slope = xx / yy
                
                # Get Card Data #
                if MOUSE.clickElement.id.split()[-1].isdigit():
                    handIndex = int(MOUSE.clickElement.id.split()[-1])
                    if handIndex < len(self.properties["Player Hand"]):
                        cardData = self.properties["Player Hand"][handIndex]
                        startLocation = [MOUSE.x, MOUSE.y]
                        moveTimerMax = int((abs(xx) + abs(yy)) / 70) + 1
                        if "Click Drag Card Offset" in MOUSE.properties:
                            startLocation[0] -= (MOUSE.properties["Click Drag Card Offset"][0] + 20)
                            startLocation[1] -= MOUSE.properties["Click Drag Card Offset"][1]
                        self.properties["Flying Card"] = {"Hand Index": handIndex, "Start Location": startLocation, "Travel Distance": [xx, yy], "Card Data": cardData, "Move Timer": 0, "Move Timer Max": moveTimerMax}
            
        if "Click Drag Card Offset" in MOUSE.properties:
            del MOUSE.properties["Click Drag Card Offset"]
        
        if "All" not in self.drawDict:
            self.drawDict["All"] = True
        
    def mouseMove(self, MOUSE):
        
        if MOUSE.clickElement != None and MOUSE.clickElement.id[0:18] == "Player Hand Button":
            if "All" not in self.drawDict:
                self.drawDict["All"] = True
                
    # Class Functions #
    def initiateCardFlips(self, BOARD_INDEX):
    
        targetCard = self.properties["Board"][BOARD_INDEX]
        cardLocMod = [-3, 1, 3, -1]
        attackFlipIndexList = [-1, -1, -1, -1]
        sameFlipIndexList = [-1, -1, -1, -1]
        plusDictList = {}
        shineIndexList = []
        cardFlipCheck = False
        wallRuleCheck = "Same Wall" in self.properties["Rule List"] or "Plus Wall" in self.properties["Rule List"]
        
        if targetCard != None:
        
            # Get Flip Data #
            for i in range(4):
                sideCard = None
                sideIndex = BOARD_INDEX + cardLocMod[i]
                targetCardAttack = targetCard.getAttackPower(i, BOARD_INDEX, self.properties)
                
                # Side Is A Wall #
                if wallRuleCheck and (sideIndex < 0 or sideIndex > 8 or (i == 1 and BOARD_INDEX in [2, 5, 8]) or (i == 3 and BOARD_INDEX in [0, 3, 6])):
                    sideCard = Card.Load(0, None)
                
                # Side Card Is Inside Board #
                elif sideIndex >= 0 and sideIndex < 9 and not (i == 1 and BOARD_INDEX in [2, 5, 8]) and not (i == 3 and BOARD_INDEX in [0, 3, 6]):
                    if self.properties["Board"][sideIndex] != None:
                        sideCard = self.properties["Board"][sideIndex]
                        
                if sideCard != None:
                    if sideCard.id == "Wall Card" : sideCardDefense = 10
                    else : sideCardDefense = sideCard.getDefense(i, sideIndex, self.properties)
                    
                    # Plus Check #
                    if "Plus" in self.properties["Rule List"] and not (sideCard.id == "Wall Card" and "Plus Wall" not in self.properties["Rule List"]):
                        plusNum = targetCardAttack + sideCardDefense
                        if plusNum not in plusDictList : plusDictList[plusNum] = 1
                        else : plusDictList[plusNum] += 1
                            
                    # Same Check #
                    if "Same" in self.properties["Rule List"] and not (sideCard.id == "Wall Card" and "Same Wall" not in self.properties["Rule List"]):
                        if targetCardAttack == sideCardDefense:
                            if sideCard.id == "Wall Card" : sameFlipIndexList[i] = "Wall Card"
                            else : sameFlipIndexList[i] = sideIndex
                    
                    # Attack/Defense Check #
                    if sideCard.id != "Wall Card" and targetCard.targetPlayer != sideCard.targetPlayer and targetCardAttack > sideCardDefense:
                        attackFlipIndexList[i] = sideIndex
        
            # Plus Flip Check #
            if plusDictList != {}:
                shineIndexList = []
                for i in range(4):
                    sideIndex = BOARD_INDEX + cardLocMod[i]
                    if sideIndex >= 0 and sideIndex < 9 and not (i == 1 and BOARD_INDEX in [2, 5, 8]) and not (i == 3 and BOARD_INDEX in [0, 3, 6]):
                        if self.properties["Board"][sideIndex] != None:
                            sideCard = self.properties["Board"][sideIndex]
                            if sideCard.id != "Wall Card":
                                plusNum = targetCard.getAttackPower(i, BOARD_INDEX, self.properties) + sideCard.getDefense(i, sideIndex, self.properties)
                                if sideCard.targetPlayer != targetCard.targetPlayer:
                                    if plusNum in plusDictList and plusDictList[plusNum] >= 2:
                                        shineIndexList.append(sideIndex)
                                        cardFlipCheck = True
                                        
                if shineIndexList != []:
                    ruleLabelAnimationData = {"Label ID": "Plus Label", "Animation Timer": 0, "Animation Timer Max": 30, "Animation Timer Count": 0, "Parent Card": targetCard, "Shine Index List": shineIndexList}
                    self.properties["Rule Label Animation Data"] = ruleLabelAnimationData
               
            # Same Flip Check #
            if sameFlipIndexList != [-1, -1, -1, -1]:
                sameFlipNumberDict = {}
                sameFlipPlayerCheckDict = {}
                for i, flipIndex in enumerate(sameFlipIndexList):
                    if flipIndex != -1:
                        cardAttack = targetCard.getAttackPower(i, BOARD_INDEX, self.properties)
                        if cardAttack not in sameFlipNumberDict : sameFlipNumberDict[cardAttack] = 1
                        else : sameFlipNumberDict[cardAttack] += 1
                        
                        if flipIndex != "Wall Card":
                            sideCard = self.properties["Board"][flipIndex]
                            if sideCard.targetPlayer != targetCard.targetPlayer:
                                sameFlipPlayerCheckDict[cardAttack] = True
                        
                shineIndexList = []
                for i, flipIndex in enumerate(sameFlipIndexList):
                    if flipIndex != -1 and flipIndex != "Wall Card":
                        sideCard = self.properties["Board"][flipIndex]
                        if sideCard.getDefense(i, flipIndex, self.properties) in sameFlipNumberDict and sameFlipNumberDict[sideCard.getDefense(i, flipIndex, self.properties)] >= 2 and sideCard.getDefense(i, flipIndex, self.properties) == targetCard.getAttackPower(i, BOARD_INDEX, self.properties):
                            if sideCard.getDefense(i, flipIndex, self.properties) in sameFlipPlayerCheckDict:
                                shineIndexList.append(flipIndex)
                                cardFlipCheck = True
                      
                if shineIndexList != []:
                    ruleLabelAnimationData = {"Label ID": "Same Label", "Animation Timer": 0, "Animation Timer Max": 30, "Animation Timer Count": 0, "Parent Card": targetCard, "Shine Index List": shineIndexList}
                    self.properties["Rule Label Animation Data"] = ruleLabelAnimationData
                                                  
            # Regular Card Flip Animations #
            if attackFlipIndexList != [-1, -1, -1, -1]:
                oldCardFlipIndexList = []
                for flipAnimationData in self.properties["Flip Animation Data List"]:
                    oldCardFlipIndexList.append(flipAnimationData["Board Slot"])
                
                # Initiate Flip Animation #
                for flipIndex in attackFlipIndexList:
                    if flipIndex != -1 and flipIndex not in oldCardFlipIndexList and flipIndex not in shineIndexList:
                        self.loadFlipAnimation(targetCard, flipIndex)
                        cardFlipCheck = True

        return cardFlipCheck
             
    def loadFlipAnimation(self, TARGET_CARD, FLIP_INDEX, SAME_PLUS_CHECK=False):
        
        sideCard = self.properties["Board"][FLIP_INDEX]
        cardFlipImage = self.imageDict["Cards"]["Template"]
        if sideCard.id in self.imageDict["Cards"]:
            cardFlipImage = self.imageDict["Cards"][sideCard.id][sideCard.targetPlayer]
        flipAnimationData = {"Target Card": sideCard, "New Target Player": TARGET_CARD.targetPlayer, "Board Slot": FLIP_INDEX, "Card Flip Image": cardFlipImage, "Card Flip Image Base": cardFlipImage, "Animation Timer": 0, "Animation Timer Max": 12, "Animation Timer Count": 0, "Same/Plus Check": SAME_PLUS_CHECK}
        self.properties["Flip Animation Data List"].append(flipAnimationData)
         
    def loadNextTurn(self, WINDOW):
    
        currentPlayerIndex = self.properties["Player List"].index(self.properties["Current Turn"])
        
        if currentPlayerIndex == len(self.properties["Player List"]) - 1:
            self.properties["Current Turn"] = self.properties["Player List"][0]
        else:
            self.properties["Current Turn"] = self.properties["Player List"][currentPlayerIndex + 1]
            
        if self.properties["Current Turn"][0:3] == "NPC":
            self.loadNPCTurn(self.properties["Current Turn"])
            self.properties["NPC Hand Display ID"] = self.properties["Current Turn"] + " Hand"
        
        npcHandID = ' '.join(self.properties["NPC Hand Display ID"].split()[0:2])
        self.npcHandButtonList = self.loadHandButtonList(npcHandID, WINDOW)
            
    def loadNPCTurn(self, TARGET_PLAYER):
        
        self.properties["Combo Label Activated"] = False
        
        boardChoiceIndexList = []
        for i, boardSlot in enumerate(self.properties["Board"]):
            if boardSlot == None:
                boardChoiceIndexList.append(i)
        
        if boardChoiceIndexList != []:
            self.properties["Current Turn"] = TARGET_PLAYER
            self.properties["NPC Turn"] = {}
            self.properties["NPC Turn"]["Animation State"] = "Choose Card"
            self.properties["NPC Turn"]["Current Card Choice Index"] = 0
            self.properties["NPC Turn"]["Current Card Choice Timer"] = 0
            self.properties["NPC Turn"]["Current Card Choice Timer Max"] = random.randrange(15, 45)
            
            aiChoiceData = self.getAIChoiceData()
            self.properties["NPC Turn"]["Final Card Choice Index"] = aiChoiceData["Final Card Choice Index"]
            self.properties["NPC Turn"]["Board Choice Index"] = aiChoiceData["Board Choice Index"]
        
            # Calculate Drag Card Time (Using Slope) #
            if True:
                targetCardIndex = self.properties["NPC Turn"]["Final Card Choice Index"]
                startPosRect = self.npcHandButtonList[targetCardIndex].rect
                boardSlotButton = self.boardButtonList[self.properties["NPC Turn"]["Board Choice Index"]]
                boardSlotPos = [boardSlotButton.rect.left + 8, boardSlotButton.rect.top + 8]

                xx = startPosRect.left - boardSlotPos[0]
                yy = startPosRect.top - boardSlotPos[1]
                moveTimerMax = int((abs(xx) + abs(yy)) / 20) + 1
                self.properties["NPC Turn"]["Drag Card Timer Max"] = moveTimerMax
                self.properties["NPC Turn"]["Drag Card Timer"] = 0
                 
    def getAIChoiceData(self):
    
        # Get Choice Data #
        choiceDataList = []
        cardLocMod = [-3, 1, 3, -1]
        targetPlayer = self.properties["Current Turn"]
        if targetPlayer + " Hand" in self.properties:
            for choiceCardIndex, choiceCard in enumerate(self.properties[targetPlayer + " Hand"]):
                for boardIndex in range(len(self.properties["Board"])):
                    if self.properties["Board"][boardIndex] == None:
                        boardSlot = self.properties["Board"][boardIndex]
                        
                        choiceDataDict = {}
                        choiceDataDict["Card Flip Index List"] = [-1, -1, -1, -1]
                        choiceDataDict["Flipped Sides"] = 0
                        choiceDataDict["Exposed Sides"] = 0
                        choiceDataDict["Total Defense"] = 0
                        choiceDataDict["Final Card Choice Index"] = choiceCardIndex
                        choiceDataDict["Board Choice Index"] = boardIndex
                        
                        for i in range(4):
                            sideIndex = boardIndex + cardLocMod[i]
                            if sideIndex >= 0 and sideIndex < 9 and not (i == 1 and boardIndex in [2, 5, 8]) and not (i == 3 and boardIndex in [0, 3, 6]):
                                choiceCardAttack = choiceCard.getAttackPower(i, boardIndex, self.properties)
                                if self.properties["Board"][sideIndex] == None:
                                    choiceDataDict["Exposed Sides"] += 1
                                    choiceDataDict["Total Defense"] += choiceCardAttack
                                else:
                                    sideCard = self.properties["Board"][sideIndex]
                                    sideCardDefense = sideCard.getDefense(i, sideIndex, self.properties)
                                    
                                    if choiceCardAttack > sideCardDefense and choiceCard.targetPlayer != sideCard.targetPlayer:
                                        choiceDataDict["Flipped Sides"] += 1
                                        choiceDataDict["Card Flip Index List"][i] = sideIndex
                        
                        choiceDataList.append(choiceDataDict)
                        
        # Calculate Turn Choice #
        if choiceDataList != []:
            currentChoiceData = choiceDataList[0]
            if len(choiceDataList) > 1:
                for newChoiceData in choiceDataList[1::]:
                    
                    if newChoiceData["Flipped Sides"] > currentChoiceData["Flipped Sides"]:
                        currentChoiceData = newChoiceData
                    elif newChoiceData["Flipped Sides"] == currentChoiceData["Flipped Sides"]:
                        if newChoiceData["Exposed Sides"] < currentChoiceData["Exposed Sides"]:
                            currentChoiceData = newChoiceData
                        elif newChoiceData["Exposed Sides"] == currentChoiceData["Exposed Sides"]:
                            
                            # Get Data #
                            newChoiceTotalDefense = 0
                            if newChoiceData["Exposed Sides"] > 0:
                                newChoiceTotalDefense = newChoiceData["Total Defense"] / newChoiceData["Exposed Sides"]
                            currentChoiceTotalDefense = 0
                            if currentChoiceData["Exposed Sides"] > 0:
                                currentChoiceTotalDefense = currentChoiceData["Total Defense"] / currentChoiceData["Exposed Sides"]
                            
                            if newChoiceTotalDefense > currentChoiceTotalDefense:
                                currentChoiceData = newChoiceData
                          
            return currentChoiceData
                     
    def getCurrentHoverButton(self):
    
        targetButton = None
        
        return targetButton
    
    def keyPress(self, SCREEN_LEVEL, PLAYER, MOUSE, KEYBOARD, KEY):
        
        pass
        
    def resetActiveHoverVariables(self, RESET_SUBSCREEN=True):
    
        if "Deck Select Text Box Button List" in self.properties:
            for deckSelectButton in self.properties["Deck Select Text Box Button List"]:
                deckSelectButton.properties["Hover Active"] = False
        
    def getElementList(self, SCREEN_LEVEL):
    
        elementList = []
        
        if self.properties["Game Phase"] == "Playing":
            for element in self.boardButtonList:
                elementList.append(element)
            for element in self.playerHandButtonList:
                elementList.append(element)
            for element in self.npcHandButtonList:
                elementList.append(element)
            
        if "Deck Select Text Box Button List" in self.properties:
            for element in self.properties["Deck Select Text Box Button List"]:
                elementList.append(element)
    
        return elementList
        