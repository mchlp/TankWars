
#Final Project - Game
#Tank Wars
#Multiplayer Version
#Michael Pu & Samuel Liu
#ICS2O1
#2016/12/06
#SCREEN RESOLUTION: LAPTOP -> H 768 W 1366

import os
import time
import random
import hashlib
import getpass
import sys

#Get Path to Working Directory 
curPath = os.getcwd()

#detect windows version
if sys.maxsize == 9223372036854775807:
    v = 64
else:
    v = 32

#pygame module
sys.path.append(os.getcwd()+"/pygame"+str(v))

import pygame
from pygame.locals import *  


#LOAD GAME RESOURCES
def loadGame(resourcePath, loadMusicName):
    #Loading Screen Function
    def dispalyLoading(screen):
        #Fill loading screen with grey colour
        loadingScreen = pygame.surface.Surface(size)
        loadingScreen.fill((100,100,100))
        #Loading screen background (darkens screen)
        loadGameBGPic = pygame.image.load(resourcePath + "gameOverBackground.png").convert_alpha()
        loadGameBG = pygame.transform.scale(loadGameBGPic, size)
        loadGameBGRect = loadGameBG.get_rect()
        loadGameBGRect.center = loadingScreen.get_rect().center
        #Loading screen text
        loadFont = pygame.font.Font(resourcePath+"blackOpsOne.ttf", size[1]//10)
        loadFont2 = pygame.font.Font(resourcePath+"blackOpsOne.ttf", size[1]//20)
        loadText = loadFont.render("Loading Game...", True, (200,200,200))
        loadText2 = loadFont2.render("This may take a while.", True, (200,200,200))
        loadTextRect = loadText.get_rect()
        loadTextRect2 = loadText2.get_rect()
        loadTextRect.midtop = (loadGameBGRect.centerx, loadGameBGRect.centery-40-size[1]//7-size[1]//20)
        loadTextRect2.midtop = (loadGameBGRect.centerx, loadGameBGRect.centery-size[1]//20-10)
        
        #Blit text and images to screen to screen
        loadingScreen.blit(loadGameBG, loadGameBGRect)
        loadingScreen.blit(loadText, loadTextRect)
        loadingScreen.blit(loadText2, loadTextRect2)
        screen.blit(loadingScreen, (0,0))
        pygame.display.update()
        
        #return loadingScreen, y cord for bottom of text
        return (loadingScreen, loadTextRect2.bottom)
    
    #Screen when loading is finished
    def doneLoading(loadingScreen, lastTextBotttom):
        global fonts
        global colours
        #text and fonts
        loadFont = pygame.font.Font(fonts["bops1"], size[1]//25)
        loadText = loadFont.render("Loading Complete.", True, colours["light grey"])
        loadText2 = loadFont.render("Press any key or click to continue...", True, colours["light grey"])
        loadTextDash = loadFont.render("-----", True, colours["light grey"])
        #generate rect for texts
        loadTextRect = loadText.get_rect()
        loadTextRect2 = loadText2.get_rect()
        #set position for text
        loadTextDashRect = loadTextDash.get_rect()
        loadTextDashRect.midtop = (screen.get_rect().centerx, lastTextBotttom+30)
        lastTextBotttom += loadTextDashRect.height+30
        loadTextRect.midtop = (screen.get_rect().centerx, lastTextBotttom+10)
        lastTextBotttom += loadTextRect.height+10
        loadTextRect2.midtop = (screen.get_rect().centerx, lastTextBotttom+10)
        
        #keep going flag
        keepGoing = True
        
        #speed at which the text flashes
        flashLimit = fpsRate*0.8
        #set counter since last flash
        flashCounter = flashLimit
        #if text visible or not (flashing)
        visible = True
        
        while keepGoing:
            #fps rate
            clock.tick(fpsRate)
            
            #if flash counter is up
            if flashCounter <= 0:
                #cover up old screen
                screen.blit(loadingScreen, (0,0))
                screen.blit(loadTextDash, loadTextDashRect)
                screen.blit(loadText, loadTextRect)
                
                if not visible:
                    #previously not visible --> show text
                    screen.blit(loadText2, loadTextRect2)
                    visible = True
                else:
                    #previously visible --> do not show text
                    visible = False
                #reset flash counter 
                flashCounter = flashLimit    
            #-1 tick for flash counter
            flashCounter -= 1
            
            #check for key or mouse down --> start game
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    #if windows close button is pressed
                    pygame.quit()
                    sys.exit()()
                if ev.type == pygame.KEYDOWN:
                    #if key is pressed
                    keepGoing = False
                    break
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    #if mouse button is pressed
                    if ev.button == 1 or ev.button == 3 or ev.button == 2:
                        #if left(1), right(2), or middle mouse button(3) is pressed, not scroll wheel (4,5)
                        keepGoing = False
                        break
            #update display
            pygame.display.update()        
            
    #Test if screen resolution is full screen compatible (sometimes pygame incorrectly detects the resolution
    #of the screen, which will cause the full screen graphics to be distorted. this can be prevented by 
    #showing an image of a square, which will be distorted if the detected screen resolution is incorrect.
    #If detection is incorrect, then the game will not run in full screen mode so that the graphics remain normal.)
    def testRes(squareSize, fontSize, displayW, displayH):
        #vertical spacing between text blocks
        spacing = displayH//100
        #set display to full screen
        testScreen = pygame.display.set_mode((displayW,displayH), pygame.FULLSCREEN)
        testScreen.fill((255,128,0))
        
        #instructions text and font
        instructFont = pygame.font.Font(resourcePath+"calibril.ttf", int(fontSize*1.5))
        explainFont = pygame.font.Font(resourcePath+"calibril.ttf", fontSize)
        instructText = instructFont.render("Testing the full screen compatability of your screen...", True, (0,0,0))
        #if not the entire screen is visible, the user can press ESCAPE, which is the same as pressing NO
        instructText2 = explainFont.render("Press ESCAPE if any part of the screen is not visible.", True, (0,0,0))
        #generate rect for text
        instructRect = instructText.get_rect()
        instructRect2 = instructText2.get_rect()
        #position text on the screen
        imageBottom = spacing*4
        instructRect.midtop = (displayW//2, imageBottom+spacing)
        imageBottom += instructRect.h+spacing
        instructRect2.midtop = (displayW//2, imageBottom+spacing)
        imageBottom += instructRect.h+spacing
        #blit text to the screen
        testScreen.blit(instructText, instructRect)
        testScreen.blit(instructText2, instructRect2)
        
        #test image (one of the following are used)
        #TEST IMAGE 1: checkerboard pattern
        #trImage = pygame.image.load(resourcePath+"checkerboard.png")
        #TEST IMAGE 2: square
        trImage = pygame.image.load(resourcePath+"testRes.jpg")
        #scale image according to size of screen
        trImage = pygame.transform.scale(trImage, (squareSize,squareSize))
        #get rect for image
        trImageRect = pygame.Rect(trImage.get_rect())      
        #position image
        trImageRect.midtop = (displayW//2,imageBottom+spacing*2)
        imageBottom += trImageRect.h+spacing*2
        testScreen.blit(trImage, trImageRect)
        
        #add explain text
        explainText = explainFont.render("Are the side lengths of the shape above equal AND the orange background fills the entire screen?", True, (0,0,0))
        explainRect = explainText.get_rect()
        #position explain text
        explainRect.midtop = (displayW//2, imageBottom+spacing*3)
        imageBottom += explainRect.h+spacing*3
        #blit explain text to screen
        testScreen.blit(explainText, explainRect)
        #create buttons (yes, no)
        yesButton = pygame.image.load(resourcePath+"yButton.png")
        noButton = pygame.image.load(resourcePath+"nButton.png")
        #position buttons
        yRect = yesButton.get_rect()
        yRect.center = ((displayW//3)*1,imageBottom+spacing*5)
        nRect = noButton.get_rect()
        nRect.center = ((displayW//3)*2,imageBottom+spacing*5)
        #blit buttons to screen
        testScreen.blit(yesButton, yRect)
        testScreen.blit(noButton, nRect)
        #update display
        pygame.display.flip()
        while True:
            for ev in pygame.event.get():
                if ev.type == MOUSEBUTTONDOWN:
                    #get mouse position when button down is pressed
                    pos = pygame.mouse.get_pos()
                    #yes button
                    if yRect.collidepoint(pos):
                        #yes - full screen compatible
                        return True
                    #no button
                    elif nRect.collidepoint(pos):
                        #no - not full screen compatible
                        return False
                elif ev.type == KEYDOWN:
                    #if key is pressed, check if it is ESC
                    if ev.key == K_ESCAPE:
                        #escape button - not full screen compatible
                        return False

    #Set up screen
    def setupDisplay():
        global screen
        global images
        global size
        import platform
        
        #If game is not run in full screen, the y position of the top of the window
        winYPos = 50
        
        #Flag whether to check Resolution for Full Screen or not (should the program check if the
        #screen is compatible with full screen) - FOR TESTING PURPOSES (should be true)
        checkFullScreenRes = True
        
        #Attempts to Detect Display Info
        displayInfo = pygame.display.Info()
        displayH = displayInfo.current_h
        displayW = displayInfo.current_w

        #TEMP TESTING (testing for screens with different resolution)
        #displayW = 640
        #displayH = 480
        #displayH = 768
        #displayW = 1366
        #TEMP TESTING
        
        #the game screen will be a bit smaller than the actual screen if the game is not run in full screen
        gameH = displayH-200
        gameW = displayW-20
        
        #Set Screen Size
        if gameH <= -1 or gameW <= -1:
            #if pygame cannot detect the screen resolution, it will return -1, so set default size
            size = (1366,768)
            #set window position (where the midtop of the window is on the screen when the game starts)
            os.environ['SDL_VIDEO_WINDOW_POS'] = '%i,%i' % (displayW//2-min(1600, gameW)//2, winYPos)
            #default size
        else:
            #round to nearest 25 pixels 
            gameW = gameW - gameW%25
            #add height of status bar to the game screen size
            gameH = gameH - gameH%25 + 75
            
            if gameH > 1600 or gameW > 1600:
                #if screen is larger than the background image, then get the largest size which 
                #will be covered by the background image (which has dimensions of 1600x1600)
                size = (min(1600, gameW), min(1600, gameH))
                #center window on screen when it is opened
                os.environ['SDL_VIDEO_WINDOW_POS'] = '%i,%i' % (displayW//2-min(1600, gameW)//2, winYPos)
                screen = pygame.display.set_mode(size) 
                
            else:
                #else - if the screen is a good size for full screen (not too big)
                if checkFullScreenRes:
                    #if check for full screen resolution compatability
                    #get whether or not the screen is full screen compatible by running testRes function (see functoin above)
                               #testRes(size of testing image,            fontSize,     displayW, displayH)
                    ynGoodRes = testRes(((min(displayW, displayH))//5)*2, displayH//35, displayW, displayH)
                    if ynGoodRes:
                        #if full screen compatible
                        #the size of the game screen = size of screen
                        size = (displayW, displayH)
                        #set display mode to full screen
                        screen = pygame.display.set_mode(size, pygame.FULLSCREEN) 
                    else:
                        #not full screen compatible
                        #size of game screen = gameW, gameH (calculated above to be a bit smaller than the screen)
                        size = (gameW, gameH)
                        #center window when it is opened on the screen
                        os.environ['SDL_VIDEO_WINDOW_POS'] = '%i,%i' % (displayW//2-gameW//2, winYPos)
                        #create display with the dimensions of the size variable
                        screen = pygame.display.set_mode(size)
                else:
                    #else - don't check for full screen compatability, automatically go to not full screen
                    #size = gameW, gameH (calculated above to be a bit smaller than the screen)
                    size = (gameW, gameH)
                    #center opening window
                    os.environ['SDL_VIDEO_WINDOW_POS'] = '%i,%i' % (displayW//2-gameW//2, winYPos)
                    screen = pygame.display.set_mode(size)
            
        if platform.system() == "Windows":
            #TESTING STUFF
            #os.environ['SDL_VIDEO_WINDOW_POS'] = str(position[0]) + "," + str(position[1])
            #os.environ['SDL_VIDEO_WINDOW_POS'] = '%i,%i' % (displayW//2-gameW//2,1)
            #os.environ['SDL_VIDEO_CENTERED'] = '1'
            #TESTING STUFF
            
            #set video driver to 'windlib' (included in example code)
            os.environ['SDL_VIDEODRIVER'] = 'windib'  
        
        #set caption of the window (on the top)
        pygame.display.set_caption("Tank Wars")
        #set icon of the window 
        pygame.display.set_icon(pygame.image.load(resourcePath+"icon.png"))
        screen.fill((100,100,100))
        #return the screen, where images will be blitted onto
        return screen

    #Load Images
    def loadImages():
        global images
        global tankControls
        
        #dictionary for storing images {nameOfImage:imageSurfaceObject}
        images = {}
        
        #directions for directional images (eg. tank, missile)
        directions = ["U", "D", "L", "R"]
        
        #one image list (images which one have one copy) --> {imageName:imageNameInFolder.jpg}
        oImageList = {"trImage":"testRes.jpg", "bgImage":"dirt.jpg", "tank1Temp":"tank1.png", "wall":"wall2.png", "bWall":"bWall.png"
        ,"ammo":"ammo.png", "ammoPower":"ammoPower.png", "heart":"heart.png", "skull":"skull.png", "blank":"blank.png", "ghost":"ghost.png"
        ,"LBbg":"gameOverLeaderboardBackground.png", "rankSlot":"rankSlot.png", "rankingTitleBG":"titleSlot.png", "rankSlotTitle":"rankSlotTitle.png"
        ,"shotsFired":"shotsFired.png", "shotsHit":"shotsHit.png", "accuracy":"accuracy.png", "shotsTaken":"shotsTaken.png", "netDamage":"netDamage.png"
        ,"time":"time.png" ,"help":"help.png", "helpLong":"helpLong.png", "rankingBlank":"rankingBlank.png", "pauseFull":"pauseFull.png", "powerUp":"powerUp.png"
        ,"pauseFade":"pauseFade.png", "playFull":"playFull.png", "settingsBG":"settingsBG.png", "SGbg":"setupGameBackground.png", "helpInst":"helpInst.png"
        ,"GObg":"gameOverBackground.png"}
        
        #direction image list (4 images for each of the four states - up, down, left, right)
        dImageList = {"missile":"missile.png", "bWall":"bWall.png"}
        
        #images for keyboard keys
        for player in range(1, 4+1):
            for key in tankControls[player].keys():
                #for each key in the list of possible keyboard control keys, load its image 
                name = pygame.key.name(key)
                if name == "/":
                #image cannot be named "/", so it is named slash
                    name = "slash"
                #add key image to the dictionary for all images
                images["k_"+name] = pygame.image.load(resourcePath + "keys/" +name+".png").convert_alpha()

        #add buttons to image dictionary
        for button in ["restart", "mainMenu", "playAgain", "quit"]:
            #normal button --> add to list of images to load later
            oImageList[button+"But"] = button+".png"
            #button darkens when the mouse is over it --> add to list of images to load later
            oImageList[button+"ButSel"] = button+"Sel.png"
        
        #add power ups images to image list --> add to list of images to load later
        for powerUp in ["AmmoInfin", "Speed", "DoubleLife", "AmmoPower"]:
            oImageList["pu"+powerUp] = "pu"+powerUp+".png"
        #image on status bar when the infinite ammo power up is obtained
        oImageList["puAmmoImage"] = "puAmmoImage.png"
        
        #add cracked wall to image list (3 different states - walls take 3 hits to destory and with
        #every hit, more cracks appear)
        for cWall in range(1, 3+1):
            #--> add to list of images to load later
            oImageList["wallCracked"+str(cWall)] = "wall2Crack"+str(cWall)+".png"
        
        #add tanks to image list (total of 4 possible tank images)
        for tankNum in range(4+1):
            #--> add to list of directional images (the images with 4 states - up, down, left, right)
            dImageList["tank"+str(tankNum)] = "tank"+str(tankNum)+".png"
            #--> add to list of images to load later
            oImageList["tank"+str(tankNum)] = "tank"+str(tankNum)+".png"
        
        #load images in list to load later (images with only one possible state)
        for loadOImage in oImageList:
            images[loadOImage] = pygame.image.load(resourcePath + oImageList[loadOImage]).convert_alpha()
            
        #load direction images (image with 4 possible states - up,down,left,right)
        for loadDImage in dImageList:
            for direct in directions:
                #find location of dot
                dot = dImageList[loadDImage].find(".")
                #add "R","L","U", or "D" before the dot (end of the file name), depending on the direction
                fileName = dImageList[loadDImage][:dot] + direct + dImageList[loadDImage][dot:]
                images[loadDImage+direct] = pygame.image.load((resourcePath + fileName)).convert_alpha()
                
        #load explosion frames (total of 19 frames for animation)
        for explosionImage in range(1, 19+1):
            #big explosion
            images["explosion"+str(explosionImage)] = pygame.image.load(resourcePath + "explosion (" + str(explosionImage) + ").gif")
            #small explosion
            images["sExplosion"+str(explosionImage)] = pygame.image.load(resourcePath + "sExplosion (" + str(explosionImage) + ").png")
            
    #Load Maps
    def loadMap():
        global maps
        #create dictionary to store maps
        maps = {}
        #open map file (can be found in the resources folder)
        mapFile = open(resourcePath + "mapDataBase.txt")
        #set flag whether to add the following lines to the map database
        addData = False
        #for each line in the mapFile
        for line in mapFile:
            #strip off the whitespace (" ", "\n", etc.)
            line = line.strip()
            if line == "***":
                #"***" means start of new map or end of map
                if addData:
                    #if lines are already being added, then it represents the end of a map
                    addData = False
                    #add the current map to the map database
                    maps[mapCount] = curMap
                else:
                    #else - the lines are not already being added, it is the beginning of a map
                    addData = True
                    #declare list to store map data temporarily
                    curMap = []
                #skip the rest of the code and read the next line
                continue
            elif addData:
                #elif - the beginning of a map has been detected (addData boolean), so add the line to 
                #the map database
                if line in "1234567890":
                    #the map number -> set mapCount to the map number
                    mapCount = int(line)
                else:
                    #add line to current map list, which will later be added to the map database
                    #(contains data on how different objects will be arranged on the game screen)
                    curMap.append(line) 
    
    #Load WAV Sounds 
    def loadSounds():
        #(mp3 sounds cannot be converted into a pygame Sound object, so they will be
        #loaded directly within the code where they are played)
        global sounds
        #create dictionary to store sound objects
        sounds = {}
        #list of sounds to process
        soundListWAV = {"smallExplosion":"smallExplosion.wav", "bigExplosion":"bigExplosion.wav", "shoot":"pew.wav", "powerUp":"powerUp.wav"
        ,"victory":"victory.wav", "leaderboard":"leaderboard.wav", "countDown":"cwBeep.wav", "countDownFin":"cwFinBeep.wav"}
        for sound in soundListWAV:
            #add converted sound to sound dictionary
            sounds[sound] = pygame.mixer.Sound(resourcePath + soundListWAV[sound])
            
    #Load Fonts
    def loadFonts():
        global fonts
        fonts = {}
        #create dictionary to store font objects
        #list of fonts to process
        fontList = {"bops1":"blackOpsOne.ttf", "tankFont":"tankFont.ttf", "roboto":"roboto.ttf", "openSans":"openSans.ttf", "calibri":"calibril.ttf",
        "openSansBold":"openSansBold.ttf", "openSansEBold":"openSansExtraBold.ttf", "coda":"codaReg.ttf"}
        for font in fontList:
            #add converted font to font dictionary
            fonts[font] = resourcePath + fontList[font]
    
    #Load Colours
    def loadColours():
        global colours
        #create dictionary to store colour names leading to their colour RGB values
        colours = {"black":(0,0,0), "white":(255,255,255), "grey":(128,128,128), "silver":(192,192,192),
        "light grey":(200,200,200), "dark grey":(50,50,50), "blue":(74,160,216), "green":(61,188,22),
        "pink":(198,100,176), "orange":(200,117,44), "red":(239, 43, 43), "goGreen":(45, 185, 45)}
    
    #Play loading music
    global musicOn
    if musicOn:
        pygame.mixer.music.load(resourcePath + loadMusicName)
        pygame.mixer.music.play(-1) 
    
    #Set up screen 
    setupDisplay()
    
    #display loading screen (returns [loadingScreen, y cord of the bottom of the lowest object])
    returnData = dispalyLoading(screen)
    lastTextBotttom = returnData[1]
    loadingScreen = returnData[0]
    
    loadImages()
    loadMap()
    loadSounds()
    loadFonts()
    loadColours()  
    
    #dispaly done loading screen (calling the function with parameters returned by displayLoading() function)
    doneLoading(loadingScreen, lastTextBotttom)

#GET USER TO SET UP SETTINGS
def userSetup(resourcePath, setupMusicName):
    global tankControls
    global images
    global fonts
    global screen
    global size
    global colours
    global sounds
    global musicOn
    
    #create groups for player sprites
    playerProfileGroup = pygame.sprite.Group()
    playerProfileDict = {}
    
    #play setup background music 
    if musicOn:
        pygame.mixer.music.load(resourcePath + setupMusicName)
        pygame.mixer.music.play(-1)
    
    #class for instructions text
    class profileInstructions(pygame.sprite.Sprite):
        #initialization method
        def __init__(self, parent):
            pygame.sprite.Sprite.__init__(self)
            #parent --> grey background rectangle
            self.parent = parent
            #text background
            self.image = pygame.Surface((parent.width-20, 50))
            self.image.fill(colours["red"])
            self.rect = self.image.get_rect()
            self.rect.topleft = (10, 20)
            #set text modes
            self.notReadyText = "Press the any Button in your Profile to Join."
            self.readyText = "Press the Space Bar to Begin. Or Esc to Restart."
            self.morePlayers = "More Players Needed. Press the any Button in your Profile to Join."
            self.onePlayer = "Player 1 Must Join. Press Any of the Keys in the First Profile to Join."
            #set font
            #self.font = pygame.font.Font(fonts["bops1"], 33) 
            self.font = pygame.font.Font(fonts["coda"], 30) 
            
        #method to update the colour and text
        def update(self, keyPress = None):
            #check key press
            if keyPress != None:
                #if a key press parameter is passed into the variable
                if keyPress == pygame.K_SPACE:
                    #if space bar is pressed
                    if self.oneJoined and self.otherOneJoined:
                        #if enough players joined -->
                        global controlsPlayerDict
                        global setupKeepGoing
                        for player in playerProfileDict:
                            if playerProfileDict[player].joined:
                                #if player is joined --> bind player control profile to a player tank profile
                                controlsPlayerDict[playerProfileDict[player].num] = playerProfileDict[player].playerNum
                        #stop loop (start game)
                        setupKeepGoing = False
                        
                if keyPress == pygame.K_ESCAPE:
                    #if escape is pressed - clear all joined players
                    global curPlayer
                    #the next empty player control profile is player 2
                    curPlayer = 2
                    for player in playerProfileDict:
                        #for each player profile, set its joined status to False
                        playerProfileDict[player].joined = False
                        
            #update text and colour
            self.oneJoined = False
            self.otherOneJoined = False
            
            #check how many players joined
            for player in playerProfileDict:
                #for player in the player control profile dictionary, check if the player has joined
                if playerProfileDict[player].joined:
                    #if player has joined
                    if player == 1:
                        #if joined player is player 1, set the corresponding variable to True
                        self.oneJoined = True
                    else:
                        #if joined player is player not 1, set the corresponding variable to True
                        self.otherOneJoined = True
                          
            if not self.oneJoined and not self.otherOneJoined:
                #if no players joined      
                self.text = self.notReadyText
                self.image.fill(colours["red"])
                
            elif self.oneJoined and not self.otherOneJoined:
                #if only player 1 joined
                self.text = self.morePlayers
                self.image.fill(colours["red"])
                
            elif self.otherOneJoined and not self.oneJoined:
                #if players have joined, but not player 1
                self.text = self.onePlayer
                self.image.fill(colours["red"])
                
            else:
                #else - enough players joined
                self.text = self.readyText
                self.image.fill(colours["goGreen"])
                
            #render instruction text into surface object
            self.textImage = self.font.render(self.text, True, colours["black"])
            self.textRect = self.textImage.get_rect()
            self.textRect.center = (self.rect.width//2, self.rect.height//2)
            
            #blit text to background
            self.image.blit(self.textImage, self.textRect)
    
    #class for each individual player profile (includes its image, tank image, and key images)
    class playerProfile(pygame.sprite.Sprite):
        #variables to store dimensions of keyboard key images
        keyWidth = images["k_w"].get_width()
        keyHeight = images["k_w"].get_height()
        #spacing between each of the keys images
        keySpacing = 10
        
        #class for the actual image of the tank
        class playerImage(pygame.sprite.Sprite):
            #initialization method
            def __init__(self, playerNum):
                pygame.sprite.Sprite.__init__(self)
                #set the player number of the profile
                self.playerNum = playerNum
                #set the tank image for the player profile
                self.image = images["tank"+str(self.playerNum)]
                #get rect for the tank image
                self.rect = self.image.get_rect()
                #set dimensions for the tank image rect
                self.rect.topleft = (20,20)
        
        #class for the text for the player (eg. Player 1)
        class playerText(pygame.sprite.Sprite):
            #initialization method
            def __init__(self, parent, playerNum):
                pygame.sprite.Sprite.__init__(self)
                #set the player number of the profile
                self.playerNum = playerNum
                #set the parent of the profile (the background on which the profile will be blitted)
                self.parent = parent
                #set the font for the text
                self.font = pygame.font.Font(fonts["coda"], 30) 
                #render the text into a surface object
                self.image = self.font.render("Player "+str(playerNum), True, colours["black"])
                #get rect of the text object
                self.rect = self.image.get_rect()
                #set the position of the rect
                self.rect.topright = (self.parent.width-10, 10)
        
        #class for each of the images of keyboard keys
        class key(pygame.sprite.Sprite):
            #initialization method
            def __init__(self, parent, profile, type, keyName):
                pygame.sprite.Sprite.__init__(self)
                #set the name of the key
                self.keyName = keyName
                #retrive the image of the key from the image database
                self.image = images["k_"+self.keyName]
                #get rect for the image
                self.rect = self.image.get_rect()
                #set the spacing between each of the keys
                self.edgeSpacing = 10
                #check for the function of the key (left, right, up, down, or shoot)
                if type == "L":
                    #if the key is the move left key, set position of the rect (left-most, bottom-most)
                    self.rect.bottomleft = (self.edgeSpacing, parent.height-self.edgeSpacing)
                if type == "D":
                    #if the key is the move down key, set position of the rect (second left-most, bottom-most)
                    self.rect.bottomleft = (self.edgeSpacing+profile.keyWidth, parent.height-self.edgeSpacing)
                if type == "R":
                    #if the key is the move right key, set position of the rect (third left-most, bottom-most)
                    self.rect.bottomleft = (self.edgeSpacing+profile.keyWidth*2, parent.height-self.edgeSpacing)
                if type == "U":
                    #if the key is the move up key, set position of the rect (second left-most, second bottom-most)
                    self.rect.bottomleft = (self.edgeSpacing+profile.keyWidth, parent.height-self.edgeSpacing-profile.keyHeight)
                if type == "X":
                    #if the key is the shoot key, set position of the rect (right-most, bottom-most)
                    self.rect.bottomright = (parent.width-self.edgeSpacing, parent.height-self.edgeSpacing)
        
        #initialization method
        def __init__(self, num, controls):
            pygame.sprite.Sprite.__init__(self)
            #create a sprite group to store the profile key sprites
            self.playerProfileKeysGroup = pygame.sprite.Group()
            #set the control profile number for the profile
            self.num = num
            #set the player profile number for the profile
            self.playerNum = None
            #set the control set for the profile
            self.controls = controls
            #set the joined status to False
            self.joined = False
            
            #generate background for the profile
            self.image = pygame.Surface((463, 228))
            self.image.fill(colours["grey"])
            #get rect for the background
            self.rect = self.image.get_rect()
            #check for which player this profile is for
            if self.num == 1:
                #if player 1, set position to top left
                self.rect.topleft = (25,95)
            if self.num == 2:
                #if player 2, set position to top right
                self.rect.topright = (975,95)
            if self.num == 3:
                #if player 3, set position to bottom left
                self.rect.bottomleft = (25,575)
            if self.num == 4:
                #if player 4, set position to bottom right
                self.rect.bottomright = (975,575)
                
            #background for keys (with a transparent fill right now, but will change to red or green accordingly)
            self.keyImage = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
            #set up the rect for the key images background 
            self.keyRect = self.rect.copy()
              
            #set up panel to blit key images onto (with transparent fill)
            self.keyPanel = pygame.Surface((450, 225), pygame.SRCALPHA)
            #get rect for the key panel
            self.keyRect = self.keyPanel.get_rect()
            #set up position of the key panel
            self.keyRect.midbottom = (self.rect.width//2, self.rect.height-10)
            
            #for each key in the player's control profile
            for self.keyName in self.controls:
                #convert the name of the key from ascii to a string name
                self.name = pygame.key.name(self.keyName)
                if self.name == "/":
                    #if the name of the key is "/", it is name "slash" in the images database ("/" is not a valid file name)
                    self.name = "slash"
                #create an instance of the key class for each of the keys in the player control profile and add it to
                #the playerProfileKeysGroup sprite group
                self.playerProfileKeysGroup.add(self.key(self.keyRect, self, self.controls[self.keyName], self.name))
                
            #blit the sprite group sprites to the key panel
            self.playerProfileKeysGroup.draw(self.keyPanel)
            #blit the key panel onto the profile background
            self.keyImage.blit(self.keyPanel, self.keyRect)
            #blit the profile background onto the sprite's image
            self.image.blit(self.keyImage, (0,0))
        
        #update the text and images of the player profile
        def update(self, keyPress=None):
            if keyPress != None:
            #if a keyPress has been passed into the method
                if not self.joined:
                    #if the player profile is not joined
                    if keyPress in self.controls:
                        #if the keyPress matches a key in the player control profile
                        global curPlayer
                        #set the joined status variable to True
                        self.joined = True
                        #change background of profile to green
                        self.image.fill(colours["goGreen"])
                        #generate player image background (a transparent background)
                        self.selectedImage = pygame.Surface((450, 225), pygame.SRCALPHA)
                        #get rect of the player image background
                        self.selectedImageRect = self.selectedImage.get_rect()
                        if self.num == 1:
                            #if the player is player 1
                            #create an instance of the playerImage class for the tank image of this profile
                            self.playerIcon = self.playerImage(1)
                            #create an instance of the playerText class to display the player number of this profile
                            self.playerIconText = self.playerText(self.selectedImageRect, 1)
                            #set the playerNum of this profile to 1
                            self.playerNum = 1
                        else:
                            #if the player is NOT player 1
                            #create an instance of the playerImage class for the tank image of this profile
                            self.playerIcon = self.playerImage(curPlayer)
                            #create an instance of the playerText class to display the player number of this profile
                            self.playerIconText = self.playerText(self.selectedImageRect, curPlayer)
                            #set the playerNum of this profile to the curPlayer variable (the following empty player slot)
                            self.playerNum = curPlayer
                            #set the next avaliable player slot to the next one (+1)
                            curPlayer += 1
                            
                        #play sound effect 
                        sounds["powerUp"].play()
                        #blit the player icon image to the selectedImage surface 
                        self.selectedImage.blit(self.playerIcon.image, self.playerIcon.rect)
                        #blit the player profile text to the sprite's image when selected
                        self.selectedImage.blit(self.playerIconText.image, self.playerIconText.rect)
                            
            #update background colour
            if self.joined:
                #if the profile is joined
                #background colour is green
                self.image.fill(colours["goGreen"])
                #blit the selectedImage surface to the sprite's image surface
                self.image.blit(self.selectedImage, (0,0))
            else:
                #if the profile is not joined
                #background colour is red
                self.image.fill(colours["red"])
            #blit the keyImage panel to the sprite's image
            self.image.blit(self.keyImage, (0,0))
    
    #class for the help button in the set up screen
    class helpInstButton(pygame.sprite.Sprite):
        #initialization method
        def __init__(self, bgRect):
            pygame.sprite.Sprite.__init__(self)
            #assign rect of the background to the sprite
            self.bgRect = bgRect
            #image when not selected 
            self.unSelImage = images["help"]
            #not selected image rect
            self.unSelRect = self.unSelImage.get_rect()
            #not selected rect position
            self.unSelRect.topleft = (self.bgRect.left, self.bgRect.bottom+10)
            #image when selected
            self.selImage = images["helpInst"]
            #selected image rect
            self.selRect = self.selImage.get_rect()
            #selected rect position
            self.selRect.bottomleft = self.unSelRect.bottomleft
            #set image and rect to unselected mode (default is not selected)
            self.image = self.unSelImage
            self.rect = self.unSelRect
        
        #update the sprite image
        def update(self, mousePos):
            if self.rect.collidepoint(mousePos):
                #if the rect of the image collides with the mouse position (selected)
                self.image = self.selImage
                self.rect = self.selRect
            else:
                #else - rect does not collide with the mouse position
                self.image = self.unSelImage
                self.rect = self.unSelRect
            
    #generate the set up screen with the same dimesions as the game 
    setupScreen = pygame.surface.Surface(size)
    
    #create a grey background from an image
    setupGameBG = images["SGbg"]
    #get the rect of the grey background image
    setupGameBGRect = setupGameBG.get_rect()
    #center the grey background image within the screen
    setupGameBGRect.center = setupScreen.get_rect().center
    
    #create a player profile for each of the possible players (1-4)
    for player in range(1, 4+1):
        #add the player profile to a dictionary containing all the profiles
        playerProfileDict[player] = playerProfile(player, tankControls[player])
        #add the profile to a sprite group containing all of the set up screen sprites
        playerProfileGroup.add(playerProfileDict[player])
    
    #set up the help button (create an instance of the helpInsButton class)
    helpButton = helpInstButton(setupGameBGRect)
    
    #set up the instructions and add it to a sprite group containing all of the set up screen sprites
    playerProfileGroup.add(profileInstructions(setupGameBGRect))
    
    #set up the curPlayer counter (the next avaliable player slot)
    global curPlayer
    curPlayer = 2
    
    #keep going flag
    global setupKeepGoing
    setupKeepGoing = True
    
    #create a dictionary which store the player controls data {control set:player number}
    global controlsPlayerDict
    controlsPlayerDict = {}
    
    while setupKeepGoing:
        #Set up fps rate
        clock.tick(fpsRate)
        
        #check for events
        for ev in pygame.event.get():
            if ev.type == pygame.KEYDOWN:
                #key is pressed
                #update profile objects with the key pressed
                playerProfileGroup.update(ev.key)
            if ev.type == pygame.QUIT:
                #if the close button is clicked
                setupKeepGoing = False
                #close the game
                pygame.quit()
                sys.exit()
        
        #get the mouse position
        mousePos = pygame.mouse.get_pos()
        #set up the dirt background
        setupScreen.blit(images["bgImage"], (0,0))
        #blit a mask over the dirt background to make it darker
        setupScreen.blit(pygame.transform.scale(images["GObg"], size), (0,0))
        #update player profiles
        playerProfileGroup.update()
        #blit player profiles to the set up game screen background
        playerProfileGroup.draw(setupGameBG)
        #blit set up game screen background onto the set up game screen
        setupScreen.blit(setupGameBG, setupGameBGRect)
        #blit the set up game screen to the actual game screen
        screen.blit(setupScreen, (0,0))
        #update the help button 
        helpButton.update(mousePos)
        #blit the help button to the background
        screen.blit(helpButton.image, helpButton.rect)
        #update screen
        pygame.display.update()
    
    #stop set up background music
    pygame.mixer.music.stop()
    #return a dictionary containing player numbers mapped to their control sets
    return controlsPlayerDict
        
#START GAME
def startGame(resourcePath, mapNum, numPlayer, bgMusicName, score, returnMainMenu, controlsPlayerDict):
    global tankControls
    global screen
    global images
    global sounds
    global size 
    global fonts
    global colours
    global musicOn
    global testMode
    
    #Countdown screen before game starts
    def preGameStart(gameScreen):
        global fonts
        global screen
        global sounds
        #countdown from this number (default 3)
        countDownLimit = 3
        #countdown text
        countDownFont = pygame.font.Font(fonts["bops1"], size[1]//5)
        #background - makes screen darker
        preGameBG = pygame.transform.scale(images["GObg"], size)
        preGameBGRect = preGameBG.get_rect()
        preGameBGRect.center = screen.get_rect().center
        #set up countdown number tracker
        countDownNum = countDownLimit
        #set up countdown number length tracker (see below)
        countDownNumLen = 0
        #set up countdown number length limit (how long each number will remain on screen)
        #1 second = fpsRate ticks
        countDownNumLenLimit = fpsRate
        
        while countDownNum >= 0:
            #Set up fps rate
            clock.tick(fpsRate)
            
            #check for events
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    #if close button is pressed
                    pygame.quit()
                    sys.exit()
                
            #set up the text
            if countDownNum > 0: 
                #countdown number is greater than 0
                if countDownNumLen == 0:
                    #if the number has just been displayed --> play beep sound
                    sounds["countDown"].play()
                #turn interger into string to display
                text = str(countDownNum)
            else:
                #countdown finished (at 0) --> Start!
                if countDownNumLen == 0:
                    #play sound if number has just been displayed
                    sounds["countDownFin"].play()
                #text to display is "Start!"
                text = "Start!"
            
            #render text using font
            countDownText = countDownFont.render(text, True, colours["light grey"])
            #get rect of text and center it
            countDownRect = countDownText.get_rect()
            countDownRect.center = screen.get_rect().center
            
            #blit images to screen
            screen.blit(gameScreen, (0,0))
            screen.blit(preGameBG, preGameBGRect)
            screen.blit(countDownText, countDownRect)
            
            #update the screen
            pygame.display.update()
            
            #add 1 to the countdown number length tracker (how long the number has been displayed)
            countDownNumLen += 1
            
            if countDownNumLen > countDownNumLenLimit:
            #if the number has been displayed long enough (default 1 sec = fpsTick Rate)
                #go to the next number
                countDownNumLen = 0
                countDownNum -= 1
    
    #Game Over Function
    def gameOver(ranking, gameScreen, returnMainMenu, score, controlsPlayerDict):
        global screen
        global fonts
        global prevSlotYPos
        
        #create sprite groups
        leadrbrdMouseGroup = pygame.sprite.Group()
        leadrbrdGroup = pygame.sprite.Group()
        leadrbrdObjGroup = pygame.sprite.Group()
        
        #class for each row in the rankings table
        class rankingSlot(pygame.sprite.Sprite):
            #slot for the title cells (top row headings)
            class rankingTitle(pygame.sprite.Sprite):
                #initialization method
                def __init__(self, obj, col, slot):
                    #set the slot which the title object where be will placed
                    self.slot = slot
                    #set the column where the title object will be placed
                    self.col = col
                    #make this object a pygame sprite
                    pygame.sprite.Sprite.__init__(self)
                    #set up the font
                    self.font = pygame.font.Font(fonts["roboto"], 15)
                    #render the text into a surface using the font
                    self.titleText = self.font.render(obj[0], True, colours["black"])
                    #set up image of the object
                    self.titleImage = obj[1]
                    self.image = self.titleImage
                    #get the rect of the object
                    self.rect = self.image.get_rect()
                    #position the rect
                    self.rect.center = (75*(self.col-1)+30+self.slot.rect.left, self.slot.rect.centery)
                    #get the rect of the image of the object
                    self.imageRect = self.rect.copy()
                
                #check if mouse collides with slot
                def update(self, mousePos):
                    #check if mouse is colliding with the heading image
                    if self.imageRect.collidepoint(mousePos):
                        #if collide - show the text text
                        self.image = self.titleText
                    else:
                        #else no collide - show the image
                        self.image = self.titleImage
                    #reset the rect and reposition it
                    self.rect = self.image.get_rect()
                    self.rect.center = (75*(self.col-1)+30+self.slot.rect.left, self.slot.rect.centery)
                    
            #class for the text for each player cell
            class rankingText(pygame.sprite.Sprite):
                #initialization method
                def __init__(self, text, col, slot):
                    #make this a pygame sprite
                    pygame.sprite.Sprite.__init__(self)
                    #set column where it will be placed
                    self.col = col
                    #set slot (row) where it will be placed
                    self.slot = slot
                    #set up font
                    self.font = pygame.font.Font(fonts["roboto"], 25)
                    #render the text into a surface using the font
                    self.image = self.font.render(text, True, colours["light grey"])
                    #get rect and center it
                    self.rect = self.image.get_rect()
                    self.rect.center = (75*(self.col-1)+30+self.slot.rect.left, self.slot.rect.centery)
                    
            #class for the image for each player cell
            class rankingImage(pygame.sprite.Sprite):
                #initialization method
                def __init__(self, num, image, col, slot):
                    #make this a pygame sprite
                    pygame.sprite.Sprite.__init__(self)
                    #set the player number
                    self.num = num
                    #set the slot (row) where it will be placed
                    self.slot = slot
                    #set the column where it will be placed
                    self.col = col
                    #set up the image
                    self.tankImage = image
                    self.image = self.tankImage
                    #get rect of the image and center
                    self.rect = self.image.get_rect()
                    self.rect.center = (75*(self.col-1)+30+self.slot.rect.left, self.slot.rect.centery)
                    #get the rect of the object when its image is dispalyed
                    self.imageRect = self.rect.copy()
                    #set up the font
                    self.font = pygame.font.Font(fonts["roboto"], 20)
                    #render the text into a surface using the font
                    self.text = self.font.render("Player "+str(self.num), True, colours["light grey"])
              
                #check if mouse collides with image
                def update(self, mousePos):
                    if self.imageRect.collidepoint(mousePos):
                        #display text - collide
                        self.image = self.text
                    else:
                        #display image - no collide
                        self.image = self.tankImage
                    #get rect for text/image and center it
                    self.rect = self.image.get_rect()
                    self.rect.center = (75*(self.col-1)+30+self.slot.rect.left, self.slot.rect.centery)
            
            #initialization method
            def __init__(self, bgRect, data, place=None):
                #the y pos of the bottom of the last slot
                global prevSlotYPos
                #make it a pygame sprite
                pygame.sprite.Sprite.__init__(self)
                #get the rect of the background of the slot
                self.bg = bgRect
                #set the spacing between the slots
                self.spacing = 10
                
                if data["num"] == 0:
                    #this is the headings (first) slot
                    #the background image for the slot (yellow slot) 
                    self.image = images["rankSlotTitle"]
                    #get rect for the background image
                    self.rect = self.image.get_rect()
                    #center the background rect
                    self.rect.midtop = (self.bg.midtop[0], prevSlotYPos+self.spacing)
                    #update the prevSlotYPos (the y pos of the bottom of the previous slot)
                    prevSlotYPos += self.image.get_height()+self.spacing
                    #create a data set for each column of the slot with the text and image
                    self.data = []
                    self.data.append(("Rank", images["rankingBlank"]))
                    self.data.append(("Tank", images["rankingBlank"]))
                    self.data.append(("Shots Fired", images["shotsFired"]))
                    self.data.append(("Shots Hit", images["shotsHit"]))
                    self.data.append(("Accuracy", images["accuracy"]))
                    self.data.append(("Shots Taken", images["shotsTaken"]))
                    self.data.append(("Power Ups", images["powerUp"]))
                    self.data.append(("Time", images["time"]))
                    #for each column in the data set --> create raknkingTitle object for that column
                    for num, titleObj in enumerate(self.data):
                        #                         (data, column num, the background slot)
                        newObj = self.rankingTitle(titleObj, num+1, self)
                        #add to sprite group of interactive objects 
                        leadrbrdMouseGroup.add(newObj)
                        #add to leaderboard objects group
                        leadrbrdObjGroup.add(newObj)
                    
                else:
                    #else - it is a slot for one of the players
                    #set the background image for the slot (black slot)
                    self.image = images["rankSlot"]
                    #get rect for the background image
                    self.rect = self.image.get_rect()
                    #position the background image 
                    self.rect.midtop = (self.bg.midtop[0], prevSlotYPos+self.spacing)
                    #update the prevSlotYPos (the y pos of the bottom of the previous slot)
                    prevSlotYPos += self.image.get_height()+self.spacing
                    #create a data set for each column of the slot with the text and image
                    self.data = []
                    #the place (1st, 2nd, 3rd, etc.)
                    self.data.append(str(place))
                    #image of the tank
                    self.data.append(images["tank"+str(data["num"])])
                    #shots fired
                    self.data.append(str(data["shots"]))
                    #shots taken
                    self.data.append(str(data["kills"]))
                    #accuracy
                    if data["shots"] > 0:
                        #calculate accuracy if shots fired is > 0 
                        self.data.append("%.1f%s" %(data["kills"]/data["shots"]*100, "%"))
                    else:
                        #else - no shots fired (cannot divide by 0)
                        self.data.append("0%")
                    #damage taken
                    self.data.append(str(data["damage"]))
                    #number of power ups used
                    self.data.append(str(data["powerUps"]))
                    #time survived (how long the tank survived)
                    if type(data["time"]) == float:
                        #if the tank has died (there is a float representing the amount of time the
                        #tank survived) --> convert into min:seconds
                        self.data.append(str(int(data["time"]//60))+":"+str(int(data["time"]%60)).zfill(2))
                    else:
                        #else - it is the winning tank (no time)
                        self.data.append(data["time"])
                        
                    #for each column, create objects representing its data
                    for num, infoObj in enumerate(self.data):
                        if type(infoObj) != str:
                            #the column contains image and text (when moused over)
                            newObj = self.rankingImage(data["num"], infoObj, num+1, self)
                            #add to interactive group
                            leadrbrdMouseGroup.add(newObj)
                        else:
                            #the column contains only text
                            newObj = self.rankingText(infoObj, num+1, self)
                        #add to the leaderboard object group
                        leadrbrdObjGroup.add(newObj)
        
        #class for the help button (game over screen)
        class helpButton(pygame.sprite.Sprite):
            #class for the text of the help button
            class helpText(pygame.sprite.Sprite):
                #initialization method
                def __init__(self, helpBox, text):
                    #set the text
                    self.text = text
                    #set rect where the text will be blitted
                    self.helpBox = helpBox
                    #make this a pygame sprite
                    pygame.sprite.Sprite.__init__(self)
                    #set the font
                    self.font = pygame.font.Font(fonts["openSans"], 25)
                    #render the text into a surface using the font
                    self.image = self.font.render(self.text, True, colours["white"])
                    #get the rect for the surface
                    self.rect = self.image.get_rect()
                    #center the text on the background rect
                    self.rect.midleft = (self.helpBox.rect.left+images["help"].get_rect().right+10,
                    self.helpBox.rect.top+self.helpBox.image.get_rect().height//2)
            
            #initialization method
            def __init__(self, text, bgRect):
                global prevSlotYPos
                #make this a pygame sprite
                pygame.sprite.Sprite.__init__(self)
                #set the y pos of the bottom of the last slot of the ranking table
                self.prevSlotYPos = prevSlotYPos
                #set a boolean to keep track of whether the help button is expanded
                self.expanded = False
                #set the background on which the help button will be blitted on
                self.bgRect = bgRect
                #set the image 
                self.image = images["help"]
                #get the rect
                self.rect = self.image.get_rect()
                #position the rect
                self.rect.topleft = (self.bgRect.left, self.prevSlotYPos+10)
                #update the prevSlotYPos 
                prevSlotYPos += self.rect.height+10
                #set the text (using the helpText class)
                self.text = self.helpText(self, text)
                
            def update(self, mousePos):
                #check if mouse collides with help button
                if self.rect.collidepoint(mousePos):
                    #expand the help button
                    self.image = images["helpLong"] 
                    leadrbrdObjGroup.add(self.text)
                else:
                    #shrink the help butotn
                    self.image = images["help"] 
                    leadrbrdObjGroup.remove(self.text)
                #update rect
                self.rect = self.image.get_rect()
                self.rect.topleft = (self.bgRect.left,self.prevSlotYPos+10)
        
        #class for each button at the bottom of the rankings table
        class bottomButtons(pygame.sprite.Sprite):
            def __init__(self, type):
                pygame.sprite.Sprite.__init__(self)
                #set what type the button
                self.type = type
                #set images and rect for the button
                self.selImage = images[self.type+"ButSel"]
                self.unSelImage = images[self.type+"But"]
                self.image = self.unSelImage
                self.rect = self.image.get_rect()
                
            def update(self, mousePos):
                #check whether the mouse pos has collided with the button
                if self.rect.collidepoint(mousePos):
                    #collided - use lighter image
                    self.image = self.selImage
                else:
                    #not collide - use darked image
                    self.image = self.unSelImage
                  
            def clicked(self, controlsPlayerDict, score):
                #if clicked
                if self.type == "restart":
                    #if restart button clicked
                    pygame.mixer.music.stop()
                    pygame.mixer.stop()
                    #get new controls
                    controlsPlayerDict = userSetup(resourcePath, setupMusicName)
                    numPlayer = len(controlsPlayerDict)
                    #set up score tracker
                    score = {}
                    for player in range(1, numPlayer+1):
                        score[player] = 0
                    #start new game
                    startGame(resourcePath, mapNum, numPlayer, bgMusicName, score, returnMainMenu, controlsPlayerDict)
                if self.type == "mainMenu":
                    #if main menu pressed
                    pygame.quit()
                    sys.exit()
                if self.type == "playAgain":
                    #if play again pressed
                    pygame.mixer.music.stop()
                    pygame.mixer.stop()
                    #start new game
                    numPlayer = len(controlsPlayerDict)
                    startGame(resourcePath, mapNum, numPlayer, bgMusicName, score, returnMainMenu, controlsPlayerDict)
                if self.type == "quit":
                    #if quit pressed
                    pygame.quit()
                    sys.exit()
        
        #class for the scoreboard
        class scoreboard(pygame.sprite.Sprite):
            def __init__(self, score):
                pygame.sprite.Sprite.__init__(self)
                global prevSlotYPos
                self.prevSlotYPos = prevSlotYPos
                self.spacing = 3
                #score of the player
                self.score = score
                #set image as a blank square
                self.image = pygame.Surface(((50-self.spacing)*len(self.score)+self.spacing, 50))
                #position the rect of the image
                self.rect = self.image.get_rect()
                self.rect.midtop = (gameOverLBRect.centerx, self.prevSlotYPos)
                #update the prevSlotYPos
                prevSlotYPos += self.rect.height+10 
                #set font
                self.scoreFont = pygame.font.Font(fonts["openSansBold"], 23)
                self.prevXPos = self.spacing
                for player in range(1, len(score)+1):
                    #for each player, make a square to show their score
                    self.tempImage = pygame.Surface((50-self.spacing*2, 50-self.spacing*2))
                    self.tempImageRect = self.tempImage.get_rect()
                    
                    #set the background colour according to the player number
                    if player == 1:
                        self.tempImage.fill(colours["blue"])
                    if player == 2:
                        self.tempImage.fill(colours["green"])
                    if player == 3:
                        self.tempImage.fill(colours["pink"])
                    if player == 4:
                        self.tempImage.fill(colours["orange"])
                    
                    #create the text 
                    self.tempText = self.scoreFont.render(str(score[player]), True, colours["black"])
                    self.tempTextRect = self.tempText.get_rect()
                    self.tempTextRect.center = self.tempImageRect.center
                    #blit the text onto the square
                    self.tempImage.blit(self.tempText, self.tempTextRect)
                    #blit the square onto the scoreboard image
                    self.tempImageRect.topleft = (self.prevXPos, self.spacing)
                    self.image.blit(self.tempImage, self.tempImageRect)
                    self.prevXPos += 50-self.spacing
                    
                
        #play victory sound
        pygame.mixer.stop()
        sounds["victory"].play()
        
        #game over leaderboard background (a template to position the objects on)
        gameOverLB = images["LBbg"]
        gameOverLBRect = gameOverLB.get_rect()
        gameOverLBRect.center = screen.get_rect().center
        
        #game over background (darkens the screen)
        gameOverBG = pygame.transform.scale(images["GObg"], size)
        gameOverBGRect = gameOverBG.get_rect()
        gameOverBGRect.center = screen.get_rect().center
        
        #add players to a dictionary containing all the scores 
        for place, player in enumerate(ranking):
            score[player["num"]] += place
        
        #create the scoreboard at the top
        global prevSlotYPos
        prevSlotYPos = (gameOverLBRect.top)
        leadrbrdGroup.add(scoreboard(score))
        
        #creat the ranking title text
        #font
        rankingFont = pygame.font.Font(fonts["bops1"],35)
        #surface
        rankingSur = rankingFont.render("Rankings", True, colours["light grey"])
        #rect
        rankingRect = rankingSur.get_rect()
        rankingRect.midtop = (gameOverLBRect.centerx, prevSlotYPos)
        #background
        rankingTitleBG = images["rankingTitleBG"]
        #center the title text
        rankingTitleRect = rankingTitleBG.get_rect()
        rankingTitleRect.center = rankingRect.center
        prevSlotYPos += rankingRect.height
        
        #create the leaderboard slots
        leadrbrdGroup.add(rankingSlot(gameOverLBRect ,{"num":0}))
        ranking.reverse()
        for place, player in enumerate(ranking):
            leadrbrdGroup.add(rankingSlot(gameOverLBRect, player, place+1))
        
        
        #create the help button
        rankingsHelpButton = helpButton("Mouse Over Images for Explanation", gameOverLBRect)    
        leadrbrdMouseGroup.add(rankingsHelpButton)
        leadrbrdGroup.add(rankingsHelpButton)
        
        #create the buttons at the bottom
        bottomButtonBar = []
        prevSlotYPos += 10
        buttonSpacing = 10
        leadrbrdButRestart = bottomButtons("restart")
        leadrbrdButPlayAgain = bottomButtons("playAgain")
        if returnMainMenu:
            leadrbrdButMainMenu = bottomButtons("mainMenu")
        else:
            leadrbrdButMainMenu = bottomButtons("quit")
        
        #set the rects for the buttons
        leadrbrdButMainMenu.rect.midtop = (gameOverLBRect.centerx, prevSlotYPos)
        leadrbrdButPlayAgain.rect.topleft = (leadrbrdButMainMenu.rect.right+buttonSpacing, prevSlotYPos)
        leadrbrdButRestart.rect.topright = (leadrbrdButMainMenu.rect.left-buttonSpacing, prevSlotYPos)
        
        #add the buttons to interactive group and leaderboard object group
        leadrbrdMouseGroup.add(leadrbrdButMainMenu)
        leadrbrdMouseGroup.add(leadrbrdButPlayAgain)
        leadrbrdMouseGroup.add(leadrbrdButRestart)
        leadrbrdGroup.add(leadrbrdButMainMenu)
        leadrbrdGroup.add(leadrbrdButPlayAgain)
        leadrbrdGroup.add(leadrbrdButRestart)
        #add buttons to a list containing all the buttons
        bottomButtonBar.append(leadrbrdButMainMenu)
        bottomButtonBar.append(leadrbrdButPlayAgain)
        bottomButtonBar.append(leadrbrdButRestart)
      
        #show leaderboard flag
        showLeaderboard = True
        
        while showLeaderboard:
            #Set up fps rate
            clock.tick(fpsRate)
            
            #fill background
            screen.fill((100,100,100))
            
            #check if sound is being played, if not - play leaderboard music
            if not pygame.mixer.get_busy():
                sounds["leaderboard"].play(loops=-1)
            
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    #close button pressed
                    keepGoing = False
                if ev.type == pygame.KEYDOWN:
                    #escape is pressed
                    if ev.key == K_ESCAPE:
                        keepGoing = False
                        break
                    #selection key (space bar is pressed)
                    if ev.key == selectKey:
                        #default - play again
                        leadrbrdButPlayAgain.clicked(controlsPlayerDict, score)
                        
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    if ev.button == 1:
                        #if mouse button 1 is pressed
                        for button in bottomButtonBar:
                            #for button in the button list
                            if button.rect.collidepoint(ev.pos):
                                #if the button collided with the mouse pos --> run the clicked method
                                button.clicked(controlsPlayerDict, score)
                                
            #get mouse position
            mousePos = pygame.mouse.get_pos()
            
            #update interactive sprites
            leadrbrdMouseGroup.update(mousePos) 
            
            #blit stuff to screen
            screen.blit(gameScreen, (0,0))
            screen.blit(gameOverBG, gameOverBGRect)
            screen.blit(gameOverLB, gameOverLBRect)
            screen.blit(rankingTitleBG, rankingTitleRect)
            screen.blit(rankingSur, rankingRect)
            
            #draw background images
            leadrbrdGroup.draw(screen)
            
            #draw foreground images
            leadrbrdObjGroup.draw(screen)
            
            #update the display
            pygame.display.update()

    #Set up keepGoing flag
    keepGoing = True

    #Setup game screen
    gameScreen = pygame.surface.Surface(size)
    
    #class for each of the tanks
    class Tank(pygame.sprite.Sprite):   
        #initialization method
        def __init__(self, x, y, num, numPlayer, powerUpList, settings, controlNum):
            #player number
            self.num = num
            #control set number
            self.controlNum = controlNum
            #the image number
            self.tankNum = self.num
            #set up tank settings
            #               [ammo, life]
            self.settings = settings
            self.dead = False
            self.face = "R"
            self.totalPlayer = numPlayer
            #missile settings
            self.missileRegenTime = 2
            self.missileRegenCount = 0
            self.missileLimit = self.settings[0]
            self.missileLeft = self.missileLimit
            self.missilePower = 1
            #movement settings
            self.moveRate = 3  
            self.defaultMoveRate = self.moveRate
            #life settings
            self.lives = self.settings[1]
            #image settings
            self.imageNum = str(self.tankNum)
            #power up settings
            self.powerUpTime = 10
            #set up stats tracker (for leaderboard)
            self.totalShot = 0
            self.hitShot = 0
            self.damage = 0
            self.powerUpCount = 0
            #whether tank becomes a ghost when it dies (for testing purposes)
            self.ghost = False
            #if the tank has been added to the rank list
            self.addedToRankList = False
            #list of the tank movement keys
            self.moveList = []
            #whether the tank can slide sideways
            self.slide = True
            if testMode:
                #TESTING STUFF
                self.missileLeft = 1000000
                self.ghost = True
                
            #power up status (default is False)
            self.powerUpStatus = {}
            for powerUp in powerUpList:
                self.powerUpStatus[powerUp] = False
   
            #create tank
            pygame.sprite.Sprite.__init__(self)
            #set image
            self.image = images["tank"+self.imageNum+"R"]
            #set rect
            self.rect = self.image.get_rect()
            self.rect.x = x
            #run y cord through getYCord function (adds the status bar height into the y cord)
            self.rect.y = getYCord(y)
            #set facing direction
            self.prevFace = self.face
        
        #when the tank moves
        def move(self, deltaX, deltaY, face):
            #if the tank cannot move in that direction (hits wall or other tank)
            def undoMove(self):
                #undo movement
                self.rect = self.tempRect.copy()
                self.image = self.tempImage
                self.face = self.prevFace
        
            #set facing direction
            self.face = face
            #set temp in case of collision
            self.tempRect = self.rect.copy()
            self.tempImage = self.image
            #change image
            self.image = images["tank"+self.imageNum+self.face]
            #get new dimensions
            self.rect.width = self.image.get_width()
            self.rect.height = self.image.get_height()
            #move tank (sets which way the tank turns if it turns - tank turns differently depending
            #on which way it was facing and which way it now is facing)
            if self.prevFace == "R":
                #previously facing right
                if self.face == "D": 
                    self.rect.topright = self.tempRect.topright
                elif self.face == "U":
                    self.rect.bottomright = self.tempRect.bottomright
                else:
                    self.rect.center = self.tempRect.center
            if self.prevFace == "L":
                #previously facing left
                if self.face == "D": 
                    self.rect.topleft = self.tempRect.topleft
                elif self.face == "U":
                    self.rect.bottomleft = self.tempRect.bottomleft
                else:
                    self.rect.center = self.tempRect.center
            if self.prevFace == "U":     
                #previously facing up
                if self.face == "L":
                    self.rect.topright = self.tempRect.topright
                elif self.face == "R":
                    self.rect.topleft = self.tempRect.topleft
                else:
                    self.rect.center = self.tempRect.center
            if self.prevFace == "D":
                #previously facing down
                if self.face == "L":
                    self.rect.bottomright = self.tempRect.bottomright
                elif self.face == "R":
                    self.rect.bottomleft = self.tempRect.bottomleft
                else:
                    self.rect.center = self.tempRect.center
            
            #add change to the x and y cord
            self.deltaX = deltaX*self.moveRate
            self.deltaY = deltaY*self.moveRate
            self.rect.x += self.deltaX
            self.rect.y += self.deltaY
            
            #create temp tank group without current tank for collision detection
            tempTankGroup = tankGroup.copy()
            tempTankGroup.remove(self)
            
            #check for collision with wall
            if pygame.sprite.spritecollide(self, wallGroup, False):
                #if collision with wall
                if not self.slide:
                    #if not slideable
                    self.confirmMove = False
                else:
                    #if slideable
                    #undo move
                    undoMove(self)
                    #try moving sideways
                    self.rect.x += self.deltaX
                    self.rect.y += self.deltaY
                    #check if it still collides
                    if pygame.sprite.spritecollide(self, wallGroup, False):
                        #if still collides, undo move again
                        undoMove(self)
                
            #check for collision with other tanks
            elif pygame.sprite.spritecollide(self, tempTankGroup, False):
                #if collide - undo move
                undoMove(self) 
            else:
                #confirm movement (set the prevFace to the current face)
                self.prevFace = self.face
        
        #when tank launches missile
        def launch(self):
            #if infinite missile powerup --> missileLeft = -1
            if self.missileLeft == -1 or self.missileLeft > 0:
                #add 1 to the shots it has fired
                self.totalShot += 1
                if self.missileLeft > 0:
                    #if the number of missiles the tank has left is > 0 (no powerup) -> update the
                    #missile left count
                    self.missileLeft -= 1
                #create a missile object (launch the missile)
                missileGroup.add(Missile(self, self.face, self.missilePower))
                #print("LAUNCH MISSILE BY TANK", self.num, self.missileLeft, "MISSILES LEFT")               
        
        #tank collide with a missile
        def collide(self, colMissile, missilePower):
            #create explosion
            explosionGroup.add(Explosion(self, "Tank"))
            #subtract the missile's damaging power from the lives of the tank
            self.lives -= missilePower
            #add to the amount of damage the tank took
            self.damage += missilePower
            #print("COLLIDE WITH TANK", self.num, "-", self.lives, "LIVES LEFT")
        
        #add the tank to the rankings 
        def addToRankings(self):
            global playerRank
            global gameTimeCounter

            if not self.addedToRankList:
                #if the tank has not already been added to the rankings list
                if self.dead:
                    #if the tank is dead
                    self.addedToRankList = True
                    playerRank.append({"num":self.num, "shots":self.totalShot, "kills":self.hitShot,
                    "damage":self.damage, "time":(gameTimeCounter/60), "powerUps":self.powerUpCount})
                else:
                    #if the tank is still alive (difference: there is no time data (the tank has not died))
                    self.addedToRankList = True
                    playerRank.append({"num":self.num, "shots":self.totalShot, "kills":self.hitShot,
                    "damage":self.damage, "time":"-", "powerUps":self.powerUpCount})
        
        #update the tank position and status (run once every cycle)
        def update(self):
            global tankStat
            
            #MISSILE REGENERATION
            if not self.dead and self.missileLeft != -1:
                #if the tank is not dead and it does not have infinite ammo power up
                #add one to the missile regen count
                self.missileRegenCount += 1
                if self.missileRegenCount >= self.missileRegenTime*fpsRate:
                    #if the missile regen count has reached the limit (time is up for the regen count)
                    if self.missileLeft < self.missileLimit:
                        #if missile left is less than the max limit -> add one missile to missile left
                        self.missileLeft += 1
                        #print("MISSILE REGEN")
                    #reset missile left
                    self.missileRegenCount = 0
                
            #CHECK IF LIVES ARE LESS THAN OR EQUAL TO 0
            if self.lives <= 0:
                if not self.dead:
                    #if not dead -> set the dead status to True and add to rankings list
                    self.dead = True
                    self.addToRankings()
                if not self.ghost:
                    #if ghost is False -> destory the tank, remove from tank list, and remove from control detection list
                    self.kill()
                    tankDict.pop(self.num)
                    controlNumList.remove(self.controlNum)
                else:
                    #if ghost is True -> tank image disappears, but it has infinite ammo and can still move around
                    self.image = images["blank"]
                    if self.missileLeft <= 1:
                        self.missileLeft += 1   
            #add the status of the tank to the list of statuses
            tankStat.append(self.dead) 
                          
            #CHECK IF THE TANK HAS RECIEVED ANY POWER UPS
            for powerUp in self.powerUpStatus:
                #for every power up in the powerUpStatus dictionary
                if not self.powerUpStatus[powerUp] is False:
                    #if the power up status is NOT False
                    
                    #INFINITE AMMO 
                    if powerUp == "ammoInfin":
                        if self.powerUpStatus[powerUp] is True:
                            #just got power up -> set the missileLeft to -1 and set power up timer
                            self.powerUpStatus[powerUp] = self.powerUpTime*fpsRate
                            self.missileLeft = -1  
                        elif self.powerUpStatus[powerUp] <= 0:
                            #if power up time has run out -> return to normal settings
                            self.missileLeft = self.missileLimit
                            self.powerUpStatus[powerUp] = False
                        else:
                            #else - power up in progress, update power up timer
                            self.powerUpStatus[powerUp] -= 1
                            
                    #FASTER SPEED
                    if powerUp == "speed":
                        if self.powerUpStatus[powerUp] is True:
                            #just got power up -> add 2 to the speed and set power up timer
                            self.powerUpStatus[powerUp] = self.powerUpTime*fpsRate
                            self.moveRate = self.defaultMoveRate+2
                        elif self.powerUpStatus[powerUp] <= 0:
                            #if power up time has run out -> return to normal settings
                            self.moveRate = self.defaultMoveRate
                            self.powerUpStatus[powerUp] = False
                        else:
                            #else - power up in progress, update power up timer
                            self.powerUpStatus[powerUp] -= 1    
                    
                    #DOUBLE LIFE
                    if powerUp == "doubleLife":
                        if self.powerUpStatus[powerUp] is True:
                            #just got power up -> double the number of lives if it is less than max lives
                            self.lives *= 2
                            if self.lives > self.settings[1]:
                                self.lives = self.settings[1]
                            self.powerUpStatus[powerUp] = False
                            
                    #STRONGER AMMO
                    if powerUp == "ammoPower":
                        if self.powerUpStatus[powerUp] is True:
                            #just got power up -> set missile damage to 4 and set power up timer
                            self.powerUpStatus[powerUp] = self.powerUpTime*fpsRate
                            self.missilePower = 4
                        elif self.powerUpStatus[powerUp] <= 0:
                            #if power up time has run out -> return to normal settings
                            self.missilePower = 1
                            self.powerUpStatus[powerUp] = False
                        else:
                            #else - power up in progress, update power up timer
                            self.powerUpStatus[powerUp] -= 1  
    
    #class for explosions
    class Explosion(pygame.sprite.Sprite):
        #initialization method
        def __init__(self, colObj, type, othObj=0):
            #set type of explosion (big - tank or small - missile)
            self.type = type
            #set the number of frames to display per cycle
            self.frameRate = 2
            self.frame = self.frameRate
            pygame.sprite.Sprite.__init__(self)
            
            #BIG EXPLOSION 
            if self.type == "Tank":
                #play explosion sound
                sounds["bigExplosion"].play()
                #set image and position it on the object it hit
                self.image = images["explosion1"]
                self.rect = self.image.get_rect()
                self.rect.center = colObj.rect.center
                
            #SMALL EXPLOSION
            elif self.type == "Missile":
                #play explosion sound
                sounds["smallExplosion"].play()
                self.image = images["sExplosion1"]
                #set image and get rect of the two objects
                self.rect = self.image.get_rect()
                posObj1 = colObj.rect.center
                posObj2 = othObj.rect.center
                #get midpoint between two missiles
                midPoint = (posObj2[0]+((posObj1[0]-posObj2[0])//2), posObj2[1]+((posObj1[1]-posObj2[1])//2))
                #position the explosion at the midpoint
                self.rect.center = midPoint
        
        #update the explosion
        def update(self):
            if self.frame <= 18*self.frameRate:
                #if the frames has not reached the end
                if self.type == "Tank":
                    #big explosion
                    self.image = images["explosion"+str((self.frame//self.frameRate)+1)]
                elif self.type == "Missile":
                    #small explosion
                    self.image = images["sExplosion"+str((self.frame//self.frameRate)+1)]
                #update frame rate
                self.frame += 1
            else:
                #frames has reached the end, animation complete, destory object
                self.kill()
    
    #class for missiles
    class Missile(pygame.sprite.Sprite): 
        #initialization method
        def __init__(self, tank, face, missilePower):
            #set missile speed
            self.missileRate = 12
            
            #PLAY PEW SOUND
            #sounds["shoot"].play()
            
            #set where the missile is launched
            self.tank = tank
            self.tankX = self.tank.rect.x
            self.tankY = self.tank.rect.y
            missileLaunch = {"R":(75, 25), "U":(25,0), "L":(0,25), "D":(25,75)}
            #set which direction the missile is facing
            self.face = face
            #set damage power of the missile
            self.missilePower = missilePower
            #if missile will explode if it hits a wall
            self.wallExplosion = True
            #create missile
            pygame.sprite.Sprite.__init__(self)
            self.image = images["missile"+face]
            self.rect = self.image.get_rect()
            
            if self.face == "U":
                #if facing up
                self.rect.midbottom = (self.tankX+(missileLaunch[self.face][0]), self.tankY+(missileLaunch[self.face][1]))
            if self.face == "D":
                #if facing down
                self.rect.midtop = (self.tankX+(missileLaunch[self.face][0]), self.tankY+(missileLaunch[self.face][1]))
            if self.face == "R":
                #if facing right
                self.rect.midleft = (self.tankX+(missileLaunch[self.face][0]), self.tankY+(missileLaunch[self.face][1]))
            if self.face == "L":
                #if facing left
                self.rect.midright = (self.tankX+(missileLaunch[self.face][0]), self.tankY+(missileLaunch[self.face][1]))
            
            #create a list of walls the missile collides with
            collideWallList = pygame.sprite.spritecollide(self, wallGroup, False)            
            if collideWallList:
                #if there is a collision
                for collideWall in collideWallList:
                    #for every wall it hit, run the hitWall method
                    self.hitWall(collideWall)     
            else:
                #otherwise - move the missile
                self.move(self.missileRate)
        
        #when the missile hits a wall        
        def hitWall(self, collideWall):
            if collideWall.destroyable:
                #if the wall is destoryable -> run the hit method on the wall
                collideWall.hit(self.missilePower)
            if self.wallExplosion:
                #if an explosion should be created
                if self.missilePower > 3:
                    #if the missile power > 3 -> big explosion
                    explosionGroup.add(Explosion(self, "Tank", self))
                else:
                    #else - small explosion
                    explosionGroup.add(Explosion(self, "Missile", self))
            #destory the missile object
            self.kill()
        
        #update the status of the missile
        def update(self):
            #create a group of missiles without the current one
            tempMissileGroup = missileGroup.copy()
            tempMissileGroup.remove(self)
            #check for collision with other missiles with double missile size (collision ratio)
            colObjList = pygame.sprite.spritecollide(self, tempMissileGroup, True, pygame.sprite.collide_rect_ratio(2))
            if colObjList:
                #if there is a collision
                for colObj in colObjList:
                    #destory the object
                    colObj.kill()
                    #create an explosion
                    explosionGroup.add(Explosion(colObj, "Missile", self))
                    #destory self
                    self.kill()
                    
            #check for collision with tanks
            tankColList = pygame.sprite.spritecollide(self, tankGroup, False)
            if tankColList:
                #if there is a collision
                for colTank in tankColList:
                    #for every tank the missile has collided with
                    if colTank != self.tank:
                        #the the tank is not itself, add one to the tank's hit shot counter
                        self.tank.hitShot += 1 
                        
                    #run collide function on the tank 
                    colTank.collide(self, self.missilePower)
                    #destory self
                    self.kill()
                
            #check for collision with walls
            collideWallList = pygame.sprite.spritecollide(self, wallGroup, False)            
            if collideWallList:
                #if it hit a wall
                for collideWall in collideWallList:
                    #run hitWall function for every wall it hit
                    self.hitWall(collideWall)     
            else:
                #else - run move function
                self.move(self.missileRate)
                
        #move the missile        
        def move(self, moveValue):
            #set default move values
            self.deltaX = 0
            self.deltaY = 0
            #set move values according to which directoin it is facing
            if self.face == "U":
                self.deltaY = -moveValue
            elif self.face == "D":
                self.deltaY = moveValue
            elif self.face == "R":
                self.deltaX = moveValue
            elif self.face == "L":
                self.deltaX = -moveValue
            #update the rect of the missile
            self.rect.x += self.deltaX
            self.rect.y += self.deltaY
            #update the image of the missile
            self.image = images["missile"+self.face] 
    
    #class for power ups
    class powerUp(pygame.sprite.Sprite):
        #initialization method
        def __init__(self, x, y, type):
            pygame.sprite.Sprite.__init__(self)
            #set type of power up
            self.type = type
            #set whether or not it has been claimed
            self.claim = False
            #set the amount of time it will be displayed
            self.displayTime = 20*fpsRate
            #set x and y coordinate
            self.x = x
            #run y cord through getYCord function (adds the status bar height into the y cord)
            self.y = getYCord(y)
            #set the image and rect for the image
            self.imageName = "pu"+self.type[0].capitalize()+self.type[1:]
            self.image = images[self.imageName]           
            self.rect = self.image.get_rect()
            self.rect.topleft = (self.x,self.y)
        
        #update the power up
        def update(self):
            #check for collision with tank
            collideTankList = pygame.sprite.spritecollide(self, tankGroup, False)
            #update the display time left
            self.displayTime -= 1

            if self.displayTime <= 0:
                #check if display time timed out -> destory the power up
                self.kill()
            else:
                #else - the power up still has time left
                if collideTankList:
                    #if collided with tank
                    #play sound
                    sounds["powerUp"].play()
                    #destory self
                    self.kill()
                    for collideTank in collideTankList:
                        #for every tank it collided with -> give the tank the power up
                        collideTank.powerUpStatus[self.type] = True
                        collideTank.powerUpCount += 1                  
    
    #class for walls
    class Wall(pygame.sprite.Sprite):
        #initialization method
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            #set the image
            self.image = images["wall"]
            #set the health for the wall
            self.destroyable = True
            self.destroyLimit = 3
            self.destroyCount = self.destroyLimit
            #set position of the wall
            self.rect = self.image.get_rect()
            self.rect.x = x
            #run y cord through getYCord function (adds the status bar height into the y cord)
            self.rect.y = getYCord(y)
        
        #if the wall has been hit
        def hit(self, missilePower):
            #update the destoryCount with the power of the missile it was hit by
            self.destroyCount -= missilePower
            if self.destroyCount < 0:
                #if the health left is less than 0 -> destory self
                self.kill()
            else:  
                #else -> update the image (more cracks in the wall)
                self.image = images["wallCracked"+str(self.destroyLimit-self.destroyCount)]
    
    #class for boundary walls
    class boundWall(pygame.sprite.Sprite):
        #initialization method
        def __init__(self, x, y, side):
            pygame.sprite.Sprite.__init__(self)
            #the wall is not destoryable
            self.destroyable = False
            #set image and rect
            self.image = images["bWall"+side]
            self.rect = self.image.get_rect()
            self.rect.x = x
            #run y cord through getYCord function (adds the status bar height into the y cord)
            self.rect.y = getYCord(y)
    
    #class for each player info bar
    class playerInfo(pygame.sprite.Sprite):
        #initialization method
        def __init__(self, tank, playerNum, totalPlayer, height, yPos):
            #set spacing between each player info image
            self.spacing = 10
            #set width for all player info bars
            self.barWidth = size[0]-50
            self.playerNum = playerNum
            self.yPos = yPos
            self.tank = tank
            #set width of the tank image
            self.playerImageWidth = images["tank"+str(self.playerNum)].get_width()
            pygame.sprite.Sprite.__init__(self)
            
            #set the amount of leftover space (after dividing the total width by 3)
            self.leftover = self.barWidth - (self.barWidth//totalPlayer)*totalPlayer
            
            if playerNum < totalPlayer:
                #this slot is not for the last player -> create a surface with width of total width/3
                self.image = pygame.Surface((self.barWidth//totalPlayer, height))
            if playerNum ==  totalPlayer:
                #this slot is for the last player -> create a surface with width of total width/3 + leftover
                self.image = pygame.Surface((self.barWidth//totalPlayer+self.leftover, height))
            
            #set rect for image
            self.rect = self.image.get_rect()
            
            #set position and colour of player info bar depending on player number
            if self.playerNum == 1:
                #first player
                self.image.fill(colours["blue"])
                #left most position
                self.rect.topleft = (0, yPos)
            if self.playerNum == 2:
                #second player
                self.image.fill(colours["green"])
                #position changes depending on number of players
                if totalPlayer == 2:
                    self.rect.topright = ((self.barWidth, yPos))
                if totalPlayer >= 3:
                    self.rect.topleft = ((self.barWidth//totalPlayer, yPos))
            if self.playerNum == 3:
                #third player
                self.image.fill(colours["pink"])
                #position changes depending on number of players
                if totalPlayer == 3:
                    self.rect.topright = ((self.barWidth, yPos))
                if totalPlayer >= 4:
                    self.rect.topleft = ((self.barWidth//totalPlayer*2, yPos))
            if self.playerNum == 4:
                #fourth player
                self.image.fill(colours["orange"])
                #right most position
                self.rect.topright = ((self.barWidth, yPos))
            
            #add ammo bar
            self.infoAmmoBar = ammoBar(self.tank, playerNum, self)
            #add life bar
            self.infoLifeBar = lifeBar(self.tank, playerNum, self)
            #get coordinate for player image
            self.imageCord = (self.infoAmmoBar.rect.right + (self.infoLifeBar.rect.left - self.infoAmmoBar.rect.right)//2, self.rect.centery)
            #add player image
            self.infoImage = playerImage(self.tank, self.imageCord, self)
            #add sprites to group
            playerInfoImageGroup.add(self.infoImage)            
            playerInfoImageGroup.add(self.infoAmmoBar)
            playerInfoImageGroup.add(self.infoLifeBar)
    
    #class for player image in the player info bar
    class playerImage(pygame.sprite.Sprite):
        #initialization method
        def __init__(self, tank, cord, playerInfoObj):
            pygame.sprite.Sprite.__init__(self)
            self.tank = tank
            self.tankNum = self.tank.tankNum
            #set the player info object it will be blitted on
            self.playerInfoObj = playerInfoObj
            #set image as image of the corresponding tank
            self.image = images["tank"+str(self.tankNum)]
            #position the image
            self.rect = self.image.get_rect()
            self.rect.center = cord
        
        #update the image
        def update(self):
            if self.tank.dead:
                #if tank is dead --> center the image within the slot
                self.rect.center = self.playerInfoObj.rect.center
    
    #class for the ammo bar
    class ammoBar(pygame.sprite.Sprite):
        #initialization method
        def __init__(self, tank, playerNum, playerInfoObj):
            #width of each ammo image
            self.width = 25
            pygame.sprite.Sprite.__init__(self)
            self.tank = tank
            #set the player info object it will be blitted on
            self.playerInfoObj = playerInfoObj
            self.ammoLeft = self.tank.missileLeft
            if testMode:
                #FOR TESTING
                self.ammoLeft = 0
            #set the image to display (subsurface depending on amount of ammo left)
            self.image = images["ammo"].subsurface((0, 0, (self.width*self.ammoLeft), (images["ammo"].get_height())))
            #get rect and position it
            self.rect = self.image.get_rect()
            self.rect.midleft = (self.playerInfoObj.rect.midleft[0]+self.playerInfoObj.spacing, self.playerInfoObj.rect.midleft[1])
        
        #update the image
        def update(self):
            if self.tank.lives > 0:
                #there are more than 0 lives left
                self.ammoLeft = self.tank.missileLeft
                if self.ammoLeft >= 0:
                    #if ammo left is equal to or greater than 0
                    if testMode:
                        #FOR TESTING
                        self.ammoLeft = 0
                    if self.tank.missilePower > 3:
                        #if the stronger ammo power up is being used
                        self.baseImage = images["ammoPower"]
                    else:
                        #else - normal ammo
                        self.baseImage = images["ammo"]
                        
                    #set subsurface to display
                    self.image = self.baseImage.subsurface((0, 0, (self.width*self.ammoLeft), (self.baseImage.get_height())))
                else:
                    #if ammo left is less than 0 - infinite ammo power up --> display infinite ammo image
                    self.image = images["puAmmoImage"]
                    
                #update rect and reposition
                self.rect = self.image.get_rect()
                self.rect.midleft = (self.playerInfoObj.rect.midleft[0]+self.playerInfoObj.spacing, self.playerInfoObj.rect.midleft[1])
            else:
                #else - 0 lives left (tank is dead)
                if self.tank.ghost:
                    #if ghost mode enables --> show ghost image
                    self.image = images["ghost"]
                else:
                    #else - normal mode --> show skull image
                    self.image = images["skull"]
                    
                #get rect of image and reposition
                self.rect = self.rect = self.image.get_rect()
                self.rect.midright = (self.playerInfoObj.infoImage.rect.left-5, self.playerInfoObj.rect.centery)
    
    #class for the life bar
    class lifeBar(pygame.sprite.Sprite):
        #initialization method
        def __init__(self, tank, playerNum, playerInfoObj):
            #width of each heart image
            self.width = 30
            #set the player info object it will be blitted on
            self.playerInfoObj = playerInfoObj
            pygame.sprite.Sprite.__init__(self)
            self.tank = tank
            self.lifeLeft = self.tank.lives
            #set image (subsurface depending on the amount of life left)
            self.image = images["heart"].subsurface((0, 0, (self.width*self.lifeLeft), (images["heart"].get_height())))
            #get rect and position the rect
            self.rect = self.image.get_rect()
            self.rect.midright = (self.playerInfoObj.rect.midright[0]-self.playerInfoObj.spacing, self.playerInfoObj.rect.midright[1])
        
        #update the image
        def update(self):
            self.lifeLeft = self.tank.lives
            #set the image (subsurface depending on the amount of life left)
            self.image = images["heart"].subsurface((0, 0, (self.width*self.lifeLeft), (images["heart"].get_height())))
            
            if self.lifeLeft <= 0:
                #if lives are less than 0 (tank is dead)
                if self.tank.ghost:
                    #ghost mode --> show ghost image
                    self.image = images["ghost"]
                else:
                    #normal mode --> show skull image
                    self.image = images["skull"]
                #get rect of image and reposition
                self.rect = self.rect = self.image.get_rect()
                self.rect.midleft = (self.playerInfoObj.infoImage.rect.right+5, self.playerInfoObj.rect.centery)
    
    #class for the settings bar
    class settingsBar(pygame.sprite.Sprite):
        #initialization method
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            #font
            self.myfont = pygame.font.Font(fonts["bops1"], 150)
            #render text using font
            self.pauseText = self.myfont.render("PAUSED", True, colours["light grey"])
            #get rect of text and center it
            self.pauseTextRect = self.pauseText.get_rect()
            self.pauseTextRect.center = screen.get_rect().center
            #set the image (subsurface of the dark background)
            self.image = images["settingsBG"].subsurface(0,0,50,50)
            #get rect of the image and position it
            self.rect = self.image.get_rect()
            self.rect.topright = (size[0],0)
            #add pause button to the settings bar
            self.pauseButton = pauseButton(self)
            #add pause button to settings bar icon sprite group
            settingsIconGroup.add(self.pauseButton)
        
        #pause the game
        def pause(self):
            #play paused music
            if musicOn:
                pygame.mixer.music.load(resourcePath + "pause.mp3")
                pygame.mixer.music.play(-1)
            #set background (darker screen)
            self.pauseBG = self.image
            self.pauseBGrect = self.rect
            #set the background image 
            self.image = pygame.transform.scale(images["GObg"], size)
            #blit the pause background onto the image
            self.image.blit(self.pauseBG, self.pauseBGrect)
            #blit the pause text onto the image
            self.image.blit(self.pauseText, self.pauseTextRect)
            #get rect for image and center it
            self.rect = self.image.get_rect()
            self.rect.center = screen.get_rect().center
            #clear tank movement list (which controls have been pressed)
            for tankNum in tankDict:
                tankDict[tankNum].moveList = []
                tankMove[tankNum]["x"] = 0
                tankMove[tankNum]["y"] = 0
        
        #unpause the game
        def unpause(self):
            #play normal music
            if musicOn:
                pygame.mixer.music.load(resourcePath + bgMusicName)
                pygame.mixer.music.play(-1)
            #reset the image and rect to normal values
            self.image = images["settingsBG"].subsurface(0,0,50,50)
            self.rect = self.image.get_rect()
            self.rect.topright = (size[0],0)           
    
    #class for the pause button    
    class pauseButton(pygame.sprite.Sprite):
    
        #class for the quit and restart buttons
        class pauseScreenButton(pygame.sprite.Sprite):
            #initialization method
            def __init__(self, type, loc):
                pygame.sprite.Sprite.__init__(self)
                #set type of button
                self.type = type
                #set location reference for button
                self.loc = loc
                #set images (selected and unselected)
                self.selImage = images[self.type+"ButSel"]
                self.unSelImage = images[self.type+"But"]
                #set image to unselected (default)
                self.image = self.unSelImage
                #get rect and position rect
                self.rect = self.image.get_rect()
                if self.type == "mainMenu" or self.type == "quit":
                    #if it is the main menu or quit button --> left side of location reference
                    self.rect.midtop = (self.loc[0]+100, self.loc[1])
                else:
                    #if it is the restart button --> right side of the location reference
                    self.rect.midtop = (self.loc[0]-100, self.loc[1])
            
            #update the image
            def update(self, mousePos):
                if self.rect.collidepoint(mousePos):
                    #if the mouse is over the rect of the button --> selected image
                    self.image = self.selImage
                else:
                    #else - mouse is not over the rect of the button --> unselected image
                    self.image = self.unSelImage
            
            #if the button is clicked
            def clicked(self):
                if self.type == "mainMenu":
                    #if this is the main menu button
                    pygame.quit()
                    sys.exit()
                if self.type == "quit":
                    #if this is the quit button
                    pygame.quit()
                    sys.exit()
                if self.type == "restart":
                    #if this is the restart button
                    #stop music
                    pygame.mixer.music.stop()
                    pygame.mixer.stop()
                    #reset score
                    #get new controls
                    controlsPlayerDict = userSetup(resourcePath, setupMusicName)
                    numPlayer = len(controlsPlayerDict)
                    #set up score tracker
                    score = {}
                    for player in range(1, numPlayer+1):
                        score[player] = 0
                    #start new game
                    startGame(resourcePath, mapNum, numPlayer, bgMusicName, score, returnMainMenu, controlsPlayerDict)   
                    
        #initialization method
        def __init__(self, setBar):
            pygame.sprite.Sprite.__init__(self)
            self.setBar = setBar
            #set the image of the pause button (default is faded)
            self.image = images["pauseFade"]
            #get rect of the image and position it
            self.rect = self.image.get_rect()
            self.rect.topright = (size[0]-5, 5)
            self.paused = False
        
        #update the image
        def update(self, mousePos, mouseDownPos):
            if self.rect.collidepoint(mousePos):
                #if collide with mouse - (full image)
                self.image = images["pauseFull"]
            else:
                #else - (faded image)
                self.image = images["pauseFade"]
            if mouseDownPos != None and self.rect.collidepoint(mouseDownPos):
                #if mouse down position is given and it collides with the button (button is clicked)
                self.pause()
        
        #if pause button is clicked
        def pause(self):
            self.paused = True
            #pause game settings bar 
            self.setBar.pause()
            #set image to full image (no longer faded)
            self.image = images["playFull"]  
            #create a quit/main menu button
            if returnMainMenu:
                quitGameButton = self.pauseScreenButton("mainMenu", (size[0]//2, size[1]-150))
            else:
                quitGameButton = self.pauseScreenButton("quit", (size[0]//2, size[1]-150))
            #create a restart button
            restartButton = self.pauseScreenButton("restart", (size[0]//2, size[1]-150))
            
            #loop for paused screen
            while self.paused:
                #set fps rate
                clock.tick(fpsRate)
                
                for ev in pygame.event.get():
                    if ev.type == pygame.QUIT:
                        #close button clicked
                        pygame.quit()
                        sys.exit()
                    if ev.type == pygame.KEYDOWN:
                        #button pressed
                        if ev.key == K_ESCAPE:
                            #escape key --> unpause
                            self.paused = False
                            self.setBar.unpause() 
                    if ev.type == pygame.MOUSEBUTTONDOWN:
                        #mouse button clicked
                        if ev.button == 1:
                            #mouse button 1
                            if self.rect.collidepoint(ev.pos):
                                #if button collides with the pos of the mouse click --> button clicked
                                self.paused = False
                                #unpause the settings bar
                                self.setBar.unpause()   
                            else:
                                #check if collided with buttons
                                if quitGameButton.rect.collidepoint(ev.pos):
                                    #collide with quit/main menu button
                                    quitGameButton.clicked()
                                if restartButton.rect.collidepoint(ev.pos):
                                    #collide with restart button
                                    restartButton.clicked()
                
                #update colour of the button
                mousePos = pygame.mouse.get_pos()
                quitGameButton.update(mousePos)
                restartButton.update(mousePos)
                
                #cover up old screen
                screen.fill((0,0,0))
                #blit the frozen game screen onto the screen
                screen.blit(gameScreen, (0,0))              
                #draw the settings sprite group objects onto the screen
                settingsGroup.draw(screen)
                #draw the settings icon sprite groups onto the screen
                settingsIconGroup.draw(screen)
                #blit the buttons onto the screen
                screen.blit(quitGameButton.image, quitGameButton.rect)
                screen.blit(restartButton.image, restartButton.rect)
                #update the display
                pygame.display.update()
                             
    #set up height of the status bar 
    global statusBarHeight
    statusBarHeight = 50  
    
    #Create groups for sprites
    allSprites = pygame.sprite.Group()
    playerInfoGroup = pygame.sprite.Group()
    playerInfoImageGroup = pygame.sprite.Group()
    missileGroup = pygame.sprite.Group()
    explosionGroup = pygame.sprite.Group()
    wallGroup = pygame.sprite.Group()
    nonDestroyWallGroup = pygame.sprite.Group()
    tankGroup = pygame.sprite.Group()
    powerUpGroup = pygame.sprite.Group()
    settingsGroup = pygame.sprite.Group()
    settingsIconGroup = pygame.sprite.Group()
    
    #add sprites to allSprites group
    allSprites.add(playerInfoGroup)
    allSprites.add(playerInfoGroup)
    allSprites.add(missileGroup)
    allSprites.add(explosionGroup)
    allSprites.add(wallGroup)
    allSprites.add(tankGroup)
    allSprites.add(powerUpGroup)
    allSprites.add(settingsGroup)
    allSprites.add(settingsIconGroup)
    
    #set up list to store all possible tank positions
    tankPosList = []
    
    #Power up settings
    powerUpOn = True
    #dictionary to store the chance of each power up spawning
    powerUpDict = {"ammoInfin":1, "speed":1, "doubleLife":1, "ammoPower":1}
    powerUpList = []
    for powerUpChance in powerUpDict:
        #for every power up in the power up dict, add it to the power up list the number of time
        #specified in the value that power up corresponds to in the powerUpDict
        powerUpList.extend([powerUpChance]*powerUpDict[powerUpChance])
    
    #set up power up spawn frequency
    powerUpFreq = (20//numPlayer,40//numPlayer)
    #choose the time when the next power up will spawn
    nextPowerUp = random.randint(powerUpFreq[0]*fpsRate, powerUpFreq[1]*fpsRate)
    #set up list to store all possible locations where power up can spawn
    powerUpLocList = []
    
    #set up settings bar and pause Button
    sBar = settingsBar()
    settingsGroup.add(sBar)
    
    #convert coordinate to coordinates for playing field (taking into account the height of the
    #player status bars)
    def getYCord(y):
        global statusBarHeight
        #add the statusBarHeight to the y cord value
        y += statusBarHeight
        return y
    
    #set up boundary walls (around the edge of the playing screen)
    #for each column
    for bWallCol in range((size[0]//25)+1):
        #add wall to top of screen
        wallGroup.add(boundWall(bWallCol*25, 0, "U"))
        #add wall to bottom of screen
        wallGroup.add(boundWall(bWallCol*25, size[1]-12-statusBarHeight, "D"))
    #for each row
    for bWallRow in range((size[1]//25)+1):
        #add wall to left side
        wallGroup.add(boundWall(0, bWallRow*25, "L"))
        #add wall to right side
        wallGroup.add(boundWall(size[0]-12, bWallRow*25,  "R"))
    
    #analyze the map data
    #for each row
    for rowNum, row in enumerate(maps[mapNum][:size[1]//25-4]):
        #for each column
        for colNum, col in enumerate(row[:size[0]//25-4]):
            if col == "W":
                #add wall with that coordinate
                wallGroup.add(Wall((colNum+1)*25, (rowNum+1)*25))
            if col == "T":
                #possible tank position
                tankPosList.append(((colNum+1)*25, (rowNum+1)*25))     
            if col == "." or  col == "O":
                #else - possible power up position (empty space)
                powerUpLocList.append(((colNum+1)*25, (rowNum+1)*25))
   
    #set up tanks & set up player info bar for each tank
    #dictionary containing all tanks
    tankDict = {}
    #dictoinary containing the move values for all tanks
    tankMove = {}
    #list of possible directions to face
    faceList = ["R","D","L","U"]   
    #get max ammo and health
    playerInfoWidth = (size[0]-50)//numPlayer-80
    #set max ammo according to the with of the screen (larger screen can fit more ammo in status bar)
    maxAmmo = min((playerInfoWidth//3)//25, 6)
    #set max life according to the with of the screen (larger screen can fit more hearts in status bar)
    maxLife = min((2*(playerInfoWidth//3))//30, 10)
    #set default settings for tanks 
    settings = (maxAmmo, maxLife)
    
    #create a list to store the control sets being used
    controlNumList = []
    
    #for each tank number in the number of players
    for tankNum in range(1, numPlayer+1):
        #for each control set in the list of selected control sets
        for testControlNum in controlsPlayerDict:
            if controlsPlayerDict[testControlNum] == tankNum:
                #if the tank nubmer for the control set being checked matches the current tank number
                #assign that control set to the tank
                tankControlNum = testControlNum
        #spawn position of tank is a random choice in the list of possible spawn locations
        tankPos = random.choice(tankPosList)
        #remove the used location from the list
        tankPosList.remove(tankPos)
        #create the tank object and add it to the tankDict
        tankDict[tankNum] = Tank(tankPos[0], tankPos[1], tankNum, numPlayer, powerUpList, settings, tankControlNum)
        #create an entry in the tankMove dictionary to store its x, y, and face values
        tankMove[tankNum] = {"x":0, "y":0, "face":"R"}
        #add the tank to the tankGroup sprite group
        tankGroup.add(tankDict[tankNum])
        #create a player info bar for that tank
        playerInfoGroup.add(playerInfo(tankDict[tankNum], tankNum, numPlayer, statusBarHeight, 0))
        #add the tank's control set to the list of control sets being used
        controlNumList.append(tankControlNum)
    
    #set the select key
    selectKey = K_SPACE
    
    #set the amount of time before ending game after last tank standing (seconds)
    gameEndCountdown = 1*fpsRate
    
    #list to track player standings
    global playerRank
    playerRank = []
    #to track the amount of ticks that have passed since the game began
    global gameTimeCounter
    gameTimeCounter = 0
    
    #run countdown before game starts
    preGameStartRun = True
    
    #actual game loop
    try:
        while keepGoing:
            #clear and refresh Screen
            screen.blit(gameScreen, (0,0))
            pygame.display.update()
        
            #Set up fps rate
            clock.tick(fpsRate)
            #update game counter
            gameTimeCounter += 1
            
            #create tank status list
            global tankStat
            tankStat = []
            
            #set default mouse down position
            mouseDownPos = None
            
            #check for events
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    #close button is pressed
                    keepGoing = False
                elif ev.type == pygame.KEYDOWN:
                    #keyboard key is pressed
                    if ev.key == K_ESCAPE:
                        #escape button --> pause game
                        sBar.pauseButton.pause()
                    for controlSet in controlNumList:
                        #for each control set in the list of used control sets
                            for controlKey in tankControls[controlSet]:
                                #for each key in that control set
                                if ev.key == controlKey:
                                    #if the key matches the key that is being checked
                                    #get the player number for that key
                                    tankNum = controlsPlayerDict[controlSet]
                                    if tankControls[controlSet][controlKey] == "X":
                                        #if the key corresponds to the shoot button
                                        tankDict[controlsPlayerDict[controlSet]].launch()
                                    else:
                                        #if the key corresponds to a move button
                                        #add the key to a list containing every button that has been pressed, but not released
                                        tankDict[tankNum].moveList.append(tankControls[controlSet][controlKey])
                                        #set the move values for the tank (change in x, y, and facing direction)
                                        tankMove[tankNum]["x"] = moveDict[tankDict[tankNum].moveList[-1]][0]
                                        tankMove[tankNum]["y"] = moveDict[tankDict[tankNum].moveList[-1]][1]
                                        tankMove[tankNum]["face"] = tankControls[controlSet][controlKey]
                                        
                elif ev.type == pygame.KEYUP:
                    #keyboard key was released
                    for controlSet in controlNumList:
                        #for each control set in the list of control sets
                        if ev.key in tankControls[controlSet]:
                            #for each key in that control set
                            if tankControls[controlSet][ev.key] != "X":
                                #if the key released is a move key
                                #get the player number for that key
                                tankNum = controlsPlayerDict[controlSet]
                                if tankControls[controlSet][ev.key] in tankDict[tankNum].moveList:
                                    #if the key is in the control set for that player --> remove that key
                                    #from the list of active keys for that player
                                    tankDict[tankNum].moveList.remove(tankControls[controlSet][ev.key])
                                if len(tankDict[tankNum].moveList) > 0:
                                    #if there is still a key left in the the active keys list for that player
                                    #set the move values for the tank (change in x, y, and facing direction
                                    #according to the next key 
                                    tankMove[tankNum]["x"] = moveDict[tankDict[tankNum].moveList[-1]][0]
                                    tankMove[tankNum]["y"] = moveDict[tankDict[tankNum].moveList[-1]][1]
                                    tankMove[tankNum]["face"] = tankDict[tankNum].moveList[-1]
                                else:
                                    #else - no keys left in active key list --> reset tank movement (x, y)
                                    #tank does not move
                                    tankMove[tankNum]["x"] = 0
                                    tankMove[tankNum]["y"] = 0
               
                elif ev.type == pygame.MOUSEBUTTONDOWN:
                    #mouse button was pressed
                    if ev.button == 1:
                        #if button 1 was pressed --> set mouseDownPos to the position of the mouse click
                        mouseDownPos = ev.pos

            if powerUpOn:
                #if power ups are enabled
                if gameTimeCounter >= nextPowerUp:
                    #if it is time for the next power up to spawn
                    #set flag to detect whether the coordinate is open
                    openCord = False
                    while openCord == False:
                        #while an open coordinate has not been found --> test a random coordinate in the list
                        #of possible power up coordinates
                        newCord = random.choice(powerUpLocList)
                        openCord = True
                        for tank in tankDict:
                            #for each tank in the list of active tanks
                            if tankDict[tank].rect.collidepoint(newCord):
                                #if the tank collides with the coordinate being checked --> coordinate is
                                #not open --> openCord = False --> keep checking
                                openCord = False
                                break
                    #type of power up is a random choice from the list of power ups
                    newType = random.choice(powerUpList)
                    #reset the next power up counter (current time + random integer choice between the power up spawn
                    #intervals)
                    nextPowerUp = gameTimeCounter + random.randint(powerUpFreq[0]*fpsRate, powerUpFreq[1]*fpsRate)
                    #add the power up to a group containing all the power ups
                    powerUpGroup.add(powerUp(newCord[0], newCord[1], newType))
                
            #get mouse position
            mousePos = pygame.mouse.get_pos()            
            
            #blit background to game screen    
            gameScreen.fill((100,100,100))
            gameScreen.blit(images["bgImage"], (0,0))
            
            #blit status bar to the game screen
            playerInfoGroup.draw(gameScreen)
            
            #update the status bars and blit them to the game screen
            playerInfoImageGroup.update()
            playerInfoImageGroup.draw(gameScreen)
            
            #blit walls to the game screen
            wallGroup.draw(gameScreen)
            
            #update power ups and blit them to the game screen
            powerUpGroup.update()
            powerUpGroup.draw(gameScreen)
            
            #for each tank in the dictionary containing all active tanks
            for tankNum in tankDict:
                #move the tank according to its move values (x, y, face)
                tankDict[tankNum].move(tankMove[tankNum]["x"], tankMove[tankNum]["y"], tankMove[tankNum]["face"])
            
            #update the tanks and blit them to the game screen
            tankGroup.update()
            tankGroup.draw(gameScreen)
           
            #update the missiles and blit them to the game screen
            missileGroup.update()
            missileGroup.draw(gameScreen)
            
            #update the explosions and blit them to the game screen
            explosionGroup.update()
            explosionGroup.draw(gameScreen)   
            
            #update the settings bar and blit it to the game screen
            settingsGroup.draw(gameScreen)
            settingsIconGroup.update(mousePos, mouseDownPos)
            settingsIconGroup.draw(gameScreen)
            
            #check if countdown has run yet
            if preGameStartRun:
                #run countdown function
                preGameStart(gameScreen)
                #countdown has run --> do not run again
                preGameStartRun = False
                if musicOn:
                    #if music enabled --> start playing background music
                    pygame.mixer.music.load(resourcePath + bgMusicName)
                    pygame.mixer.music.play(-1)
            
            #check if game should continue (if all but one tank has died)
            if tankStat.count(False) <= 1:
                #the number of tanks still alive is equal to or less than 1 (end game)
                #update the game end countdown counter
                gameEndCountdown -= 1
                if gameEndCountdown <= 1:
                    print("GAME OVER")
                    #game end countdown timer has reached 0
                    #stop the music
                    pygame.mixer.music.stop()
                    for tank in tankDict:
                        #for each tank still alive, add it to the rankings
                        tankDict[tank].addToRankings()
                    #run the gameOver function
                    gameOver(playerRank, gameScreen, returnMainMenu, score, controlsPlayerDict)
    finally:
        #exit the game
        pygame.quit()

#security
today = (time.strftime("%Y/%m/%d"))
todayMD5 = hashlib.md5(today.encode()).hexdigest()
while True:
    acsCode = input("Enter the access code: ").strip()
    if acsCode == todayMD5:
        break
    elif acsCode == "":
        password = getpass.getpass("Password: ")
        if hashlib.md5(password.encode()).hexdigest() == "de918f6ea2e9479ed9d81a8147dbae3d":
            break
    print("\nINCORRECT CODE/PASSWORD.\nEnsure you are entering in today's code. It changes each day.\n")

print("----------------------------------------")
print("Tanks Wars - Multiplayer Version")
print("Michael Pu - ICS2O\n")
print("Welcome to Tanks Wars - Multiplayer Version\nThe game should begin in a moment.")
    
#set global variables
global screen
global fonts
global images
global maps
global sounds
global size
global colours
global tankControls
global musicOn
global testMode

#initalize stuff
pygame.init()
pygame.mixer.init()
pygame.display.init()
pygame.font.init()

#for testing and debugging (testMode)
testMode = False
if testMode:
    print("TEST MODE")

#Set up framerate
fpsRate = 60
clock = pygame.time.Clock()

#set up the possible tank Controls
tankControls = {
1:{K_w:"U", K_a:"L", K_d:"R", K_s:"D", K_v:"X"}, 
2:{K_KP5:"U", K_KP1:"L", K_KP3:"R", K_KP2:"D", K_KP_ENTER:"X"},
3:{K_i:"U", K_j:"L", K_l:"R", K_k:"D", K_SLASH :"X"},
4:{K_UP:"U", K_LEFT:"L", K_RIGHT:"R", K_DOWN:"D", K_RETURN:"X"}}
moveDict = {"U":(0,-1), "D":(0,1), "L":(-1,0), "R":(1,0)}

#set up background music
musicOn = True
bgMusicList = {1:"cinema", 2:"battle", 3:"desert", 4:"beach", 5:"underwater", 6:"starship", 7:"athletic", 8:"awesome"}
bgMusicNum = 1
setupMusicNum = 5
loadMusicNum = 6

bgMusicName = bgMusicList[bgMusicNum]+".mp3"
setupMusicName = bgMusicList[setupMusicNum]+".mp3"
loadMusicName = bgMusicList[loadMusicNum]+".mp3"


#curPath = (os.path.dirname(os.path.realpath(__file__)))
#Get Path to Resources Directory 
resourcePath = curPath + "/resources/"

#Load Game Resources
loadGame(resourcePath, loadMusicName)

#Get User to Setup Their Controls 
controlsPlayerDict = userSetup(resourcePath, setupMusicName)

#Set Game Settings
#set the map to use
mapNum = 2
#set the number of players
numPlayer = len(controlsPlayerDict)
#if the game is being run from a menu or being run directly (for testing)
returnMainMenu = False

#set up score tracker
score = {}
for player in range(1, numPlayer+1):
    score[player] = 0
    
#Start the Acutal Game
startGame(resourcePath, mapNum, numPlayer, bgMusicName, score, returnMainMenu, controlsPlayerDict)
