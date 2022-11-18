from cmu_112_graphics import *
import math, random
from dot import Dot
from score import Score
from button import Button

#Main menu
def mainMenu_redrawAll(app, canvas):
    #sixshot button dimensions
    sixshotButtonLeft = app.sixshotButton.cx - app.sixshotButton.length
    sixshotButtonRight = app.sixshotButton.cx + app.sixshotButton.length
    sixshotButtonTop = app.sixshotButton.cy - app.sixshotButton.height
    sixshotButtonBottom = app.sixshotButton.cy + app.sixshotButton.height
    #strafetrack button dimensions
    strafetrackButtonLeft = (app.strafetrackButton.cx - 
    app.strafetrackButton.length)
    strafetrackButtonRight = (app.strafetrackButton.cx + 
    app.strafetrackButton.length)
    strafetrackButtonTop = (app.strafetrackButton.cy - 
    app.strafetrackButton.height)
    strafetrackButtonBottom = (app.strafetrackButton.cy + 
    app.strafetrackButton.height)
    #gridshot button dimensions
    gridshotButtonLeft = app.gridshotButton.cx - app.sixshotButton.length
    gridshotButtonRight = app.gridshotButton.cx + app.sixshotButton.length
    gridshotButtonTop = app.gridshotButton.cy - app.sixshotButton.height
    gridshotButtonBottom = app.gridshotButton.cy + app.sixshotButton.height
    #creating buttons
    canvas.create_rectangle(gridshotButtonLeft, gridshotButtonTop,
    gridshotButtonRight, gridshotButtonBottom, fill = app.gridshotButton.color)
    canvas.create_rectangle(strafetrackButtonLeft, strafetrackButtonTop,
    strafetrackButtonRight, strafetrackButtonBottom, 
    fill = app.strafetrackButton.color)
    canvas.create_rectangle(sixshotButtonLeft, sixshotButtonTop, 
    sixshotButtonRight, sixshotButtonBottom, fill = app.sixshotButton.color)
    canvas.create_text(app.gridshotButton.cx, app.gridshotButton.cy,
    text = 'Gridshot', font = 'Arial 28 bold')
    canvas.create_text(app.strafetrackButton.cx, app.strafetrackButton.cy,
    text = 'Strafetrack', font = 'Arial 28 bold')
    canvas.create_text(app.sixshotButton.cx, app.sixshotButton.cy,
    text='Sixshot', font='Arial 28 bold')
    canvas.create_text(app.width//2, app.height//20, 
    text = 'Welcome to AIMLABS at home!', font = 'Arial 28 bold')
    canvas.create_text(app.width//2, app.height//10,
    text = f'{app.catchphrase}', font = 'Arial 16')

def mainMenu_mousePressed(app, event):
    if (event.x >= app.sixshotButton.cx - app.sixshotButton.length and
    event.x <= app.sixshotButton.cx + app.sixshotButton.length and
    event.y >= app.sixshotButton.cy - app.sixshotButton.height and
    event.y <= app.sixshotButton.cy + app.sixshotButton.height):
        app.mode = 'sixshot'
    elif (event.x >= app.strafetrackButton.cx - app.strafetrackButton.length and
    event.x <= app.strafetrackButton.cx + app.strafetrackButton.length and
    event.y >= app.strafetrackButton.cy - app.strafetrackButton.height and
    event.y <= app.strafetrackButton.cy + app.strafetrackButton.height):
        app.mode = 'strafetrack'
    elif (event.x >= app.gridshotButton.cx - app.gridshotButton.length and
    event.x <= app.gridshotButton.cx + app.gridshotButton.length and
    event.y >= app.gridshotButton.cy - app.gridshotButton.height and
    event.y <= app.gridshotButton.cy + app.gridshotButton.height):
        app.mode = 'gridshot'

def mainMenu_keyPressed(app, event):
    if event.key == 'Escape':
        app.oldMode = app.mode
        app.mode = 'escapeMenu'

#Escape menu
def escapeMenu_redrawAll(app, canvas):
    resumeButtonLeft = app.resumeButton.cx - app.resumeButton.length
    resumeButtonRight = app.resumeButton.cx + app.resumeButton.length
    resumeButtonTop = app.resumeButton.cy - app.resumeButton.height
    resumeButtonBottom = app.resumeButton.cy + app.resumeButton.height
    homeButtonLeft = app.homeButton.cx - app.homeButton.length
    homeButtonRight = app.homeButton.cx + app.homeButton.length
    homeButtonTop = app.homeButton.cy - app.homeButton.height
    homeButtonBottom = app.homeButton.cy + app.homeButton.height
    if app.oldMode != 'mainMenu':
        canvas.create_rectangle(resumeButtonLeft, resumeButtonTop,
        resumeButtonRight, resumeButtonBottom, fill = app.resumeButton.color)
        canvas.create_text(app.resumeButton.cx, app.resumeButton.cy, 
        text = 'Resume', font = 'Arial 28 bold')
    canvas.create_rectangle(homeButtonLeft, homeButtonTop,
    homeButtonRight, homeButtonBottom, fill = app.homeButton.color)
    canvas.create_text(app.homeButton.cx, app.homeButton.cy,
    text = 'Home', font = 'Arial 28 bold')

