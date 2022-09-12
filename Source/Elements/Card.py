import pygame, random, Config, Utility
from pygame import *

class Load:

    def __init__(self, ID_NUM, TARGET_PLAYER):
    
        self.id = "Default"
        self.idNum = ID_NUM
        self.targetPlayer = TARGET_PLAYER
        self.attackPower = [1, 1, 1, 1]
        self.element = None
        
        self.loadCard()
        
    def loadCard(self):

        if self.idNum == 0 : self.id = "Wall Card"
        elif self.idNum == 1:
            self.id = "Terra Branford"
            self.attackPower = [2, 1, 1, 1]
        elif self.idNum == 2:
            self.id = "Locke Cole"
            self.attackPower = [1, 1, 1, 2]
        elif self.idNum == 3:
            self.id = "Edgar Figaro"
            self.attackPower = [1, 1, 2, 1]
        elif self.idNum == 4:
            self.id = "Cyan Garamonde"
            self.attackPower = [1, 10, 10, 1]
        elif self.idNum == 5:
            self.id = "Celes Chere"
            self.attackPower = [1, 1, 1, 1]
        elif self.idNum == 6:
            self.id = "Shadow"
            self.attackPower = [1, 2, 1, 1]
        elif self.idNum == 7:
            self.id = "Mog"
            self.attackPower = [1, 1, 1, 1]
        elif self.idNum == 8:
            self.id = "Gau"
            self.attackPower = [2, 1, 8, 5]
        elif self.idNum == 9:
            self.id = "Setzer Gabbiani"
            self.attackPower = [7, 7, 7, 7]
        elif self.idNum == 10:
            self.id = "Strago Magus"
            self.attackPower = [2, 2, 4, 4]
        elif self.idNum == 11:
            self.id = "Relm Arrowny"
            self.attackPower = [1, 4, 4, 8]
        elif self.idNum == 12:
            self.id = "Umaro"
            self.attackPower = [6, 7, 4, 10]
        elif self.idNum == 13:
            self.id = "Gogo"
            self.attackPower = [4, 6, 2, 7]
        
    def getImage(self, PROPERTIES={}):
    
        if self.targetPlayer == "Player" : playerColor = Config.PLAYER_COLOR[0]
        elif self.targetPlayer == "NPC 1" : playerColor = Config.PLAYER_COLOR[1]
        elif self.targetPlayer == "NPC 2" : playerColor = Config.PLAYER_COLOR[2]
    
        cardImage = pygame.image.load("../Image/Cards/" + str(self.idNum) + ".png").convert_alpha()
        borderImage = pygame.image.load("../Image/Cards/Border.png").convert_alpha()
    
        if "Small" in PROPERTIES:
            imageData = pygame.Surface([60, 87], pygame.SRCALPHA)
            pygame.draw.rect(imageData, playerColor, [3, 3, 54, 81])
            cardImage = pygame.transform.rotozoom(cardImage, 0, .50)
            borderImage = pygame.image.load("../Image/Cards/Border_Small.png").convert_alpha()
            imageData.blit(cardImage, [0, 0])
            targetFont = pygame.font.Font("../Font/TimesB.ttf", 15)
            
            outlineSize = 1
            topNumLoc = [13, 2]
            bottomNumLoc = [13, 28]
            rightNumLoc = [20, 15]
            leftNumLoc = [6, 15]
            
        else:
            imageData = pygame.Surface([118, 172], pygame.SRCALPHA)
            pygame.draw.rect(imageData, playerColor, [2, 2, 114, 168])
            imageData.blit(cardImage, [0, 0])
            targetFont = pygame.font.Font("../Font/TimesB.ttf", 30)
            
            outlineSize = 2
            topNumLoc = [21, 2]
            bottomNumLoc = [21, 48]
            rightNumLoc = [32, 24]
            leftNumLoc = [9, 24]
            
        # Attack Numbers #
        attackNumberTopString = str(self.attackPower[0])
        attackNumberRightString = str(self.attackPower[1])
        attackNumberBottomString = str(self.attackPower[2])
        attackNumberLeftString = str(self.attackPower[3])
        if attackNumberTopString == "10" : attackNumberTopString = "A"
        if attackNumberRightString == "10" : attackNumberRightString = "A"
        if attackNumberBottomString == "10" : attackNumberBottomString = "A"
        if attackNumberLeftString == "10" : attackNumberLeftString = "A"
        attackNumberTop = Utility.writeOutline(attackNumberTopString, targetFont, outlineSize)
        attackNumberRight = Utility.writeOutline(attackNumberRightString, targetFont, outlineSize)
        attackNumberBottom = Utility.writeOutline(attackNumberBottomString, targetFont, outlineSize)
        attackNumberLeft = Utility.writeOutline(attackNumberLeftString, targetFont, outlineSize)
        imageData.blit(attackNumberTop, topNumLoc)
        imageData.blit(attackNumberBottom, bottomNumLoc)
        imageData.blit(attackNumberRight, rightNumLoc)
        imageData.blit(attackNumberLeft, leftNumLoc)
        
        imageData.blit(borderImage, [0, 0])
            
        if "Alpha" in PROPERTIES:
            imageData.set_alpha(PROPERTIES["Alpha"])
        
        return imageData
        
    def getAttackPower(self, TARGET_SIDE, BOARD_INDEX, PROPERTIES):
    
        attackPower = self.attackPower[TARGET_SIDE]
    
        # Element Bonus/Penalty #
        if "Board Element List" in PROPERTIES:
            if PROPERTIES["Board Element List"][BOARD_INDEX] != None:
                if PROPERTIES["Board Element List"][BOARD_INDEX] != self.element:
                    attackPower -= 1
                else : attackPower += 1
            
        return attackPower
        
    def getDefense(self, ATTACKING_SIDE, BOARD_INDEX, PROPERTIES):
    
        defendingSideList = [2, 3, 0, 1]
        defendingSideIndex = defendingSideList[ATTACKING_SIDE]
        defense = self.attackPower[defendingSideIndex]
        
        # Element Bonus/Penalty #
        if "Board Element List" in PROPERTIES:
            if PROPERTIES["Board Element List"][BOARD_INDEX] != None:
                if PROPERTIES["Board Element List"][BOARD_INDEX] != self.element:
                    defense -= 1
                else : defense += 1
    
        return defense
        