import pygame, random, Config
from pygame import *

def loadColorCodeDict():

	codeDict = {"lr":[255, 80,  80],  "r":[255, 0,   0],   "dr":[145, 0,   0],   "ddr":[80,  0,   0],
				"lo":[255, 150, 75],  "o":[255, 100, 0],   "do":[170, 95,  0],   "ddo":[80,  40,  0],
				"ly":[255, 255, 80],  "y":[255, 255, 0],   "dy":[145, 145, 0],   "ddy":[80,  80,  0],
				"lg":[80,  255, 80],  "g":[0,   255, 0],   "dg":[0,   145, 0],   "ddg":[0,   80,  0],
				"lc":[80,  255, 255], "c":[0,   255, 255], "dc":[0,   145, 145], "ddc":[0,   80,  80],
				"lb":[80,  80,  255], "b":[0,   0,   255], "db":[0,   0,   145], "ddb":[0,   0,   80],
				"lv":[255, 80,  255], "v":[255, 0,   255], "dv":[145, 0,   145], "ddv":[80,  0,   80],
				"lm":[175, 80,  255], "m":[175, 0,   255], "dm":[95,  0,   145], "ddm":[75,  0,   80],
				"lw":[255, 255, 255], "w":[255, 255, 255], "dw":[220, 220, 220], "ddw":[150, 150, 150],
				"la":[150, 150, 150], "a":[150, 150, 150], "da":[120, 120, 120], "dda":[70,  70,  70],
				"x":[0, 0, 0]}
				
	return codeDict

def write(LABEL, LOCATION, COLOR, FONT, WINDOW):

	# Location Mods #
	labelSize = FONT.size(LABEL)
	if isinstance(LOCATION[0], str) and LOCATION[0].lower() == "left" : LOCATION[0] = 0
	elif isinstance(LOCATION[0], str) and LOCATION[0].lower() == "right" : LOCATION[0] = WINDOW.get_width() - labelSize[0]
	elif isinstance(LOCATION[0], str) and LOCATION[0].lower() == "center" : LOCATION[0] = int((WINDOW.get_width() / 2) - (labelSize[0] / 2))
	if isinstance(LOCATION[1], str) and LOCATION[1].lower() == "top" : LOCATION[1] = 0
	elif isinstance(LOCATION[1], str) and LOCATION[1].lower() == "bottom" : LOCATION[1] = WINDOW.get_height() - labelSize[1]
	
	labelRender = FONT.render(LABEL, True, COLOR)
	WINDOW.blit(labelRender, LOCATION)
    
	return [LOCATION[0], LOCATION[1], labelSize[0], labelSize[1]]
    
def writeColor(LABEL, COLOR_CODE, COLOR_DICT, LOCATION, FONT, WINDOW):

	# Location Mods #
	labelSize = FONT.size(LABEL)
	if isinstance(LOCATION[0], str) and LOCATION[0].lower() == "left" : LOCATION[0] = 0
	elif isinstance(LOCATION[0], str) and LOCATION[0].lower() == "right" : LOCATION[0] = WINDOW.get_width() - labelSize[0]
	if isinstance(LOCATION[1], str) and LOCATION[1].lower() == "top" : LOCATION[1] = 0
	elif isinstance(LOCATION[1], str) and LOCATION[1].lower() == "bottom" : LOCATION[1] = WINDOW.get_height() - labelSize[1]
	
	# Regular Variables #
	targetColor = ""
	colorCount = 0
	printIndex = 0
	displayX = LOCATION[0]
	writeCheck = False
	
	for i, letter in enumerate(COLOR_CODE):
	
		# Sort #
		if stringIsNumber(letter):
			if colorCount != 0 : colorCount *= 10
			colorCount += int(letter)
		else:
			targetColor = targetColor + letter
			if len(COLOR_CODE) > i+1 and stringIsNumber(COLOR_CODE[i+1]):
				writeCheck = True
			
		# Write Check #
		if i+1 == len(COLOR_CODE):
			writeCheck = True
			
		# Write #
		if writeCheck == True:
			writeColor = [255, 255, 255]
			if targetColor in COLOR_DICT : writeColor = COLOR_DICT[targetColor]
			
			textString = LABEL[printIndex:printIndex+colorCount]
			textRender = FONT.render(textString, True, writeColor)	
			WINDOW.blit(textRender, [displayX, LOCATION[1]])
			
			printIndex += colorCount
			if printIndex == len(LABEL) : return
			displayX += FONT.size(textString)[0]
			colorCount = 0
			targetColor = ""
			writeCheck = False
		
