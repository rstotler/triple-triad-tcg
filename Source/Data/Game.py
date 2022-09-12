import pygame
from pygame import *
from Data import Player, Location

class Load:
    
    def __init__(self):
    
        self.screenLevel = "Main Menu"
        self.lastTownID = None
        
        self.playerData = Player.Load()
        self.locationDataDict = self.loadLocationDataDict()
        
    def loadLocationDataDict(self):
    
        locationDataDict = {}
        
        for townName in ["House A.", "Kohlingen", "Narshe", "Zozo", "Jidoor", "Opera House", "Figaro", "S. Figaro", \
                         "Cabin", "Hideout", "Nikeah", "House B.", "Doma Castle", "Mobliz", "Thamasa", "Tzen", \
                         "Vector", "Albrook", "House C.", "Maranda"]:
            locationDataDict[townName] = Location.Load(townName)
        
        return locationDataDict
        
    def update(self, WINDOW, SCREEN, MOUSE, KEYBOARD):
    
        if SCREEN.id == "Game Screen":
            
            if "Town Name Text Box Timer" in SCREEN.properties:
                SCREEN.properties["Town Name Text Box Timer"] -= 1
                if SCREEN.properties["Town Name Text Box Timer"] <= 0:
                    del SCREEN.properties["Town Name Text Box Timer"]
                    
                    SCREEN.drawDict["All"] = True
                    
            if "Deck Name Area Hover Timer" in SCREEN.properties and SCREEN.properties["Deck Name Area Hover Timer"] != None:
                SCREEN.properties["Deck Name Area Hover Timer"] += 1
                if SCREEN.properties["Deck Name Area Hover Timer"] >= 120:
                    SCREEN.properties["Deck Name Area Hover Timer"] = 0
                    
                if SCREEN.properties["Deck Name Area Hover Timer"] in [0, 60]:
                    SCREEN.drawDict["All"] = True
                    
                targetDeckIndex = SCREEN.properties["Deck Editor Index"]
                if len(self.playerData.deckNameList[targetDeckIndex]) > 0:
                    if KEYBOARD.backspace and KEYBOARD.backspaceTimer % KEYBOARD.backspaceSpeed == 0:
                        self.playerData.deckNameList[targetDeckIndex] = self.playerData.deckNameList[targetDeckIndex][0:-1]
                        SCREEN.drawDict["All"] = True
                    
        elif SCREEN.id == "Battle":
        
            # Deal Cards Animation #
            if "Deal Cards Animation Data" in SCREEN.properties:
                SCREEN.properties["Deal Cards Animation Data"]["Card Animation Timer"] += 1
                if SCREEN.properties["Deal Cards Animation Data"]["Card Animation Timer"] >= SCREEN.properties["Deal Cards Animation Data"]["Card Animation Timer Max"]:
                    SCREEN.properties["Deal Cards Animation Data"]["Card Animation Timer"] = 0
                    SCREEN.properties["Deal Cards Animation Data"]["Current Card Index"] += 1
                    if SCREEN.properties["Deal Cards Animation Data"]["Current Card Index"] >= SCREEN.properties["Deal Cards Animation Data"]["Hand Size"]:
                    
                        # Next Player #
                        if SCREEN.properties["Deal Cards Animation Data"]["Current Player"] != SCREEN.properties["Deal Cards Animation Data"]["Player List"][-1]:
                            nextPlayerIndex = SCREEN.properties["Deal Cards Animation Data"]["Player List"].index(SCREEN.properties["Deal Cards Animation Data"]["Current Player"]) + 1
                            nextPlayer = SCREEN.properties["Deal Cards Animation Data"]["Player List"][nextPlayerIndex]
                            SCREEN.properties["Deal Cards Animation Data"]["Current Player"] = nextPlayer
                            SCREEN.properties["Deal Cards Animation Data"]["Current Card Index"] = 0
                        
                        # Animation End #
                        else:
                            SCREEN.properties["Game Phase"] = "Playing"
                            del SCREEN.properties["Deal Cards Animation Data"]
                            
                            if SCREEN.properties["Current Turn"] != "Player":
                                SCREEN.loadNPCTurn(SCREEN.properties["Current Turn"])
                            
                if "All" not in SCREEN.drawDict:
                    SCREEN.drawDict["All"] = True
        
            # Card Flying Back To Player's Hand Animation #
            if "Flying Card" in SCREEN.properties:
                SCREEN.properties["Flying Card"]["Move Timer"] += 1
                if SCREEN.properties["Flying Card"]["Move Timer"] >= SCREEN.properties["Flying Card"]["Move Timer Max"]:
                    del SCREEN.properties["Flying Card"]
                    
                if "All" not in SCREEN.drawDict:
                    SCREEN.drawDict["All"] = True
                 
            # Rule Label Animations #
            if SCREEN.properties["Rule Label Animation Data"] != None:
                SCREEN.properties["Rule Label Animation Data"]["Animation Timer"] += 1
                if SCREEN.properties["Rule Label Animation Data"]["Animation Timer"] >= SCREEN.properties["Rule Label Animation Data"]["Animation Timer Max"]:
                    SCREEN.properties["Rule Label Animation Data"]["Animation Timer Count"] += 1
                    SCREEN.properties["Rule Label Animation Data"]["Animation Timer"] = 0
                    
                    # Animation End #
                    if SCREEN.properties["Rule Label Animation Data"]["Animation Timer Count"] == 2:
                        comboRuleCheck = "Combo" in SCREEN.properties["Rule List"]
                        for flipIndex in SCREEN.properties["Rule Label Animation Data"]["Shine Index List"]:
                            targetCard = SCREEN.properties["Board"][flipIndex]
                            parentCard = SCREEN.properties["Rule Label Animation Data"]["Parent Card"]
                            if targetCard != None and targetCard.targetPlayer != parentCard.targetPlayer:
                                SCREEN.loadFlipAnimation(parentCard, flipIndex, comboRuleCheck)
                        
                        SCREEN.properties["Rule Label Animation Data"] = None
                            
                if "All" not in SCREEN.drawDict:
                    SCREEN.drawDict["All"] = True
                 
            # Card Flip Animations #
            if True:
                flipAnimationDelList = []
                delSlotList = []
                delAnimationCheck = False
                samePlusActive = False
                for i, flipAnimationData in enumerate(SCREEN.properties["Flip Animation Data List"]):
                    if flipAnimationData["Animation Timer Count"] > -1:
                        flipAnimationData["Animation Timer"] += 1
                        
                        cardImageRect = SCREEN.imageDict["Cards"]["Template"].get_rect()
                        flipCardSize = [cardImageRect.width, cardImageRect.height]
                        animationPercent = flipAnimationData["Animation Timer"] / flipAnimationData["Animation Timer Max"]
                        if flipAnimationData["Animation Timer Count"] == 0:
                            animationPercent = 1 - animationPercent
                        flipCardSize[0] = int(flipCardSize[0] * animationPercent)
                        flipAnimationData["Card Flip Image"] = pygame.transform.scale(flipAnimationData["Card Flip Image Base"], flipCardSize)
                        
                        if flipAnimationData["Animation Timer"] >= flipAnimationData["Animation Timer Max"]:
                            
                            # Flip Card #
                            if flipAnimationData["Animation Timer Count"] == 0:
                                flipAnimationData["Animation Timer Count"] += 1
                                flipAnimationData["Animation Timer"] = 0
                                
                                # Update Card Color (Mid-Flip) #
                                targetCard = flipAnimationData["Target Card"]
                                newTargetPlayer = flipAnimationData["New Target Player"]
                                updatedCardImage = SCREEN.imageDict["Cards"][targetCard.id][newTargetPlayer]
                                flipAnimationData["Card Flip Image Base"] = updatedCardImage
                                targetCard.targetPlayer = newTargetPlayer
                                
                            # Animation End #
                            else:
                                flipAnimationDelList.append(i)
                                delSlotList.append(flipAnimationData["Board Slot"])
                                if "Same/Plus Check" in flipAnimationData and flipAnimationData["Same/Plus Check"] == True:
                                    samePlusActive = True
                        
                        if "All" not in SCREEN.drawDict:
                            SCREEN.drawDict["All"] = True
                        
                flipAnimationDelList.reverse()
                for i in flipAnimationDelList:
                    del SCREEN.properties["Flip Animation Data List"][i]
                    delAnimationCheck = True
                
                # Combo/End Turn #
                if delAnimationCheck == True and len(SCREEN.properties["Flip Animation Data List"]) == 0:
                    
                    # Combo Check #
                    comboCheck = False
                    cardLocMod = [-3, 1, 3, -1]
                    if samePlusActive == True and "Combo" in SCREEN.properties["Rule List"] and len(delSlotList) > 0:
                        for boardIndex in delSlotList:
                            if SCREEN.properties["Board"][boardIndex] != None:
                                targetCard = SCREEN.properties["Board"][boardIndex]
                                for i in range(4):
                                    sideIndex = boardIndex + cardLocMod[i]
                                    if sideIndex >= 0 and sideIndex < 9:
                                        if not (i == 1 and boardIndex in [2, 5, 8]) and not (i == 3 and boardIndex in [0, 3, 6]):
                                            if SCREEN.properties["Board"][sideIndex] != None:
                                                sideCard = SCREEN.properties["Board"][sideIndex]
                                                targetCardAttack = targetCard.getAttackPower(i, boardIndex, SCREEN.properties)
                                                sideCardDefense = sideCard.getDefense(i, sideIndex, SCREEN.properties)
                                                
                                                if targetCardAttack > sideCardDefense and targetCard.targetPlayer != sideCard.targetPlayer:
                                                    SCREEN.loadFlipAnimation(targetCard, sideIndex, True)
                                                    comboCheck = True
                                                    if SCREEN.properties["Combo Label Activated"] == False:
                                                        ruleLabelAnimationData = {"Label ID": "Combo Label", "Animation Timer": 0, "Animation Timer Max": 30, "Animation Timer Count": 0, "Parent Card": targetCard, "Shine Index List": []}
                                                        SCREEN.properties["Rule Label Animation Data"] = ruleLabelAnimationData
                                                        SCREEN.properties["Combo Label Activated"] = True

                    # Switch Turn #
                    if comboCheck == False:
                        emptyBoardSlot = False
                        for boardIndex in SCREEN.properties["Board"]:
                            if boardIndex == None:
                                emptyBoardSlot = True
                                break
                                
                        if emptyBoardSlot:
                            SCREEN.loadNextTurn(WINDOW)
                            if SCREEN.properties["Current Turn"][0:3] == "NPC":
                                MOUSE.update(SCREEN, self.screenLevel)

            # NPC Turn #
            if "NPC Turn" in SCREEN.properties:
                
                # Choose Card Animation #
                if SCREEN.properties["NPC Turn"]["Animation State"] == "Choose Card":
                    SCREEN.properties["NPC Turn"]["Current Card Choice Timer"] += 1
                    if SCREEN.properties["NPC Turn"]["Current Card Choice Timer"] >= SCREEN.properties["NPC Turn"]["Current Card Choice Timer Max"]:
                        SCREEN.properties["NPC Turn"]["Current Card Choice Timer"] = 0
                        SCREEN.properties["NPC Turn"]["Current Card Choice Index"] += 1
                        if SCREEN.properties["NPC Turn"]["Current Card Choice Index"] > SCREEN.properties["NPC Turn"]["Final Card Choice Index"]:
                            SCREEN.properties["NPC Turn"]["Current Card Choice Index"] -= 1
                            SCREEN.properties["NPC Turn"]["Animation State"] = "Drag Card"
                    
                        if "All" not in SCREEN.drawDict:
                            SCREEN.drawDict["All"] = True
    
                # Drag Card To Board Animation #
                elif SCREEN.properties["NPC Turn"]["Animation State"] == "Drag Card":
                    SCREEN.properties["NPC Turn"]["Drag Card Timer"] += 1
                    if SCREEN.properties["NPC Turn"]["Drag Card Timer"] >= SCREEN.properties["NPC Turn"]["Drag Card Timer Max"]:
                        
                        # Place Card On Board #
                        npcTargetCardHandIndex = SCREEN.properties["NPC Turn"]["Final Card Choice Index"]
                        npcHandID = SCREEN.properties["Current Turn"] + " Hand"
                        if npcHandID in SCREEN.properties:
                            npcTargetCard = SCREEN.properties[npcHandID][npcTargetCardHandIndex]
                            npcTargetBoardIndex = SCREEN.properties["NPC Turn"]["Board Choice Index"]
                            SCREEN.properties["Board"][npcTargetBoardIndex] = npcTargetCard
                            
                            # Remove Card From NPC Hand #
                            del SCREEN.properties[npcHandID][npcTargetCardHandIndex]
                            del SCREEN.properties["NPC Turn"]
                            
                            # Update Turn Status #
                            if SCREEN.initiateCardFlips(npcTargetBoardIndex) == False:
                                SCREEN.loadNextTurn(WINDOW)
                                MOUSE.update(SCREEN, self.screenLevel)
                        
                    if "All" not in SCREEN.drawDict:
                        SCREEN.drawDict["All"] = True
                        