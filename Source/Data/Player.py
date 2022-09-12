import pygame, Config, Utility
from pygame import *

class Load:

    def __init__(self):
        
        self.cardCollectionDict = {1:52, 2:3, 3:1, 4:0, 5:2, 6:2, 7:2, 10:2, 11:2, 12:2}
        self.deckNameList = ["Custom Deck 1", "Custom Deck 2", "Custom Deck 3"]
        self.deckDataList = [[5, 5, 2, 2, 2], [2, 2, 3, 5, 7], [6, 7, 10, 11, 12]]
        
    def getTotalCardCount(self, PROPERTIES={}):
    
        totalCount = 0
        
        CARD_COLLECTION_DICT = self.cardCollectionDict
        if "Card Collection Dict" in PROPERTIES:
            CARD_COLLECTION_DICT = PROPERTIES["Card Collection Dict"]
        
        for card in CARD_COLLECTION_DICT:
            if CARD_COLLECTION_DICT[card] > 0:
                if not ("Exclude Card List" in PROPERTIES and card in PROPERTIES["Exclude Card List"] and (CARD_COLLECTION_DICT[card] - PROPERTIES["Exclude Card List"].count(card)) <= 0):
                    totalCount += 1
        
        return totalCount
        
    def getSortedCollectionList(self, PROPERTIES={}):
    
        indexList = []
        
        CARD_COLLECTION_DICT = self.cardCollectionDict
        if "Card Collection Dict" in PROPERTIES:
            CARD_COLLECTION_DICT = PROPERTIES["Card Collection Dict"]
        
        for i in CARD_COLLECTION_DICT:
            if CARD_COLLECTION_DICT[i] > 0:
                if not ("Exclude Card List" in PROPERTIES and i in PROPERTIES["Exclude Card List"] and (CARD_COLLECTION_DICT[i] - PROPERTIES["Exclude Card List"].count(i)) <= 0):
                    indexList.append(i)
        indexList.sort()
        
        return indexList
        
    def getMaxDeckSize(self):
    
        return 6
        