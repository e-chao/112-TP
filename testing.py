import pygame
from cube import Cube
from button import Button
from score import Score
from inputRect import InputRect
import math, random, copy, time
from pygame.locals import *

#Most drawing and display code was learned from https://realpython.com/pygame-a-primer/ 
#and pygame.org

#Initialize pygame and global variables
pygame.init()
pygame.mixer.init()
#Sounds
#Learning sound and music code from 
#https://www.geeksforgeeks.org/python-playing-audio-file-in-pygame/
#clickSound from https://mixkit.co/free-sound-effects/pop/
#buttonSound from https://www.youtube.com/watch?v=h8y0JMVwdmM (from Minecraft)
clickSound = pygame.mixer.Sound("dotClicked.wav")
buttonSound = pygame.mixer.Sound("buttonClick.wav")
#Set display dimensions
screen = pygame.display.set_mode(size = (0,0), flags = pygame.FULLSCREEN)
sWidth, sHeight = screen.get_size()
#Game
gameStarted = False
sens = .3
start = 0
timePast = 0
scores = []
accuracies = []
totalHits = []
targetColor = (255,255,0)
crosshairColor = (255,255,255)
crosshairRadius = 2
#Get buttons
playButton = Button(sWidth/2,sHeight/2,sWidth/4,sHeight/16,(0,0,255))
quitButton = Button(19*sWidth/20, 9*sHeight/10, sWidth/15, sWidth/15,
(255,0,0))
resumeButton = Button(sWidth/13,2*sHeight/5, sWidth/8, sHeight/16, 
(111,111,111))
settingsButton = Button(sWidth/13,sHeight/2, sWidth/8, sHeight/16,
(111,111,111))
helpButton = Button(sWidth/13, 3*sHeight/5, sWidth/8, sHeight/16,
(111,111,111))
homeButton = Button(sWidth/13, 7*sHeight/10, sWidth/8, sHeight/16,
(111,111,111))
replayButton = Button(sWidth/13,3*sHeight/10, sWidth/8, sHeight/16,
(111,111,111))
backButton = Button(sWidth/2, 7*sHeight/10, sWidth/3, sHeight/10,
(111,111,111))
#settings
sensInputButton = Button(sWidth/13,sHeight/5, sWidth/8, sHeight/16,
(90,90,90))
targetRGBInputButton = Button(sWidth/13, 3*sHeight/10, sWidth/8, sHeight/16,
(90,90,90))
crosshairRGBInputButton = Button(sWidth/13, 2*sHeight/5, sWidth/8, sHeight/16,
(90,90,90))
crosshairRadiusInputButton = Button(sWidth/13, sHeight/2, sWidth/8, 
sHeight/16, (90,90,90))
#Text from https://stackoverflow.com/questions/20842801/how-to-display-text-in-pygame
pygame.font.init()
buttonFontSize = (sWidth*80)//1920
titleFontSize = (sWidth*100)//1920
smallFontSize = (sWidth*30)//1920
font = pygame.font.SysFont('Arial bold', buttonFontSize)
titleFont = pygame.font.SysFont('Arial bold', titleFontSize)
smallFont = pygame.font.SysFont('Arial bold', smallFontSize)
playText = font.render('Play', False, (0,0,0))
playTextRect = playText.get_rect(center=(playButton.cx,playButton.cy))
quitText = font.render('Quit', False, (0,0,0))
quitTextRect = quitText.get_rect(center=(quitButton.cx,quitButton.cy))
resumeText = font.render('Resume', False, (0,0,0))
resumeTextRect = resumeText.get_rect(center=(resumeButton.cx,
resumeButton.cy))
replayText = font.render('Replay', False, (0,0,0))
replayTextRect = replayText.get_rect(center=(replayButton.cx, replayButton.cy))
settingsText = font.render('Settings', False, (0,0,0))
settingsTextRect = settingsText.get_rect(center=(settingsButton.cx,
settingsButton.cy))
helpText = font.render('Help', False, (0,0,0))
helpTextRect = helpText.get_rect(center=(helpButton.cx,helpButton.cy))
homeText = font.render('Home', False, (0,0,0))
homeTextRect = homeText.get_rect(center=(homeButton.cx,homeButton.cy))
welcomeText = titleFont.render('Welcome to AimPy, AIMLABS at home!', False,
(0,0,0))
welcomeTextRect = welcomeText.get_rect(center=(sWidth/2,sHeight/20))
#Catchphrases
catchphrases = ['We have the meats!', 'You will love this!',
    'Did you watch the dev hour for this?', 'Haha dev hour deez nuts',
    'you will not believe your eyes', 'I heckin love TenZ', 
    'Technoblade neva dies!','The greatest thing since sliced bread',
    'hop on fortnite!','u gotta be trolling']
#Clock
clock = pygame.time.Clock()