def writeOutline(LABEL, FONT, PX_OUTLINE=2, COLOR_TEXT=[230, 230, 230], COLOR_OUTLINE=[10, 10, 10]):

	surfaceText = FONT.render(LABEL, True, COLOR_TEXT).convert_alpha()
	textWidth = surfaceText.get_width() + 2 * PX_OUTLINE
	textHeight = FONT.get_height()

	surfaceOutline = pygame.Surface([textWidth, textHeight + 2 * PX_OUTLINE]).convert_alpha()
	surfaceOutline.fill([0, 0, 0, 0])
	surfaceMain = surfaceOutline.copy()
	surfaceOutline.blit(FONT.render(str(LABEL), True, COLOR_OUTLINE).convert_alpha(), [0, 0])
	
	circleCache = {}
	for dx, dy in circlePoints(circleCache, PX_OUTLINE):
		surfaceMain.blit(surfaceOutline, [dx + PX_OUTLINE, dy + PX_OUTLINE])
		
	surfaceMain.blit(surfaceText, [PX_OUTLINE, PX_OUTLINE])
	
	return surfaceMain
	
def createTextBox(TEXT_BOX_IMAGE, PROPERTIES):

    # Create Base Surface #
    size = [100, 100]
    if "Size" in PROPERTIES:
        size = PROPERTIES["Size"]
    textBox = pygame.Surface(size, pygame.SRCALPHA)
    
    if "Color" in PROPERTIES:
        textBoxFill = pygame.Surface([size[0] - (Config.BORDER_INDENT * 2), size[1] - (Config.BORDER_INDENT * 2)], pygame.SRCALPHA)
        textBoxFill.fill(PROPERTIES["Color"])
        textBox.blit(textBoxFill, [Config.BORDER_INDENT, Config.BORDER_INDENT])
        
    # Create Border Corners #
    cornerWidth = TEXT_BOX_IMAGE["Corner"].get_rect().width
    
    textBox.blit(TEXT_BOX_IMAGE["Corner"], [0, 0])
    topRightCorner = pygame.transform.rotate(TEXT_BOX_IMAGE["Corner"], -90)
    textBox.blit(topRightCorner, [size[0] - cornerWidth, 0])
    bottomLeftCorner = pygame.transform.rotate(TEXT_BOX_IMAGE["Corner"], 90)
    textBox.blit(bottomLeftCorner, [0, size[1] - cornerWidth])
    bottomRightCorner = pygame.transform.rotate(TEXT_BOX_IMAGE["Corner"], 180)
    textBox.blit(bottomRightCorner, [size[0] - cornerWidth, size[1] - cornerWidth])
    
    # Create Border Sides #
    sideSize = TEXT_BOX_IMAGE["Side"].get_rect().size
    gapWidth = size[0] - (cornerWidth * 2)
    gapHeight = size[1] - (cornerWidth * 2)
    
    topSide = pygame.transform.scale(TEXT_BOX_IMAGE["Side"], [gapWidth, sideSize[1]])
    textBox.blit(topSide, [cornerWidth, 0])
    bottomSide = pygame.transform.rotate(TEXT_BOX_IMAGE["Side"], 180)
    bottomSide = pygame.transform.scale(bottomSide, [gapWidth, sideSize[1]])
    textBox.blit(bottomSide, [cornerWidth, size[1] - sideSize[1]])
    
    leftSide = pygame.transform.rotate(TEXT_BOX_IMAGE["Side"], 90)
    leftSide = pygame.transform.scale(leftSide, [sideSize[1], gapHeight])
    textBox.blit(leftSide, [0, cornerWidth])
    rightSide = pygame.transform.rotate(TEXT_BOX_IMAGE["Side"], -90)
    rightSide = pygame.transform.scale(rightSide, [sideSize[1], gapHeight])
    textBox.blit(rightSide, [size[0] - sideSize[1], cornerWidth])
    
    return textBox
    
def getTargetResolutionLevel():

    # Resolution Level 2 - [800, 600], [1024, 768], [1152, 864]
    # Resolution Level 1 - [1280, 720], [1280, 768], [1360, 768], [1366, 768], [1280, 800], [1440, 900], [1280, 960]
    # Resolution Level 0 - [1280, 1024], [1400, 1050], [1680, 1050], [1920, 1080]

    currentResolution = Config.SCREEN_RESOLUTION[Config.SCREEN_RESOLUTION_INDEX]

    if currentResolution in [[800, 600], [1024, 768], [1152, 864]]:
        return 2
    elif currentResolution in [[1280, 720], [1280, 768], [1360, 768], [1366, 768], [1280, 800], [1440, 900], [1280, 960]]:
        return 1
    else:
        return 0
    
