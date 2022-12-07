from cmu_112_graphics import *
import math, random, copy
from score import Score
from button import Button
from cube import Cube

#Initial launch will be a bit slow due to GIFs
#Switching screen code from 112 course notes
#Getting user input from 112 course notes
#Gif code from 112 course notes, gif from 
#https://tenor.com/view/fortnite-default-dance-gif-13330926
#Converting to 2d from the 3D graphics mini-lecture
#Matrix multiplication and rotation matrices function from Yuta A.'s YouTube 
#Video: 3D Rotation & Projection using Python/Pygame

#Main menu
def mainMenu_redrawAll(app, canvas):
    #creating buttons
    canvas.create_rectangle(app.sixshotButton.left, app.sixshotButton.top, 
    app.sixshotButton.right, app.sixshotButton.bottom, 
    fill = app.sixshotButton.color)
    canvas.create_rectangle(app.helpButton.left, app.helpButton.top,
    app.helpButton.right, app.helpButton.bottom,
    fill = app.helpButton.color)
    canvas.create_text(app.sixshotButton.cx, app.sixshotButton.cy,
    text='Sixshot', font='Arial 28 bold')
    canvas.create_text(app.width//2, app.height//20, 
    text = 'Welcome to AIMLABS at home!', font = 'Arial 28 bold')
    canvas.create_text(app.width//2, app.height//10,
    text = f'{app.catchphrase}', font = 'Arial 16')
    canvas.create_text(app.helpButton.cx, app.helpButton.cy,
    text = 'Help', font = 'Arial 28 bold')
    if app.gifsOn == True:
        photoImage1 = app.spritePhotoImages[app.spriteCounter]
        canvas.create_image(app.width//10, app.height//2, image=photoImage1)
        photoImage2 = app.spritePhotoImages[app.spriteCounter]
        canvas.create_image(9*app.width//10, app.height//2, image=photoImage2)

def mainMenu_mousePressed(app, event):
    if app.sixshotButton.pressed(event.x, event.y):
        app.mode = 'sixshot'
        app.timerDelay = 200
    elif app.helpButton.pressed(event.x, event.y):
        app.oldMode = app.mode
        app.mode = 'helpMenu'
        app.timerDelay = 200

def mainMenu_keyPressed(app, event):
    if event.key == 'Escape':
        app.oldMode = app.mode
        app.mode = 'escapeMenu'

def mainMenu_loadAnimatedGif(path):
    # load first sprite outside of try/except to raise file-related exceptions
    spritePhotoImages = [ PhotoImage(file=path, format='gif -index 0') ]
    i = 1
    while True:
        try:
            spritePhotoImages.append(PhotoImage(file=path,
                                                format=f'gif -index {i}'))
            i += 1
        except Exception as e:
            return spritePhotoImages

def mainMenu_timerFired(app):
    if app.gifsOn:
        app.spriteCounter = (1 + app.spriteCounter) % len(app.spritePhotoImages)

#Help menu
def helpMenu_redrawAll(app, canvas):
    canvas.create_text(app.width//2, app.height//20,
    text = 'Welcome to AimPy!', font = 'Arial 28 bold')
    canvas.create_text(app.width//2, app.height//4,
    text = '''In the main menu, click on any of the blue buttons to begin 
    playing. Destroy as many targets as you can in the alotted time frame to
    achieve a high score! Successive hits reward more points!''', 
    font = 'Arial 28 bold', justify = 'center')
    canvas.create_text(app.width//2, app.height//2,
    text = 'Press the back button to return to the main menu', 
    font = 'Arial 28 bold')
    canvas.create_rectangle(app.homeButton.left, app.homeButton.top,
    app.homeButton.right, app.homeButton.bottom, fill = "gray")
    canvas.create_text(app.homeButton.cx, app.homeButton.cy,
    text = 'Back', font = 'Arial 28 bold')

def helpMenu_mousePressed(app, event):
    if app.homeButton.pressed(event.x, event.y):
        app.mode = 'mainMenu'
        app.timerDelay = 40

#Escape menu
def escapeMenu_redrawAll(app, canvas):
    if app.oldMode != 'mainMenu':
        canvas.create_rectangle(app.resumeButton.left, app.resumeButton.top,
        app.resumeButton.right, app.resumeButton.bottom, 
        fill = app.resumeButton.color)
        canvas.create_text(app.resumeButton.cx, app.resumeButton.cy, 
        text = 'Resume', font = 'Arial 28 bold')
    canvas.create_rectangle(app.settingsButton.left, app.settingsButton.top,
    app.settingsButton.right, app.settingsButton.bottom, 
    fill = app.settingsButton.color)
    canvas.create_rectangle(app.homeButton.left, app.homeButton.top,
    app.homeButton.right, app.homeButton.bottom, fill = app.homeButton.color)
    canvas.create_text(app.homeButton.cx, app.homeButton.cy,
    text = 'Home', font = 'Arial 28 bold')
    canvas.create_text(app.settingsButton.cx, app.settingsButton.cy,
    text = 'Settings', font = 'Arial 28 bold')

def escapeMenu_mousePressed(app, event):
    if app.resumeButton.pressed(event.x, event.y):
        app.mode = app.oldMode
    elif app.homeButton.pressed(event.x, event.y):
        # oldTargetColor = app.targetColor
        # oldGifStatus = app.gifsOn
        # appStarted(app)
        # app.gifsOn = oldGifStatus
        # app.targetColor = oldTargetColor
        app.mode = 'mainMenu'
        app.timerDelay = 40
    elif app.settingsButton.pressed(event.x, event.y):
        app.mode = 'settings'

#Settings
def settings_redrawAll(app, canvas):
    canvas.create_rectangle(app.sensButton.left, app.sensButton.top,
    app.sensButton.right, app.sensButton.bottom, fill = app.sensButton.color)
    canvas.create_text(app.width//2, app.height//20,
    text = f'Target color: {app.targetColor}')
    canvas.create_text(app.sensButton.cx, app.sensButton.cy,
    text = 'Edit Sensitivity', font = 'Arial 28 bold')
    canvas.create_text(app.width//2, app.height//10, 
    text = f'Sensitivity: {app.sens}')
    canvas.create_rectangle(app.targetColorButton.left,
    app.targetColorButton.top, app.targetColorButton.right,
    app.targetColorButton.bottom, fill = app.targetColorButton.color)
    canvas.create_text(app.targetColorButton.cx, app.targetColorButton.cy,
    text = 'Edit Target Color', font = 'Arial 28 bold')
    canvas.create_rectangle(app.exitButton.left, app.exitButton.top,
    app.exitButton.right, app.exitButton.bottom, fill = app.exitButton.color)
    canvas.create_text(app.exitButton.cx, app.exitButton.cy,
    text = 'Exit', font = 'Arial 28 bold')
    canvas.create_text(app.width//10, app.height//6, text = 'Possible Colors:',
    font = 'Arial 20 bold', justify = 'center')
    canvas.create_text(app.width//10, app.height//6 + app.height//15,
    text = 'Yellow\nBlue\nGreen\nRed\nBlack\nWhite', justify = 'center')
    canvas.create_rectangle(app.gifsButton.left, app.gifsButton.top,
    app.gifsButton.right, app.gifsButton.bottom, fill = app.gifsButton.color)
    if app.gifsOn:
        canvas.create_text(app.gifsButton.cx, app.gifsButton.cy, 
        text = 'Disable main menu GIFs', font = 'Arial 28 bold')
    elif app.gifsOn != True:
        canvas.create_text(app.gifsButton.cx, app.gifsButton.cy, 
        text = 'Enable main menu GIFs', font = 'Arial 28 bold')

def settings_mousePressed(app, event):
    if app.sensButton.pressed(event.x, event.y):
        oldSens = app.sens
        app.sens = app.getUserInput('Enter your new sensitivity:')
        if app.sens == None:
            app.sens = oldSens
    elif app.exitButton.pressed(event.x, event.y):
        app.mode = 'escapeMenu'
    elif app.targetColorButton.pressed(event.x, event.y):
        oldColor = app.targetColor
        app.targetColor = app.getUserInput(
        'Enter your new target color in all lowercase:')
        while app.targetColor not in app.possibleTargetColors:
            app.targetColor = oldColor
            app.targetColor = app.getUserInput(
        'That was not a valid color! Enter your new target color:')
    elif app.gifsButton.pressed(event.x, event.y):
        app.gifsOn = not app.gifsOn

#Sixshot
def sixshot_redrawAll(app, canvas):
    createRoomColors(app, canvas)
    #target lines
    for target in app.targets2d:
        createTargetColors(app, canvas, target)
        #create colors
    canvas.create_oval(app.width//2 + 3,app.height//2 + 3,
    app.width//2 - 3,app.height//2 - 3)
    #stats
    if app.gameStarted == False:
        canvas.create_text(app.width//2, 3*app.height//20, 
        text = f'Start in: {(4000-app.timePast)//1000}')
    elif app.gameStarted:
        canvas.create_text(app.width//2, 3*app.height//20,
        text = f'Time remaining: {(60000-app.gameTimePast)//1000}')
        if app.sixshotShots > 0:
            canvas.create_text(app.width//2, app.height//20,
            text = f'Score: {app.sixshotScore.score}', font = 'Arial 28',
            justify = 'center')
            canvas.create_text(app.width//2, app.height//10,
            text = f'Accuracy: {round(100*app.sixshotHits/app.sixshotShots)}%', 
            font = 'Arial 28', justify = 'center')
        else:
            canvas.create_text(app.width//2, app.height//20,
            text = 'Score: 0', font = 'Arial 28', justify = 'center')
            canvas.create_text(app.width//2, app.height//10,
            text = 'Accuracy: 0%', font = 'Arial 28', justify = 'center')

def createRoomColors(app, canvas):
    #back wall
    canvas.create_polygon(app.room2d[4][0], app.room2d[4][1], app.room2d[5][0],
    app.room2d[5][1], app.room2d[6][0], app.room2d[6][1], app.room2d[7][0],
    app.room2d[7][1], fill = "light blue")
    #floor
    canvas.create_polygon(app.room2d[0][0], app.room2d[0][1], app.room2d[1][0],
    app.room2d[1][1], app.room2d[5][0], app.room2d[5][1], app.room2d[4][0],
    app.room2d[4][1], fill = "light gray")
    #roof
    canvas.create_polygon(app.room2d[3][0], app.room2d[3][1], app.room2d[2][0],
    app.room2d[2][1], app.room2d[6][0], app.room2d[6][1], app.room2d[7][0],
    app.room2d[7][1], fill = "light gray")
    #left wall
    canvas.create_polygon(app.room2d[0][0], app.room2d[0][1], app.room2d[3][0],
    app.room2d[3][1], app.room2d[7][0], app.room2d[7][1], app.room2d[4][0],
    app.room2d[4][1], fill = "light blue")
    #right wall
    canvas.create_polygon(app.room2d[1][0], app.room2d[1][1], app.room2d[2][0],
    app.room2d[2][1], app.room2d[6][0], app.room2d[6][1], app.room2d[5][0],
    app.room2d[5][1], fill = "light blue")

def createTargetColors(app, canvas, pointsList):
    #front face
    canvas.create_polygon(pointsList[0][0], pointsList[0][1], pointsList[1][0],
    pointsList[1][1], pointsList[2][0], pointsList[2][1], pointsList[3][0],
    pointsList[3][1], fill = app.targetColor)
    #back face
    canvas.create_polygon(pointsList[4][0], pointsList[4][1], pointsList[5][0],
    pointsList[5][1], pointsList[6][0], pointsList[6][1], pointsList[7][0],
    pointsList[7][1], fill = app.targetColor)
    #floor
    canvas.create_polygon(pointsList[0][0], pointsList[0][1], pointsList[1][0],
    pointsList[1][1], pointsList[5][0], pointsList[5][1], pointsList[4][0],
    pointsList[4][1], fill = app.targetColor)
    #roof
    canvas.create_polygon(pointsList[3][0], pointsList[3][1], pointsList[2][0],
    pointsList[2][1], pointsList[6][0], pointsList[6][1], pointsList[7][0],
    pointsList[7][1], fill = app.targetColor)
    #left face
    canvas.create_polygon(pointsList[0][0], pointsList[0][1], pointsList[3][0],
    pointsList[3][1], pointsList[7][0], pointsList[7][1], pointsList[4][0],
    pointsList[4][1], fill = app.targetColor)
    #right face
    canvas.create_polygon(pointsList[1][0], pointsList[1][1], pointsList[2][0],
    pointsList[2][1], pointsList[6][0], pointsList[6][1], pointsList[5][0],
    pointsList[5][1], fill = app.targetColor)    

def drawConnectorLines(canvas, list, i, j):
    canvas.create_line(list[i][0],list[i][1],list[j][0],list[j][1])

def sixshot_timerFired(app):
    #converts cubes to 2d after any changes
    if app.gameStarted == False:
        app.timePast += app.timerDelay
    if app.timePast >= 3000:
        app.gameStarted = True
        app.timerDelay = 5
        app.timePast = 0
    if app.gameStarted:
        app.gameTimePast += app.timerDelay
        app.room2d = convertTo2d(app, app.drawnRoom.points, app.width//2, 
        app.height//2)
        app.gameTimePast += app.timerDelay
        for target in app.drawnTargets:
            i = app.drawnTargets.index(target)
            target2d = convertTo2d(app, target.points, app.width//2, 
            app.height//2)
            app.targets2d[i] = target2d
        #end game, switch to game over
        if app.gameTimePast >= 15000:
            app.oldMode = app.mode
            app.mode = 'gameOver'

def sixshot_keyPressed(app, event):
    if event.key == 'a':
        if app.drawnRoom.cx < app.drawnRoom.length/2:
            #update the points after updating cx in both room and target lists
            for point in app.drawnRoom.points:
                point[0] += app.room.length/100
            for point in app.room.points:
                point[0] += app.room.length/100
            app.room.updateCenter()
            app.drawnRoom.updateCenter()
            for target in app.drawnTargets:
                for point in target.points:
                    point[0] += app.drawnRoom.length/100
                target.updateCenter()
            for target in app.targets:
                for point in target.points:
                    point[0] += app.room.length/100
                target.updateCenter()
    elif event.key == 'd':
        if app.drawnRoom.cx > -app.room.length/2:
            for point in app.drawnRoom.points:
                point[0] -= app.room.length/100
            for point in app.room.points:
                point[0] -= app.room.length/100
            app.room.updateCenter()
            app.drawnRoom.updateCenter()
            for target in app.drawnTargets:
                for point in target.points:
                    point[0] -= app.drawnRoom.length/100
                target.updateCenter()
            for target in app.targets:
                for point in target.points:
                    point[0] -= app.room.length/100
                target.updateCenter()
    #rotateCube is a non-destructive function that returns rotated points
    elif event.key == 'Up':
        #rotate down
        if app.lookAngleX > -.44:
            app.lookAngleX -= .01*app.sens
            app.drawnRoom.points = rotateCube(app.room.points, 
            app.lookAngleX, app.lookAngleY)
            for target in app.targets:
                i = app.targets.index(target)
                app.drawnTargets[i].points = rotateCube(target.points, 
                app.lookAngleX, app.lookAngleY)
    elif event.key == 'Down':
        #rotate up
        if app.lookAngleX < .44:
            app.lookAngleX += .01*app.sens
            app.drawnRoom.points = rotateCube(app.room.points, 
            app.lookAngleX, app.lookAngleY)
            for target in app.targets:
                i = app.targets.index(target)
                app.drawnTargets[i].points = rotateCube(target.points, 
                app.lookAngleX, app.lookAngleY)
    elif event.key == 'Left':
        #rotate right
        if app.lookAngleY < .44:
            app.lookAngleY += .01*app.sens
            app.drawnRoom.points = rotateCube(app.room.points, 
            app.lookAngleX, app.lookAngleY)
            for target in app.targets:
                i = app.targets.index(target)
                app.drawnTargets[i].points = rotateCube(target.points, 
                app.lookAngleX, app.lookAngleY)
    elif event.key == 'Right':
        #rotate left
        if app.lookAngleY > -.44:
            app.lookAngleY -= .01*app.sens
            app.drawnRoom.points = rotateCube(app.room.points, 
            app.lookAngleX, app.lookAngleY)
            for target in app.targets:
                i = app.targets.index(target)
                app.drawnTargets[i].points = rotateCube(target.points, 
                app.lookAngleX, app.lookAngleY)
    elif event.key == 'Escape':
        app.oldMode = app.mode
        app.mode = 'escapeMenu'

def sixshot_mousePressed(app, event):
    hit = False
    for target in app.targets:
        if targetClicked(app, target):
            hit = True
            #remove the target from every list of targets
            i = app.targets.index(target)
            app.drawnTargets.pop(i)
            app.targets.pop(i)
            #generate a new target
            newCube = makeNewCube(app)
            app.targets.append(newCube)
            app.drawnTargets.append(copy.deepcopy(newCube))
            app.drawnTargets[-1].points = rotateCube(app.targets[-1].points, 
            app.lookAngleX, app.lookAngleY)
            #scoring and stats
            app.sixshotScore.incrementScore()
            app.sixshotHits += 1
            app.sixshotShots += 1
            sixshot_missedCounter(app, event.x, event.y)
            app.missedPointsL = []
            break
    if hit == False:
        app.missedPointsL.append((event.x, event.y))
        app.sixshotScore.resetScoreIncrement()
        app.sixshotShots += 1

def sixshot_mouseMoved(app, event):
    dx = event.x - app.oldX
    dy = event.y - app.oldY
    app.oldX, app.oldY = event.x, event.y
    oldAngleX, oldAngleY = app.lookAngleX, app.lookAngleY
    app.lookAngleX += .005*dy*app.sens
    app.lookAngleY -= .005*dx*app.sens
    if (app.lookAngleX > -.44 and app.lookAngleX < .44 and app.lookAngleY > -.44
    and app.lookAngleY < .44):
        app.drawnRoom.points = rotateCube(app.room.points, 
        app.lookAngleX, app.lookAngleY)
        for target in app.targets:
            i = app.targets.index(target)
            app.drawnTargets[i].points = rotateCube(target.points, 
            app.lookAngleX, app.lookAngleY)    
    else:
        app.lookAngleX, app.lookAngleY = oldAngleX, oldAngleY

#uses trig to find the location that the camera is looking at
def targetClicked(app, target):
    lookX = -1*target.cz*math.tan(app.lookAngleY) 
    lookY = target.cz*math.tan(app.lookAngleX) 
    if (round(lookX) >= target.cx-target.length/2 and 
    round(lookX) <= target.cx+target.length/2 and 
    round(lookY) >= target.cy-target.length/2 and 
    round(lookY) <= target.cy+target.length/2):
        return True

#builds performance report stats
def sixshot_missedCounter(app, mouseX, mouseY):
    for miss in app.missedPointsL:
        x, y = miss[0], miss[1]
        if x <= mouseX - 2*app.targetLength2d:
            app.sixshotMissedLeft += 1
        elif x >= mouseX + 2*app.targetLength2d:
            app.sixshotMissedRight += 1
        if y <= mouseY - 2*app.targetLength2d:
            app.sixshotMissedUp += 1
        elif y >= mouseY + 2*app.targetLength2d:
            app.sixshotMissedDown += 1

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

#Game over
def gameOver_redrawAll(app, canvas):
    if app.oldMode == 'sixshot':
        canvas.create_text(app.width//2,app.height//18,
            text = f'Your final score is: {app.sixshotScore.score}', 
            font = 'Arial 36 bold')
        if app.sixshotShots > 0:
            canvas.create_text(app.width//2,app.height//9, 
            text= 
            f'Accuracy: {math.floor((app.sixshotHits/app.sixshotShots)*100)}%',
            font='Arial 36 bold')
        else:
            canvas.create_text(app.width//2,4*app.height//5, 
            text= 
            f'Accuracy: 0%', font='Arial 36 bold')
    #create the replay button
    canvas.create_rectangle(app.resumeButton.left, app.resumeButton.top,
        app.resumeButton.right, app.resumeButton.bottom, 
        fill = app.resumeButton.color)
    canvas.create_text(app.resumeButton.cx, app.resumeButton.cy, 
    text = 'Replay', font = 'Arial 28 bold')
    #create the home button
    canvas.create_rectangle(app.homeButton.left, app.homeButton.top,
    app.homeButton.right, app.homeButton.bottom, fill = app.homeButton.color)
    canvas.create_text(app.homeButton.cx, app.homeButton.cy,
    text = 'Home', font = 'Arial 28 bold')
    #when the user can play again
    if app.gameOverTime//1000 <= 1:
        canvas.create_text(app.width//2, 2*app.height//9,
        text = f'You can play again in {2-app.gameOverTime//1000}')
    #performance report
    if app.directionReport:
        worstDirection = findWorstDirection(app)
        if worstDirection != None:
            canvas.create_text(app.width//2, 4*app.height//5,
            text = f'You missed the most in this direction: {worstDirection}')
        elif app.sixshotShots > 5:
            canvas.create_text(app.width//2, 4*app.height//5,
            text = f'You mostly aimed very close to the target, nice!')
        else:
            canvas.create_text(app.width//2, 4*app.height//5,
            text = f'Click the green button to view performance reports!')
        canvas.create_polygon(app.nextButton.left, app.nextButton.top,
        app.nextButton.left, app.nextButton.bottom, app.nextButton.right,
        app.nextButton.cy, fill = app.nextButton.color)
    elif app.accuracyReport:
        canvas.create_polygon(app.nextButton.left, app.nextButton.top,
        app.nextButton.left, app.nextButton.bottom, app.nextButton.right,
        app.nextButton.cy, fill = app.nextButton.color)
        canvas.create_polygon(app.backButton.left, app.backButton.cy,
        app.backButton.right, app.backButton.top, app.backButton.right,
        app.backButton.bottom, fill = app.backButton.color)
    elif app.totalHitsReport:
        canvas.create_polygon(app.backButton.left, app.backButton.cy,
        app.backButton.right, app.backButton.top, app.backButton.right,
        app.backButton.bottom, fill = app.backButton.color)

def findWorstDirection(app):
    worstDirection = ''
    missedCounters = [app.sixshotMissedLeft, app.sixshotMissedRight, 
    app.sixshotMissedUp, app.sixshotMissedDown]
    mostMisses = 0
    for counter in missedCounters:
        if counter > mostMisses:
            mostMisses = counter
    if mostMisses == 0:
        return None
    missIndex = missedCounters.index(mostMisses)
    if missIndex == 0:
        return 'Left'
    elif missIndex == 1:
        return 'Right'
    elif missIndex == 2:
        return 'Up'
    else:
        return 'Down'

def gameOver_keyPressed(app, event):
    if event.key == 'Escape':
        oldMode = app.mode
        app.mode = 'escapeMenu'

def gameOver_mousePressed(app, event):
    if app.paused == False:
        if app.resumeButton.pressed(event.x, event.y):
            app.mode = app.oldMode
            app.gameStarted = False
            app.timePast = 0
            app.gameTimePast = 0
            app.gameOverTime = 0
            if app.oldMode == 'gridshot':
                app.gridshotScore.resetToDefault()
                app.gridshotHits, app.gridshotShots = 0, 0
            elif app.oldMode == 'sixshot':
                gameOver_restartSixshot(app)
        elif app.homeButton.pressed(event.x, event.y):
            oldTargetColor = app.targetColor
            oldGifStatus = app.gifsOn
            appStarted(app)
            app.targetColor = oldTargetColor
            app.gifsOn = oldGifStatus
        elif app.nextButton.pressed(event.x, event.y):
            if app.directionReport:
                app.directionReport = not app.directionReport
                app.accuracyReport = not app.accuracyReport
            elif app.accuracyReport:
                app.accuracyReport = not app.accuracyReport
                app.totalHitsReport = not app.totalHitsReport
        elif app.backButton.pressed(event.x, event.y):
            if app.accuracyReport:
                app.accuracyReport = not app.accuracyReport
                app.directionReport = not app.directionReport
            elif app.totalHitsReport:
                app.totalHitsReport = not app.totalHitsReport
                app.accuracyReport = not app.accuracyReport

def gameOver_restartSixshot(app):
    # oldTargetColor = app.targetColor
    # oldGifStatus = app.gifsOn
    # appStarted(app)
    # app.gifsOn = oldGifStatus
    # app.targetColor = oldTargetColor
    app.room = Cube(0, 0, 100, 100)
    app.lookAngleX, app.lookAngleY = 0, 0
    app.sixshotScore = Score()
    app.sixshotHits = 0
    app.sixshotShots = 0
    app.gameStarted = False
    app.timePast = 0
    app.gameTimePast = 0
    app.targetLength = app.room.length/50
    app.directionReport = True
    app.accuracyReport = False
    app.totalHitsReport = False
    app.sixshotMissedLeft = 0
    app.sixshotMissedRight = 0
    app.sixshotMissedUp = 0
    app.sixshotMissedDown = 0
    app.missedPointsL = []
    #list of cube instances
    app.targets = []
    app.drawnRoom = copy.deepcopy(app.room)
    getTargets(app)
    #drawn objects are the rotated and actually drawn versions of the
    #original objects
    app.drawnTargets = copy.deepcopy(app.targets)
    app.room2d = convertTo2d(app, app.drawnRoom.points, 
    app.width//2, app.height//2)
    #convert the targets to 2d versions of 3d targets, 3d list
    app.targets2d = []
    for target in app.drawnTargets:
        target2d = convertTo2d(app, target.points, app.width//2, 
        app.height//2)
        app.targets2d.append(target2d)
    app.targetLength2d = app.targets2d[0][1][0] - app.targets2d[0][0][0]
    #game over
    app.gameOverTime = 0
    app.mode = 'sixshot'

def gameOver_timerFired(app):
    app.timerDelay = 100
    app.gameOverTime += app.timerDelay
    if app.gameOverTime >= 1000:
        app.paused = False

#Main app 
def appStarted(app):
    #Main menu
    app.mode = 'mainMenu'
    app.oldMode = app.mode
    app.paused = False
    app.catchphraseList = ['We have the meats!', 'You will love this!',
    'Did you watch the dev hour for this?', 'Haha dev hour deez nuts',
    'you would not believe your eyes', 'I heckin love TenZ', 
    'Technoblade neva dies!','The greatest thing since sliced bread',
    'hop on fortnite!','u gotta be trolling']
    app.catchphrase = random.choice(app.catchphraseList)
    app.gifsOn = True
    if app.gifsOn:
        app.spritePhotoImages = mainMenu_loadAnimatedGif('fortnite-default.gif')
        app.spriteCounter = 0
    #Buttons
    app.settingsButton = Button(app.width//2, app.height//2, app.width//4,
    app.height//16, "blue")
    app.sixshotButton = Button(app.width//2, app.height//2, app.width//4,
    app.height//16, "blue")
    app.resumeButton = Button(app.width//2, app.height//3, app.width//4,
    app.height//16, "blue")
    app.homeButton = Button(app.width//2, 2*app.height//3, app.width//4,
    app.height//16, "blue")
    app.targetColorButton = Button(app.width//2, app.height//2, app.width//4,
    app.height//16, "gray")
    app.sensButton = Button(app.width//2, 2*app.height//3, app.width//4,
    app.height//16, "gray")
    app.exitButton = Button(app.width//2, 5*app.height//6, app.width//4,
    app.height//16, "gray")
    app.nextButton = Button(3*app.width//5, 4*app.height//5, app.width//50,
    app.height//30, "green")
    app.backButton = Button(2*app.width//5, 4*app.height//5, app.width//50,
    app.height//30, "red")
    app.helpButton = Button(app.width//2, 2*app.height//3, app.width//20,
    app.height//24, "gray")
    app.gifsButton = Button(app.width//2, app.height//3, app.width//4,
    app.height//16, "gray")
    #settings
    app.sens = .3
    #Sixshot
    app.room = Cube(0, 0, 100, 100)
    app.lookAngleX, app.lookAngleY = 0, 0
    app.oldX, app.oldY = app.width/2, app.height/2
    app.sixshotScore = Score()
    app.sixshotScores = []
    app.sixshotHits = 0
    app.sixshotShots = 0
    app.gameStarted = False
    app.timePast = 0
    app.gameTimePast = 0
    app.targetLength = app.room.length/50
    app.directionReport = True
    app.accuracyReport = False
    app.totalHitsReport = False
    app.accuracies = []
    app.totalHits = []
    app.sixshotMissedLeft = 0
    app.sixshotMissedRight = 0
    app.sixshotMissedUp = 0
    app.sixshotMissedDown = 0
    app.missedPointsL = []
    #list of cube instances
    app.targets = []
    app.targetColor = 'yellow'
    app.possibleTargetColors = set(['yellow', 'blue', 'green', 'red', 'black',
    'white'])
    app.drawnRoom = copy.deepcopy(app.room)
    getTargets(app)
    #drawn objects are the rotated and actually drawn versions of the
    #original objects
    app.drawnTargets = copy.deepcopy(app.targets)
    app.room2d = convertTo2d(app, app.drawnRoom.points, 
    app.width//2, app.height//2)
    #convert the targets to 2d versions of 3d targets, 3d list
    app.targets2d = []
    for target in app.drawnTargets:
        target2d = convertTo2d(app, target.points, app.width//2, 
        app.height//2)
        app.targets2d.append(target2d)
    app.targetLength2d = app.targets2d[0][1][0] - app.targets2d[0][0][0]
    #timer
    app.timerDelay = 40
    #game over
    app.gameOverTime = 0

def getTargets(app):
    while len(app.targets) < 6:
        newCube = makeNewCube(app)
        app.targets.append(newCube)

#try to prevent spawning outside the room
def makeNewCube(app):
    dx = random.randint(int(app.drawnRoom.cx-app.room.length//4),
    int(app.drawnRoom.cx+app.room.length//4))
    dy = random.randint(int(app.drawnRoom.cy-app.room.length//4),
    int(app.drawnRoom.cy+app.room.length//4))
    newCube = Cube(dx, dy, 70, app.targetLength)
    if illegalCube(app, newCube):
        dx = random.randint(int(app.drawnRoom.cx-app.room.length//4),
        int(app.drawnRoom.cx+app.room.length//4))
        dy = random.randint(int(app.drawnRoom.cy-app.room.length//4),
        int(app.drawnRoom.cy+app.room.length//4))
        newCube = Cube(dx, dy, 70, app.targetLength)
    return newCube

def illegalCube(app, newCube):
    for target in app.targets:
        if newCube == target:
            return True
        elif (newCube.cx - target.cx < app.targetLength or 
        newCube.cy - target.cy < app.targetLength):
            return True
    return False

def convertTo2d(app, pointsList, xFactor, yFactor):
    newPointsList = copy.copy(pointsList)
    i = 0
    for point in newPointsList:
        if point[2] != 0:
            zInv = 1.0 / point[2]
        else:
            zInv = 0
        xFactor, yFactor = app.width/2, app.height/2
        newPoint = [0, 0, 0]
        newPoint[0] = (point[0] * zInv + 1) * xFactor
        newPoint[1] = (point[1] * zInv + 1) * yFactor
        newPointsList[i] = newPoint
        i += 1
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
        print("INCOMPATIBLE MATRIX SIZES")
    return product  

runApp(width=1920,height=1080)