def escapeMenu_mousePressed(app, event):
    if (event.x >= app.resumeButton.cx - app.resumeButton.length and
    event.x <= app.resumeButton.cx + app.resumeButton.length and
    event.y >= app.resumeButton.cy - app.resumeButton.height and
    event.y <= app.resumeButton.cy + app.resumeButton.height):
        app.mode = app.oldMode
    elif (event.x >= app.homeButton.cx - app.homeButton.length and
    event.x <= app.homeButton.cx + app.homeButton.length and
    event.y >= app.homeButton.cy - app.homeButton.height and
    event.y <= app.homeButton.cy + app.homeButton.height):
        appStarted(app)

#Gridshot
def gridshot_redrawAll(app, canvas):
    if app.gameStarted == False:
        canvas.create_text(app.width//2, app.height//2, 
        text=f'{3 - app.timePast//1000}', font='Arial 36 bold')
    canvas.create_text(app.width//2, 30, 
    text=f'Score: {app.gridshotScore.score}',font='Arial 28 bold')
    canvas.create_text(app.width//2, 60, text=f'{60 - app.gameTimePast//1000}')
    if app.gameStarted == True:
        for dot in app.gridshotDotsSet:
            cx, cy, r = dot.cx, dot.cy, app.gridshotR
            canvas.create_oval(cx+r, cy+r, cx-r, cy-r, 
            fill=app.exampleDot.color, width=0)

def gridshot_keyPressed(app, event):
    if event.key == 'Escape':
        app.oldMode = app.mode
        app.mode = 'escapeMenu'

def gridshot_timerFired(app):
    app.timePast += app.timerDelay
    if app.timePast >= 3000:
        app.gameStarted = True
    if app.gameStarted == True:
        app.gameTimePast += app.timerDelay
        if app.gameTimePast >= 6000:
            app.oldMode = app.mode
            app.paused = True
            app.mode = 'gameOver'

def gridshot_mousePressed(app, event):
    if app.gameStarted == True:
        currentDot = 1
        for dot in app.gridshotDotsSet:
            currentDot += 1
            cx, cy, r = dot.cx, dot.cy, app.gridshotR
            #if the mouse click is inside a dot
            if (event.x > cx-r and event.x < cx+r and event.y > cy-r 
            and event.y < cy+r):
                gridshot_dotClicked(app, dot)
                app.gridshotScore.increaseCombo()
                app.gridshotScore.incrementScore()
                print(app.gridshotScore.comboStreak)
                app.gridshotScore.score += app.gridshotScore.scoreIncrement
                app.gridshotHits += 1
                app.gridshotShots += 1
                break
            else:
                if currentDot == len(app.gridshotDotsSet):
                    app.gridshotScore.comboStreak = 0
                    print(app.gridshotScore.comboStreak)
                    app.gridshotScore.resetScoreIncrement()
                    app.gridshotShots += 1

def gridshot_dotClicked(app, dot):
        app.gridshotDotsSet.remove(dot)
        newDot = gridshot_generateDot(app)
        dot.dotClicked()
        #prevent creating another instance of the dot that was just removed
        while gridshot_isOverlapping(app, newDot, app.gridshotDotsSet):
            newDot = gridshot_generateDot(app)
        app.gridshotDotsSet.add(newDot)

def gridshot_generateDot(app):
    cx = random.randint(app.margin+2*app.gridshotR,
    app.width-app.margin-2*app.gridshotR)
    cy = random.randint(app.margin+2*app.gridshotR,
    app.height-app.margin-2*app.gridshotR)
    dot = Dot(cx, cy, app.gridshotR)
    return dot

def gridshot_isOverlapping(app, newDot, dotsSet):
    cx, cy, r = newDot.cx, newDot.cy, app.gridshotR
    for dot in dotsSet:
        oldCx, oldCy = dot.cx, dot.cy
        if (cx > oldCx-r and cx < oldCx+r and cy > oldCy-r and cy < oldCy+r):
            return True
    return False

#Strafetrack
def strafetrack_redrawAll(app, canvas):
    if app.gameStarted == False:
        canvas.create_text(app.width//2, app.height//2, 
        text=f'{3 - app.timePast//1000}', font='Arial 36 bold')
    canvas.create_text(app.width//2, 30, 
    text=f'Score: {app.strafetrackScore.score}',font='Arial 28 bold')
    canvas.create_text(app.width//2, 60, text=f'{60 - app.gameTimePast//1000}')
    if app.gameStarted == True:
        cx, cy, r = app.strafetrackDot.cx, app.strafetrackDot.cy, 
        app.strafetrackDot.r
        canvas.create_oval(cx+r, cy+r, cx-r, cy-r, 
        fill=app.strafetrackDot.color)

def strafetrack_timerFired(app):
    pass

def strafetrack_mouseDragged(app, event):
    pass

def strafetrack_generateDot(app):
    cx = random.randint(app.margin+2*app.gridshotR, 
    app.width-app.margin-2*app.gridshotR)
    cy = random.randint(app.margin+2*app.gridshotR,
    app.height-app.margin-2*app.gridshotR)
    radius = random.randint(app.r, app.gridshotR)
    dot = Dot(cx, cy, radius)

#Sixshot
def sixshot_timerFired(app):
    app.timePast += app.timerDelay
    if app.timePast >= 3000:
        app.gameStarted = True
    if app.gameStarted == True:
        app.gameTimePast += app.timerDelay
        if app.gameTimePast >= 6000:
            app.oldMode = 'sixshot'
            app.mode = 'gameOver'
            app.paused = True

def sixshot_mousePressed(app, event):
    if app.gameStarted == True:
        currentDot = 1
        for dot in app.sixshotDotsSet:
            currentDot += 1
            cx, cy, r = dot.cx, dot.cy, app.r
            #if the mouse click is inside a dot
            if (event.x > cx-r and event.x < cx+r and event.y > cy-r 
            and event.y < cy+r):
                sixshot_dotClicked(app, dot)
                app.sixshotScore.increaseCombo()
                app.sixshotScore.incrementScore()
                print(app.sixshotScore.comboStreak)
                app.sixshotScore.score += app.sixshotScore.scoreIncrement
                app.sixshotHits += 1
                app.sixshotShots += 1
                break
            else:
                if currentDot == len(app.sixshotDotsSet):
                    app.sixshotScore.comboStreak = 0
                    print(app.sixshotScore.comboStreak)
                    app.sixshotScore.resetScoreIncrement()
                    app.sixshotShots += 1

def sixshot_keyPressed(app, event):
    if event.key == 'Escape':
        app.oldMode = app.mode
        app.mode = 'escapeMenu'

def sixshot_dotClicked(app, dot):
        app.sixshotDotsSet.remove(dot)
        newDot = sixshot_generateDot(app)
        dot.dotClicked()
        #prevent creating another instance of the dot that was just removed
        while sixshot_isOverlapping(app, newDot, app.sixshotDotsSet):
            newDot = sixshot_generateDot(app)
        app.sixshotDotsSet.add(newDot)

def sixshot_generateDot(app):
    cx = random.randint(app.margin+2*app.r,app.width-app.margin-2*app.r)
    cy = random.randint(app.margin+2*app.r,app.height-app.margin-2*app.r)
    dot = Dot(cx, cy, app.r)
    return dot

def sixshot_isOverlapping(app, newDot, dotsSet):
    cx, cy, r = newDot.cx, newDot.cy, app.r
    for dot in dotsSet:
        oldCx, oldCy = dot.cx, dot.cy
        if (cx > oldCx-r and cx < oldCx+r and cy > oldCy-r and cy < oldCy+r):
            return True
    return False

def sixshot_redrawAll(app, canvas):
    if app.gameStarted == False:
        canvas.create_text(app.width//2, app.height//2, 
        text=f'{3 - app.timePast//1000}', font='Arial 36 bold')
    canvas.create_text(app.width//2, 30, 
    text=f'Score: {app.sixshotScore.score}',font='Arial 28 bold')
    canvas.create_text(app.width//2, 60, text=f'{60 - app.gameTimePast//1000}')
    if app.gameStarted == True:
        for dot in app.sixshotDotsSet:
            cx, cy, r = dot.cx, dot.cy, app.r
            canvas.create_oval(cx+r, cy+r, cx-r, cy-r, 
            fill=app.exampleDot.color, width=0)

#Game over
def gameOver_redrawAll(app, canvas):
    if app.oldMode == 'sixshot':
        canvas.create_text(app.width//2,app.height//18,
            text = f'Your final score is: {app.sixshotScore.score}', 
            font = 'Arial 36 bold')
        canvas.create_text(app.width//2,3*app.height//4, 
        text= 
        f'Accuracy: {math.floor((app.sixshotHits/app.sixshotShots)*100)}%',
        font='Arial 36 bold')
    elif app.oldMode == 'gridshot':
        canvas.create_text(app.width//2,app.height//18,
            text = f'Your final score is: {app.gridshotScore.score}', 
            font = 'Arial 36 bold')
        canvas.create_text(app.width//2,3*app.height//4, 
        text= 
        f'Accuracy: {math.floor((app.gridshotHits/app.gridshotShots)*100)}%',
        font='Arial 36 bold')
    #create replay button dimensions
    replayButtonLeft = app.resumeButton.cx - app.resumeButton.length
    replayButtonRight = app.resumeButton.cx + app.resumeButton.length
    replayButtonTop = app.resumeButton.cy - app.resumeButton.height
    replayButtonBottom = app.resumeButton.cy + app.resumeButton.height
    #create home button dimensions
    homeButtonLeft = app.homeButton.cx - app.homeButton.length
    homeButtonRight = app.homeButton.cx + app.homeButton.length
    homeButtonTop = app.homeButton.cy - app.homeButton.height
    homeButtonBottom = app.homeButton.cy + app.homeButton.height
    #create the replay button
    canvas.create_rectangle(replayButtonLeft, replayButtonTop,
    replayButtonRight, replayButtonBottom, fill = app.resumeButton.color)
    canvas.create_text(app.resumeButton.cx, app.resumeButton.cy, 
    text = 'Replay', font = 'Arial 28 bold')
    #create the home button2
    canvas.create_rectangle(homeButtonLeft, homeButtonTop,
    homeButtonRight, homeButtonBottom, fill = app.homeButton.color)
    canvas.create_text(app.homeButton.cx, app.homeButton.cy,
    text = 'Home', font = 'Arial 28 bold')
    #when the user can play again
    if app.gameOverTime//1000 <= 1:
        canvas.create_text(app.width//2, app.height//10,
        text = f'You can play again in {1-app.gameOverTime//1000}')

def gameOver_mousePressed(app, event):
    if app.paused == False:
        if (event.x >= app.resumeButton.cx - app.resumeButton.length and
        event.x <= app.resumeButton.cx + app.resumeButton.length and
        event.y >= app.resumeButton.cy - app.resumeButton.height and
        event.y <= app.resumeButton.cy + app.resumeButton.height):
            app.mode = app.oldMode
            app.gameStarted = False
            app.timePast = 0
            app.gameTimePast = 0
            app.gameOverTime = 0
            if app.oldMode == 'gridshot':
                app.gridshotScore.resetToDefault()
                app.gridshotHits, app.gridshotShots = 0, 0
            elif app.oldMode == 'sixshot':
                app.sixshotScore.resetToDefault()
                app.sixshotHits, app.sixshotShots = 0, 0
        elif (event.x >= app.homeButton.cx - app.homeButton.length and
        event.x <= app.homeButton.cx + app.homeButton.length and
        event.y >= app.homeButton.cy - app.homeButton.height and
        event.y <= app.homeButton.cy + app.homeButton.height):
            appStarted(app)

def gameOver_timerFired(app):
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
    'you will not believe your eyes', 'I heckin love TenZ', 
    'Technoblade never dies']
    app.catchphrase = random.choice(app.catchphraseList)
    #Buttons
    app.gridshotButton = Button(app.width//2, app.height//3, app.width//4,
    app.height//16, "blue")
    app.strafetrackButton = Button(app.width//2, app.height//2, app.width//4,
    app.height//16, "blue")
    app.sixshotButton = Button(app.width//2, 2*app.height//3, app.width//4,
    app.height//16, "blue")
    app.resumeButton = Button(app.width//2, app.height//4, app.width//4,
    app.height//16, "blue")
    app.homeButton = Button(app.width//2, app.height//2, app.width//4,
    app.height//16, "blue")
    #Game dimensions
    app.margin = min(app.width, app.height)//8
    app.r = min(app.width, app.height)//80
    app.gridshotR = 4*app.r
    app.exampleDot = Dot(0,0,0)
    app.sixshotDotsSet = set()
    #gridshot
    app.gridshotScore = Score()
    app.gridshotDotsSet = set()
    app.gridshotHits = 0
    app.gridshotShots = 0
    while len(app.gridshotDotsSet) < 6:
        currentDot = gridshot_generateDot(app)
        while gridshot_isOverlapping(app, currentDot, app.gridshotDotsSet):
                currentDot = gridshot_generateDot(app)
        app.gridshotDotsSet.add(currentDot)
    #strafetrack
    app.strafetrackDot = strafetrack_generateDot(app)
    #sixshot
    app.sixshotScore = Score()
    app.timerDelay = 6
    app.timePast = 0
    app.gameTimePast = 0
    app.sixshotHits = 0
    app.sixshotShots = 0
    app.gameStarted = False
    while len(app.sixshotDotsSet) < 6:
        currentDot = sixshot_generateDot(app)
        while sixshot_isOverlapping(app, currentDot, app.sixshotDotsSet):
            currentDot = sixshot_generateDot(app)
        app.sixshotDotsSet.add(currentDot)
    #game over
    app.gameOverTime = 0

runApp(width=800,height=800)