def getTargetDisplayFont():

    screenResolution = Config.SCREEN_RESOLUTION[Config.SCREEN_RESOLUTION_INDEX]
    if screenResolution == [800, 600]:
        return Config.FONT_ROMAN_10
    elif screenResolution == [1024, 768]:
        return Config.FONT_ROMAN_14
    elif screenResolution == [1152, 864]:
        return Config.FONT_ROMAN_16
    elif screenResolution in [[1280, 720], [1280, 768], [1280, 800], [1280, 960], [1280, 1024]]:
        return Config.FONT_ROMAN_18
    elif screenResolution in [[1360, 768], [1366, 768], [1440, 900], [1400, 1050]]:
        return Config.FONT_ROMAN_20
    elif screenResolution in [[1680, 1050], [1920, 1080]]:
        return Config.FONT_ROMAN_20
    
def getLabel(LABEL, COLOR, FONT):
    labelSize = FONT.size(LABEL)
    labelRender = FONT.render(LABEL, True, COLOR)
    return labelRender
    
def circlePoints(CIRCLE_CACHE, R):

	R = int(round(R))
	if R in CIRCLE_CACHE:
		return CIRCLE_CACHE[R]
	
	x, y, e = R, 0 , 1 - R
	CIRCLE_CACHE[R] = points = []
	
	while x >= y:
		points.append([x, y])
		y += 1
		if e < 0:
			e += 2 * y - 1
		else:
			x -= 1
			e += 2 * (y - x) - 1
	
	points += [[y, x] for x, y in points if x > y]
	points += [[-x, y] for x, y in points if x]
	points += [[x, -y] for x, y in points if y]
	points.sort()
	
	return points
	
def outline(SCREEN, COLOR, LOCATION, SIZE, LINE_WIDTH=1):
	
	pygame.draw.line(SCREEN, COLOR, [LOCATION[0], LOCATION[1]], [LOCATION[0] + SIZE[0] - 1, LOCATION[1]], LINE_WIDTH)                             # Top Line
	pygame.draw.line(SCREEN, COLOR, [LOCATION[0], LOCATION[1]], [LOCATION[0], LOCATION[1] + SIZE[1] - 1], LINE_WIDTH)                             # Left Line
	pygame.draw.line(SCREEN, COLOR, [LOCATION[0] + SIZE[0] - 1, LOCATION[1]], [LOCATION[0] + SIZE[0] - 1, LOCATION[1] + SIZE[1] - 1], LINE_WIDTH) # Right Line
	pygame.draw.line(SCREEN, COLOR, [LOCATION[0], LOCATION[1] + SIZE[1] - 1], [LOCATION[0] + SIZE[0] - 1, LOCATION[1] + SIZE[1] - 1], LINE_WIDTH) # Bottom Line
	
def stringIsNumber(STRING):

	try:
		int(STRING)
		return True
	except ValueError:
		return False

def createKeyList(TARGET_STRING):

    TARGET_STRING = TARGET_STRING.lower()
    keyList = [TARGET_STRING]

    if len(TARGET_STRING.split()) > 2:
        for iNum in range(len(TARGET_STRING.split())-2):
            if ' '.join(TARGET_STRING.split()[0:iNum+2]) not in keyList:
                keyList.append(' '.join(TARGET_STRING.split()[0:iNum+2]))

    if len(TARGET_STRING.split()) > 1:
        for skillKeyword in TARGET_STRING.split():
            if skillKeyword not in keyList:
                keyList.append(skillKeyword)
				
    return keyList

def generateRandomId():
	
	randomId = str(random.randrange(1000000, 9999999))
	randomIndex = random.randrange(len(randomId))
	randomAlpha1 = random.choice(Config.ALPHABET_STRING)
	randomAlpha2 = random.choice(Config.ALPHABET_STRING)
	randomId = randomId[0:randomIndex] + randomAlpha1 + randomId[randomIndex::] + randomAlpha2
	
	return randomId
	
def rectRectCollide(RECT1_LOC, RECT2_LOC, SIZE):

	if RECT1_LOC[0] in range(RECT2_LOC[0], RECT2_LOC[0] + SIZE[0]):
		if RECT1_LOC[1] in range(RECT2_LOC[1], RECT2_LOC[1] + SIZE[1]):
			return True

	return False

def circleCircleCollide(CIRCLE1_LOC, CIRCLE1_RADIUS, CIRCLE2_LOC, CIRCLE2_RADIUS):

	import math
	dx = CIRCLE1_LOC[0] - CIRCLE2_LOC[0]
	dy = CIRCLE1_LOC[1] - CIRCLE2_LOC[1]
	dr = math.sqrt((dx ** 2) + (dy ** 2))
	
	if dr <= CIRCLE1_RADIUS + CIRCLE2_RADIUS:
		return True
	
	return False
	