def main(sens, targetColor, crosshairColor, crosshairRadius):
    #Main game loop
    running = True
    pygame.event.set_grab(False)
    pygame.mouse.set_visible(True)
    #Music
    #mcMusic from https://www.youtube.com/watch?v=_3ngiSxVCBs
    #fortnite og music from https://www.youtube.com/watch?v=IpPdbU1cjVE
    #valorant og music from https://www.youtube.com/watch?v=rhQ7RTXrc6s
    #ALL MUSIC CREDIT ALSO GOES TO THE ORIGINAL GAME (MINECRAFT, FORTNITE, VALORANT)
    musicChoice = random.randint(0,2)
    if musicChoice == 0:
        pygame.mixer.music.load("sweden.wav")
        pygame.mixer.music.set_volume(1.2)
    elif musicChoice == 1:
        pygame.mixer.music.load("fortnite og.wav")
        pygame.mixer.music.set_volume(.3)
    else:
        pygame.mixer.music.load("valorant og.wav")
        pygame.mixer.music.set_volume(.3)
    pygame.mixer.music.play(-1)
    catchphrase = random.choice(catchphrases)
    while running:
        catchphraseText = font.render(catchphrase, False, (0,0,0))
        cpRect = catchphraseText.get_rect(center=(sWidth/2, sHeight/6))
        screen.fill((100,255,255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                running = False
            elif event.type == pygame.KEYDOWN:
                #opens escape menu
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.stop()
                    escape(sens, targetColor, crosshairColor, crosshairRadius)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                #changes to game menu
                if playButton.pressed():
                    pygame.mixer.music.stop()
                    buttonSound.play()
                    sixshot(sens, targetColor, crosshairColor, crosshairRadius)
                #quits the game
                elif quitButton.pressed():
                    pygame.mixer.music.stop()
                    buttonSound.play()
                    running = False
        screen.blit(catchphraseText, cpRect)
        screen.blit(quitButton.rect, (quitButton.left, quitButton.top))
        screen.blit(playButton.rect, (playButton.left, playButton.top))
        screen.blit(welcomeText, welcomeTextRect)
        screen.blit(playText, playTextRect)
        screen.blit(quitText, quitTextRect)
        clock.tick(240)
        pygame.display.flip()
    pygame.quit()

#Escape menu
#Switching screens learned from 
#https://www.youtube.com/watch?v=0RryiSjpJn0&list=WL&index=1
def escape(sens, targetColor, crosshairColor, crosshairRadius):
    running = True
    pygame.event.set_grab(False)
    pygame.mouse.set_visible(True)
    while running:
        screen.fill((90,90,90))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if quitButton.pressed():
                        buttonSound.play()
                        pygame.quit()
                    elif settingsButton.pressed():
                        buttonSound.play()
                        settings(sens, targetColor, crosshairColor, 
                        crosshairRadius)
                    elif homeButton.pressed():
                        buttonSound.play()
                        main(sens, targetColor, crosshairColor, crosshairRadius)
                    elif helpButton.pressed():
                        buttonSound.play()
                        helpMenu(sens, targetColor, crosshairColor, 
                        crosshairRadius)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main(sens, targetColor, crosshairColor, crosshairRadius)
        #Buttons
        screen.blit(quitButton.rect, (quitButton.left, 
        quitButton.top))
        screen.blit(settingsButton.rect, (settingsButton.left, 
        settingsButton.top))
        screen.blit(helpButton.rect, (helpButton.left, helpButton.top))
        screen.blit(homeButton.rect, (homeButton.left, homeButton.top))
        #Text
        screen.blit(quitText, quitTextRect)
        screen.blit(settingsText, settingsTextRect)
        screen.blit(helpText, helpTextRect)
        screen.blit(homeText, homeTextRect)
        pygame.display.flip()

#This is only for when the game is being played
def pause(sens, targetColor, crosshairColor, crosshairRadius):
    startTime = time.time()
    running = True
    pygame.event.set_grab(False)
    pygame.mouse.set_visible(True)
    while running:
        screen.fill((90,90,90))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if quitButton.pressed():
                        buttonSound.play()
                        pygame.quit()
                    elif homeButton.pressed():
                        buttonSound.play()
                        main(sens, targetColor, crosshairColor, crosshairRadius)
                    elif resumeButton.pressed():
                        buttonSound.play()
                        pygame.event.set_grab(True)
                        pygame.mouse.set_visible(False)
                        running = False
                    elif helpButton.pressed():
                        buttonSound.play()
                        pause_helpMenu(sens, targetColor, crosshairColor, 
                        crosshairRadius)
                    elif replayButton.pressed():
                        buttonSound.play()
                        sixshot(sens, targetColor, crosshairColor, 
                        crosshairRadius)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        #Buttons
        screen.blit(quitButton.rect, (quitButton.left, 
        quitButton.top))
        screen.blit(helpButton.rect, (helpButton.left, helpButton.top))
        screen.blit(homeButton.rect, (homeButton.left, homeButton.top))
        screen.blit(replayButton.rect, (replayButton.left, replayButton.top))
        screen.blit(resumeButton.rect, (resumeButton.left,resumeButton.top))
        #Text
        screen.blit(quitText, quitTextRect)
        screen.blit(helpText, helpTextRect)
        screen.blit(homeText, homeTextRect)
        screen.blit(replayText, replayTextRect)
        screen.blit(resumeText, resumeTextRect)
        pygame.display.flip()
    endTime = time.time()
    return endTime-startTime
    
def settings(sens, targetColor, crosshairColor, crosshairRadius):
    running = True
    pygame.event.set_grab(False)
    pygame.mouse.set_visible(True)
    #text box input code from 
    #https://www.geeksforgeeks.org/how-to-create-a-text-input-box-with-pygame/
    sensText = smallFont.render('Modify Sensitivity',False,(0,0,0))
    sensTextRect = sensText.get_rect(center=(sensInputButton.cx,
    sensInputButton.cy))
    targetRGBText = smallFont.render('Modify Target Color',False,(0,0,0))
    targetRGBRect = targetRGBText.get_rect(center=(targetRGBInputButton.cx,
    targetRGBInputButton.cy))
    crosshairRGBText = smallFont.render('Modify Crosshair Color',False,(0,0,0))
    crosshairRGBRect = crosshairRGBText.get_rect(center=
    (crosshairRGBInputButton.cx,crosshairRGBInputButton.cy))
    crosshairRadiusText = smallFont.render('Modify Crosshair Radius',
    False,(0,0,0))
    crosshairRadiusRect = crosshairRadiusText.get_rect(center=(
    crosshairRadiusInputButton.cx,crosshairRadiusInputButton.cy
    ))
    sensInput = InputRect(sWidth/8,2*sHeight/5,sWidth/10,sHeight/16,
    sensInputButton, sensText, sensTextRect)
    targetRGBInput = InputRect(sWidth/8,sHeight/2,sWidth/10,sHeight/16, 
    targetRGBInputButton, targetRGBText, targetRGBRect)
    crosshairRGBInput = InputRect(sWidth/8,3*sHeight/5,sWidth/10,sHeight/16,
    crosshairRGBInputButton, crosshairRGBText, crosshairRGBRect)
    crosshairRadiusInput = InputRect(sWidth/8,7*sHeight/10,sWidth/10,sHeight/16,
    crosshairRadiusInputButton, crosshairRadiusText, crosshairRadiusRect)
    inputsList = [sensInput,targetRGBInput,crosshairRGBInput,
    crosshairRadiusInput]
    while running:
        currentSens = smallFont.render(f'Current Sensitivity: {sens}',False,
        (0,0,0))
        currentSensRect = currentSens.get_rect(center=(
        sensInputButton.cx+sWidth/2,
        sensInputButton.cy))
        currentTargC = smallFont.render(f'Current Target Color: {targetColor}',
        False,(0,0,0))
        currentTargCRect = currentTargC.get_rect(center=(
        targetRGBInputButton.cx+sWidth/2, targetRGBInputButton.cy))
        currentCrossColor = smallFont.render(
        f'Current Crosshair Color: {crosshairColor}',False,(0,0,0))
        currentCrossColorRect = currentCrossColor.get_rect(center=(
        crosshairRGBInputButton.cx+sWidth/2, crosshairRGBInputButton.cy))
        currentCrossRadius = smallFont.render(
        f'Current Crosshair Radius: {crosshairRadius}',False,(0,0,0))
        currentCrossRadiusRect = currentCrossRadius.get_rect(center=(
        crosshairRadiusInputButton.cx+sWidth/2,crosshairRadiusInputButton.cy))
        screen.fill((200,200,200))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    changed = False
                    for inputRect in inputsList:
                        if inputRect.activity == True:
                            inputRect.changeActivity()
                            changed = True
                            break
                    if not changed:
                        buttonSound.play()
                        escape(sens, targetColor, crosshairColor, 
                        crosshairRadius)
                elif event.key == pygame.K_BACKSPACE:
                    for inputRect in inputsList:
                        if inputRect.activity:
                            inputRect.backspace()
                elif event.key == pygame.K_KP_ENTER:
                    for inputRect in inputsList:
                        if inputRect.activity:
                            inputRect.changeActivity()
                else:
                    for inputRect in inputsList:
                        if inputRect.activity:
                            inputRect.input += event.unicode
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if sensInputButton.pressed():
                        sensInput.changeActivity()
                    elif targetRGBInputButton.pressed():
                        targetRGBInput.changeActivity()
                    elif crosshairRGBInputButton.pressed():
                        crosshairRGBInput.changeActivity()
                    elif crosshairRadiusInputButton.pressed():
                        crosshairRadiusInput.changeActivity()
                    elif homeButton.pressed():
                        buttonSound.play()
                        main(sens, targetColor, crosshairColor, crosshairRadius)
                    elif quitButton.pressed():
                        pygame.quit()
                    else:
                        #make sure all inputs are inactive
                        for inputRect in inputsList:
                            if inputRect.activity:
                                inputRect.changeActivity()
        for inputRect in inputsList:
            #check inactives to prevent errors
            if inputRect.activity == False:
                if len(inputRect.input) > 0:
                    if inputRect == sensInput:
                        temp = inputRect.input.replace('.','')
                        if temp.isdigit():
                            if isinstance(float(inputRect.input), 
                            float):
                                sens = inputRect.input
                                inputRect.clearInput()
                            else:
                                inputRect.clearInput()
                    elif (inputRect == targetRGBInput or inputRect == 
                    crosshairRGBInput):
                        ints = inputRect.input.split(',')
                        if len(ints) < 3:
                            inputRect.clearInput()
                        #check if each val is just a number
                        clear = True
                        for val in ints:
                            if val.isdigit() == False:
                                inputRect.clearInput()
                                clear = False
                        if clear:
                            newColor = (int(ints[0]),int(ints[1]),
                            int(ints[2]))
                            #check to see if each value in the tuple
                            #is valid
                            for val in newColor:
                                if val < 0 or val > 255:
                                    inputRect.clearInput()
                                else:
                                    if inputRect == targetRGBInput:
                                        targetColor = newColor
                                    else:
                                        crosshairColor = newColor
                    else:
                        if inputRect.input.isdigit():
                            crosshairRadius = int(inputRect.input)
                            inputRect.clearInput()
                        else:
                            inputRect.clearInput()
        #input rectangles in input instaces
        #activity being kept track in class
        #draw all input rects with (screen, currentColor, input rectangle)
        for rect in inputsList:
            if rect.activity:
                textS = rect.getSurface(smallFont)
                # pygame.draw.rect(screen, activeColor, rect.rect)
                screen.blit(rect.button.rect, (rect.button.left,
                rect.button.top))
                screen.blit(textS, rect.textRect)
            else:
                screen.blit(rect.button.rect, (rect.button.left,
                rect.button.top))
                screen.blit(rect.text, rect.textRect)
        screen.blit(homeButton.rect, (homeButton.left, homeButton.top))
        screen.blit(homeText, homeTextRect)
        screen.blit(quitButton.rect, (quitButton.left, quitButton.top))
        screen.blit(quitText, quitTextRect)
        screen.blit(currentSens, currentSensRect)
        screen.blit(currentTargC, currentTargCRect)
        screen.blit(currentCrossColor, currentCrossColorRect)
        screen.blit(currentCrossRadius, currentCrossRadiusRect)
        clock.tick(60)
        pygame.display.flip()

def helpMenu(sens, targetColor, crosshairColor, crosshairRadius):
    titleText = titleFont.render('Welcome to AimPy, AIMLABS at home!', 
    False, (0,0,0))
    titleTextRect = titleText.get_rect(center=(sWidth/2,sHeight/20))
    playText = font.render('Click play in the main menu to play', 
    False, (0,0,0))
    playTextRect = playText.get_rect(center=(sWidth/2,sHeight/6))
    scoreText = font.render('Click dots quickly and accurately to score high!',
    False, (0,0,0))
    scoreTextRect = scoreText.get_rect(center=(sWidth/2,sHeight/2))
    backText = font.render('Back', False, (0,0,0))
    backTextRect = backText.get_rect(center=(backButton.cx,backButton.cy))
    running = True
    while running:
        screen.fill((255,255,255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if backButton.pressed():
                    buttonSound.play()
                    running = False
                elif quitButton.pressed():
                    buttonSound.play()
                    pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        screen.blit(quitButton.rect, (quitButton.left, quitButton.top))
        screen.blit(backButton.rect, (backButton.left, backButton.top))
        screen.blit(titleText, titleTextRect)
        screen.blit(quitText, quitTextRect)
        screen.blit(playText, playTextRect)
        screen.blit(scoreText, scoreTextRect)
        screen.blit(backText, backTextRect)
        pygame.display.flip()

def pause_helpMenu(sens, targetColor, crosshairColor, crosshairRadius):
    titleText = titleFont.render('Welcome to AimPy, AIMLABS at home!', 
    False, (0,0,0))
    titleTextRect = titleText.get_rect(center=(sWidth/2,sHeight/20))
    playText = font.render('Click play in the main menu to play', 
    False, (0,0,0))
    playTextRect = playText.get_rect(center=(sWidth/2,sHeight/6))
    scoreText = font.render('Click dots quickly and accurately to score high!',
    False, (0,0,0))
    scoreTextRect = scoreText.get_rect(center=(sWidth/2,sHeight/2))
    backText = font.render('Back', False, (0,0,0))
    backTextRect = backText.get_rect(center=(backButton.cx,backButton.cy))
    running = True
    while running:
        screen.fill((255,255,255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if backButton.pressed():
                    buttonSound.play()
                    running = False
                elif quitButton.pressed():
                    buttonSound.play()
                    pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        screen.blit(quitButton.rect, (quitButton.left, quitButton.top))
        screen.blit(backButton.rect, (backButton.left, backButton.top))
        screen.blit(titleText, titleTextRect)
        screen.blit(quitText, quitTextRect)
        screen.blit(playText, playTextRect)
        screen.blit(scoreText, scoreTextRect)
        screen.blit(backText, backTextRect)
        pygame.display.flip()
        
#Sixshot screen
def sixshot(sens, targetColor, crosshairColor, crosshairRadius):
    running = True
    pygame.mouse.set_pos = (sWidth/2,sHeight/2)
    #Sixshot
    room = Cube(0, 0, 100, 100)
    lookAngleX, lookAngleY = 0, 0
    oldX, oldY = sWidth/2, sHeight/2
    sixshotScore = Score()
    sixshotHits = 0
    sixshotShots = 0
    targetLength = room.length/50
    #time code inspired
    #from https://stackoverflow.com/questions/30720665/countdown-timer-in-pygame
    start = time.time()
    lastTime = start
    timePast = 0
    gameTimePast = 0
    pausedTime = 0
    gameStarted = False
    #list of cube instances
    targets = []
    drawnRoom = copy.deepcopy(room)
    getTargets(targets, drawnRoom, sWidth, sHeight, targetLength)
    #drawn objects are the rotated and actually drawn versions of the
    #original objects
    drawnTargets = copy.deepcopy(targets)
    room2d = convertTo2d(drawnRoom.points)
    #convert the targets to 2d versions of 3d targets, 3d list
    targets2d = []
    for target in drawnTargets:
        target2d = convertTo2d(target.points)
        targets2d.append(target2d)
    while running:
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)
        timePast = time.time() - start
        screen.fill((255,255,255))
        #Game not started yet
        if not gameStarted:
            if timePast >= 3 + pausedTime:
                gameStarted = True
        if timePast >= 63 + pausedTime:
            scores.append(sixshotScore.score)
            if sixshotShots > 0:
                accuracies.append(int((sixshotHits/sixshotShots)*100))
            else:
                accuracies.append(0)
            totalHits.append(sixshotHits)
            gameOver(sens, targetColor, crosshairColor, crosshairRadius)
        room2d = convertTo2d(drawnRoom.points)
        for target in drawnTargets:
            i = drawnTargets.index(target)
            target2d = convertTo2d(target.points)
            targets2d[i] = target2d
        #always checking
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pausedTime += pause(sens, targetColor, crosshairColor, 
                    crosshairRadius)
                if gameStarted:
                    if event.key == pygame.K_a:
                        if drawnRoom.cx < drawnRoom.length/2:
                            for point in drawnRoom.points:
                                point[0] += room.length/100
                            for point in room.points:
                                point[0] += room.length/100
                            room.updateCenter()
                            drawnRoom.updateCenter()
                            for target in drawnTargets:
                                for point in target.points:
                                    point[0] += room.length/100
                                target.updateCenter()
                            for target in targets:
                                for point in target.points:
                                    point[0] += room.length/100
                                target.updateCenter()
                    elif event.key == pygame.K_d:
                        for point in drawnRoom.points:
                            point[0] -= room.length/100
                        for point in room.points:
                            point[0] -= room.length/100
                        room.updateCenter()
                        drawnRoom.updateCenter()
                        for target in drawnTargets:
                            for point in target.points:
                                point[0] -= room.length/100
                            target.updateCenter()
                        for target in targets:
                            for point in target.points:
                                point[0] -= room.length/100
                            target.updateCenter()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if gameStarted:
                    hit = False
                    if event.button == 1:
                        sixshotShots += 1
                        for target in targets:
                            lookX = -target.cz*math.tan(lookAngleY)
                            lookY = target.cz*math.tan(lookAngleX)
                            if targetClicked(lookX, lookY, target, targets, 
                            drawnTargets, drawnRoom, targetLength, sixshotScore,
                            lookAngleX, lookAngleY):
                                sixshotHits += 1
                            else:
                                sixshotScore.resetScoreIncrement()
                #mouse motion as well as locking mouse code from 
                #https://stackoverflow.com/questions/47733992/lock-mouse-in-window-pygame
            elif event.type == pygame.MOUSEMOTION:
                (dx, dy) = event.rel
                #find new looked at position
                oldAngleX, oldAngleY = lookAngleX, lookAngleY
                lookAngleX += .005*dy*sens
                lookAngleY -= .005*dx*sens
                if (lookAngleX > -.44 and lookAngleX < .44 and 
                lookAngleY > -.44 and lookAngleY < .44):
                    drawnRoom.points = rotateCube(room.points, lookAngleX,
                    lookAngleY)
                    for target in targets:
                        i = targets.index(target)
                        drawnTargets[i].points = rotateCube(target.points, 
                        lookAngleX, lookAngleY)
                else:
                    lookAngleX, lookAngleY = oldAngleX, oldAngleY
        drawSixshot(targets2d, room2d, targetColor)
        drawGameText(timePast, pausedTime, gameStarted, sixshotScore.score, 
        sixshotHits, sixshotShots)
        pygame.draw.circle(screen, crosshairColor, (sWidth/2,sHeight/2),
        crosshairRadius)
        clock.tick(240)
        pygame.display.flip()
    pygame.quit()

def gameOver(sens, targetColor, crosshairColor, crosshairRadius):
    running = True
    pygame.event.set_grab(False)
    pygame.mouse.set_visible(True)
    backButton = Button(sWidth/3, 3*sHeight/4, sWidth/50, sHeight/50, 
    (255,0,0))
    nextButton = Button(2*sWidth/3, 3*sHeight/4, sWidth/50, sHeight/50,
    (0,255,0))
    accuracyReport = True
    scoreReport = False
    hitPerTimeReport = False
    while running:
        screen.fill((100,255,255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                #treat resume as replay button here
                if resumeButton.pressed():
                    buttonSound.play()
                    sixshot(sens, targetColor, crosshairColor, crosshairRadius)
                elif homeButton.pressed():
                    buttonSound.play()
                    main(sens, targetColor, crosshairColor, crosshairRadius)
                elif helpButton.pressed():
                    buttonSound.play()
                    helpMenu(sens, targetColor, crosshairColor, crosshairRadius)
                elif quitButton.pressed():
                    buttonSound.play()
                    pygame.quit()
                elif settingsButton.pressed():
                    buttonSound.play()
                    settings(sens, targetColor, crosshairColor, crosshairRadius)
                elif nextButton.pressed():
                    buttonSound.play()
                    if accuracyReport:
                        accuracyReport = False
                        scoreReport = True
                    elif scoreReport:
                        scoreReport = False
                        hitPerTimeReport = True
                elif backButton.pressed():
                    buttonSound.play()
                    if scoreReport:
                        scoreReport = False
                        accuracyReport = True
                    elif hitPerTimeReport:
                        hitPerTimeReport = False
                        scoreReport = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause(sens, targetColor, crosshairColor, crosshairRadius)
        #Buttons
        screen.blit(quitButton.rect, (quitButton.left, 
        quitButton.top))
        screen.blit(settingsButton.rect, (settingsButton.left, 
        settingsButton.top))
        screen.blit(helpButton.rect, (helpButton.left, helpButton.top))
        screen.blit(homeButton.rect, (homeButton.left, homeButton.top))
        screen.blit(resumeButton.rect, (resumeButton.left, resumeButton.top))
        if accuracyReport:
            screen.blit(nextButton.rect, (nextButton.left, nextButton.top))
        elif scoreReport:
            screen.blit(nextButton.rect, (nextButton.left, nextButton.top))
            screen.blit(backButton.rect, (backButton.left, backButton.top))
        else:
            screen.blit(backButton.rect, (backButton.left, backButton.top))
        #Text
        screen.blit(replayText, resumeTextRect)
        screen.blit(quitText, quitTextRect)
        screen.blit(settingsText, settingsTextRect)
        screen.blit(helpText, helpTextRect)
        screen.blit(homeText, homeTextRect)
        #Performance Report
        drawPerformanceReport(accuracyReport, scoreReport, hitPerTimeReport)
        drawGameOverText()
        pygame.display.flip()
    pygame.quit()

def drawPerformanceReport(accuracyReport, scoreReport, hitPerTimeReport):
    if len(scores) > 1:
        currentAcc, avgAcc = accuracies[-1], (sum(accuracies)/len(accuracies))
        currentScore, avgScore = scores[-1], (sum(scores)/len(scores))
        currentHPT = round(totalHits[-1]/60,2)
        avgHPT = round(sum(totalHits)/(len(totalHits)*60),2)
        if accuracyReport:
            if currentAcc >= avgAcc:
                inc = int((100*currentAcc/avgAcc))-100
                accPerf = smallFont.render(
                f'Your accuracy was {inc}% better than your average', False, 
                (0,0,0))
                accPerfRect = accPerf.get_rect(center=(sWidth/2,
                3*sHeight/4))
            else:
                dec = 100-(int(100*currentAcc/avgAcc))
                accPerf = smallFont.render(
                f'Your accuracy was {dec}% worse than your average', False, 
                (0,0,0))
                accPerfRect = accPerf.get_rect(center=(sWidth/2,
                3*sHeight/4))
            screen.blit(accPerf, accPerfRect)
        elif scoreReport:
            if currentScore >= avgScore:
                inc = int((100*currentScore/avgScore))-100
                scorePerf = smallFont.render(
                f'Your score was {inc}% better than your average', False, 
                (0,0,0))
                scorePerfRect = scorePerf.get_rect(center=(sWidth/2,
                3*sHeight/4))
            else:
                dec = 100-(int(100*currentScore/avgScore))
                scorePerf = smallFont.render(
                f'Your score was {dec}% worse than your average', False, 
                (0,0,0))
                scorePerfRect = scorePerf.get_rect(center=(sWidth/2,
                3*sHeight/4))
            screen.blit(scorePerf, scorePerfRect)
        else:
            if currentHPT >= avgHPT:
                inc = int((100*currentHPT/avgHPT))-100
                HPTPerf = smallFont.render(
                f'Your hits/second was {inc}% better than your average', False, 
                (0,0,0))
                HPTPerfRect = HPTPerf.get_rect(center=(sWidth/2,
                3*sHeight/4))
            else:
                dec = 100-(int(100*currentHPT/avgHPT))
                HPTPerf = smallFont.render(
                f'Your hits/second was {dec}% worse than your average', False, 
                (0,0,0))
                HPTPerfRect = HPTPerf.get_rect(center=(sWidth/2,
                3*sHeight/4))
            screen.blit(HPTPerf, HPTPerfRect)
    else:
        noText = smallFont.render('Nothing here yet!', False, (0,0,0))
        noTextRect = noText.get_rect(center=(sWidth/2,3*sHeight/4))
        screen.blit(noText, noTextRect)

def drawGameOverText():
    scoreText = font.render(f'Score: {scores[-1]}',False,(0,0,0))
    scoreTextRect = scoreText.get_rect(center=(sWidth/2,sHeight/20))
    if scores[-1] == max(scores):
        highScoreText = font.render('You got a high score!',False,(0,0,0))
        highScoreTextRect = highScoreText.get_rect(center=(sWidth/2,
        3*sHeight/20))
        screen.blit(highScoreText, highScoreTextRect)
    accuracyText = font.render(f'Accuracy: {accuracies[-1]}%',False,(0,0,0))
    accuracyTextRect = accuracyText.get_rect(center=(sWidth/2, 2*sHeight/5))
    if accuracies[-1] == max(accuracies):
        bestAccuracyText = font.render('This is your best accuracy!',False,
        (0,0,0))
        bestAccuracyTextRect = bestAccuracyText.get_rect(center=(sWidth/2,
        sHeight/2))
        screen.blit(bestAccuracyText, bestAccuracyTextRect)
    screen.blit(scoreText, scoreTextRect)
    screen.blit(accuracyText, accuracyTextRect)

def drawGameText(timePast, pausedTime, gameStarted, score, sixshotHits, 
sixshotShots):
    startCountdown = font.render(f'{int(4-timePast+pausedTime)}', False, 
    (0,0,0))
    startCountdownRect = startCountdown.get_rect(center=(sWidth/2,
    sHeight/3))
    gameCountdown = font.render(f'{int(64-timePast+pausedTime)}', False, 
    (0,0,0))
    gameCountdownRect = gameCountdown.get_rect(center=(sWidth/2,
    3*sHeight/20))
    scoreCount = font.render(f'Score: {score}', False, (0,0,0))
    scoreCountRect = scoreCount.get_rect(center=(sWidth/2,sHeight/20))
    if sixshotShots >= 1:
        accuracy = int(100*sixshotHits/sixshotShots)
        accuracyCount = font.render(f'Accuracy: {accuracy}%', False, (0,0,0))
        accuracyCountRect = accuracyCount.get_rect(center=(sWidth/2,
        sHeight/10))
    else:
        accuracyCount = font.render('Accuracy: 0%', False, (0,0,0))
        accuracyCountRect = accuracyCount.get_rect(center=(sWidth/2,
        sHeight/10))
    if not gameStarted:
        screen.blit(startCountdown, startCountdownRect)
    else:
        screen.blit(gameCountdown, gameCountdownRect)
        screen.blit(scoreCount, scoreCountRect)
        screen.blit(accuracyCount, accuracyCountRect)

def targetClicked(lookX, lookY, target, targets, drawnTargets, drawnRoom, 
targetLength, sixshotScore, lookAngleX, lookAngleY):
    if (round(lookX) >= target.cx-target.length/2 and 
    round(lookX) <= target.cx+target.length/2 and 
    round(lookY) >= target.cy-target.length/2 and 
    round(lookY) <= target.cy+target.length/2):
        clickSound.play()
        hit = True
        i = targets.index(target)
        targets.pop(i)
        drawnTargets.pop(i)
        newCube = makeNewCube(targets, drawnRoom, 
        sWidth, sHeight, targetLength)
        targets.append(newCube)
        drawnTargets.append(copy.deepcopy(newCube))
        drawnTargets[-1].points = rotateCube(
        targets[-1].points, lookAngleX, lookAngleY)
        #scoring
        sixshotScore.incrementScore()
        return True
    else:
        return False

def drawSixshot(targets2d, room2d, targetColor):
    createRoomColors(room2d)
    for target in targets2d:
        createTargetColors(targetColor, target)

def createRoomColors(room2d):
    #back wall
    pygame.draw.polygon(screen, (100,255,255), ((room2d[4][0], room2d[4][1]), 
    (room2d[5][0], room2d[5][1]), (room2d[6][0], room2d[6][1]), (room2d[7][0],
    room2d[7][1])))
    #floor
    pygame.draw.polygon(screen, (150,150,150), ((room2d[0][0], room2d[0][1]), 
    (room2d[1][0], room2d[1][1]), (room2d[5][0], room2d[5][1]), (room2d[4][0], 
    room2d[4][1])))
    #roof
    pygame.draw.polygon(screen, (150,150,150), ((room2d[3][0], room2d[3][1]), 
    (room2d[2][0], room2d[2][1]), (room2d[6][0], room2d[6][1]), (room2d[7][0],
    room2d[7][1])))
    #left wall
    pygame.draw.polygon(screen, (100,255,255), ((room2d[0][0], room2d[0][1]), 
    (room2d[3][0], room2d[3][1]), (room2d[7][0], room2d[7][1]), (room2d[4][0],
    room2d[4][1])))
    #right wall
    pygame.draw.polygon(screen, (100,255,255), ((room2d[1][0], room2d[1][1]), 
    (room2d[2][0], room2d[2][1]), (room2d[6][0], room2d[6][1]), (room2d[5][0],
    room2d[5][1])))

def createTargetColors(targetColor, pointsList):
    #back wall
    pygame.draw.polygon(screen, targetColor, ((pointsList[4][0], 
    pointsList[4][1]), (pointsList[5][0], pointsList[5][1]), 
    (pointsList[6][0], pointsList[6][1]), (pointsList[7][0], pointsList[7][1])))
    #floor
    pygame.draw.polygon(screen, targetColor, ((pointsList[0][0], 
    pointsList[0][1]), (pointsList[1][0], pointsList[1][1]), (pointsList[5][0], 
    pointsList[5][1]), (pointsList[4][0], pointsList[4][1])))
    #roof
    pygame.draw.polygon(screen, targetColor, ((pointsList[3][0], 
    pointsList[3][1]), (pointsList[2][0], pointsList[2][1]), (pointsList[6][0], 
    pointsList[6][1]), (pointsList[7][0], pointsList[7][1])))
    #left wall
    pygame.draw.polygon(screen, targetColor, ((pointsList[0][0], 
    pointsList[0][1]), (pointsList[3][0], pointsList[3][1]), (pointsList[7][0], 
    pointsList[7][1]), (pointsList[4][0], pointsList[4][1])))
    #right wall
    pygame.draw.polygon(screen, targetColor, ((pointsList[1][0], 
    pointsList[1][1]), (pointsList[2][0], pointsList[2][1]), (pointsList[6][0], 
    pointsList[6][1]), (pointsList[5][0], pointsList[5][1])))
    #front wall
    pygame.draw.polygon(screen, targetColor, ((pointsList[0][0],
    pointsList[0][1]),(pointsList[1][0],pointsList[1][1]),(pointsList[2][0],
    pointsList[2][1]),(pointsList[3][0],pointsList[3][1])))

def getTargets(targetsL, drawnRoom, sWidth, sHeight, targetLength):
    while len(targetsL) < 6:
        newCube = makeNewCube(targetsL,drawnRoom,sWidth,sHeight,targetLength)
        targetsL.append(newCube)

#try to prevent spawning outside the room
def makeNewCube(targetsL, drawnRoom, sWidth, sHeight, targetLength):
    dx = random.randint(int(drawnRoom.cx-drawnRoom.length//4),
    int(drawnRoom.cx+drawnRoom.length//4))
    dy = random.randint(int(drawnRoom.cy-drawnRoom.length//4),
    int(drawnRoom.cy+drawnRoom.length//4))
    newCube = Cube(dx, dy, 70, targetLength)
    if illegalCube(targetsL, newCube, targetLength):
        dx = random.randint(int(drawnRoom.cx-drawnRoom.length//4),
        int(drawnRoom.cx+drawnRoom.length//4))
        dy = random.randint(int(drawnRoom.cy-drawnRoom.length//4),
        int(drawnRoom.cy+drawnRoom.length//4))
        newCube = Cube(dx, dy, 70, targetLength)
    return newCube

def illegalCube(targetsL, newCube, targetLength):
    for target in targetsL:
        if newCube == target:
            return True
        elif (newCube.cx - target.cx < targetLength or 
        newCube.cy - target.cy < targetLength):
            return True
    return False

#code from the 3D graphics mini lecture
def convertTo2d(pointsList):
    newPointsList = copy.copy(pointsList)
    i = 0
    for point in newPointsList:
        if point[2] != 0:
            zInv = 1.0 / point[2]
        else:
            zInv = 0
        xFactor, yFactor = sWidth/2, sHeight/2
        newPoint = [0, 0, 0]
        newPoint[0] = (point[0] * zInv + 1) * xFactor
        newPoint[1] = (point[1] * zInv + 1) * yFactor
        newPointsList[i] = newPoint
        i += 1
    return newPointsList

#Rotation matrices and matrix multiplication function from Yuta A's YouTube Video:
#https://www.youtube.com/watch?v=sQDFydEtBLE
def rotateCube(pointsList, angle_x, angle_y):
    newPointsList = copy.deepcopy(pointsList)
    for point in newPointsList:
        i = newPointsList.index(point)
        pointMatrix = [[point[0]],[point[1]],[point[2]]]
        rotation_x = [[1, 0, 0],
                    [0, math.cos(angle_x), -math.sin(angle_x)],
                    [0, math.sin(angle_x), math.cos(angle_x)]]

        rotation_y = [[math.cos(angle_y), 0, math.sin(angle_y)],
                    [0, 1, 0],
                    [-math.sin(angle_y), 0, math.cos(angle_y)]]
        rotate_x = multiplyMatrix(rotation_x, pointMatrix)
        rotate_y = multiplyMatrix(rotation_y, rotate_x)
        x, y, z = rotate_y[0][0], rotate_y[1][0], rotate_y[2][0]
        newPointsList[i] = [x, y, z]
    return newPointsList

def multiplyMatrix(a,b):
    a_rows = len(a)
    a_cols = len(a[0])
    b_rows = len(b)
    b_cols = len(b[0])
    # Dot product matrix dimentions = a_rows x b_cols
    product = [[0 for _ in range(b_cols)] for _ in range(a_rows)]
    if a_cols == b_rows:
        for i in range(a_rows):
            for j in range(b_cols):
                for k in range(b_rows):
                    product[i][j] += a[i][k] * b[k][j]
    else:
        return None
    return product  

main(sens, targetColor, crosshairColor, crosshairRadius)
