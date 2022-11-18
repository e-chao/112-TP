from cmu_112_graphics import *
import math, random
from dot import Dot
from score import Score

def appStarted(app):
    app.margin = min(app.width, app.height)//8
    app.r = min(app.width, app.height)//80
    app.exampleDot = Dot(0,0,0)
    app.dotsSet = set()
    app.sixshotScore = Score()
    app.timerDelay = 6
    app.timePast = 0
    app.gameTimePast = 0
    app.gameStarted = False
    app.gameOver = False
    while len(app.dotsSet) < 6:
        currentDot = generateDot(app)
        app.dotsSet.add(currentDot)

def timerFired(app):
    if app.gameOver == False:
        app.timePast += app.timerDelay
        if app.timePast >= 3000:
            app.gameStarted = True
    if app.gameStarted == True:
        app.gameTimePast += app.timerDelay
        if app.gameTimePast >= 60000:
            app.gameOver = True

def generateDot(app):
    cx = random.randint(app.margin,app.width-app.margin)
    cy = random.randint(app.margin,app.height-app.margin)
    dot = Dot(cx, cy, app.r)
    return dot

def mousePressed(app, event):
    if app.gameStarted == True:
        currentDot = 1
        for dot in app.dotsSet:
            currentDot += 1
            cx, cy, r = dot.cx, dot.cy, app.r
            #if the mouse click is inside a dot
            if (event.x > cx-r and event.x < cx+r and event.y > cy-r 
            and event.y < cy+r):
                dotClicked(app, dot)
                app.sixshotScore.increaseCombo()
                app.sixshotScore.incrementScore()
                print(app.sixshotScore.comboStreak)
                app.sixshotScore.score += app.sixshotScore.scoreIncrement
                break
            else:
                if currentDot == len(app.dotsSet):
                    app.sixshotScore.comboStreak = 0
                    print(app.sixshotScore.comboStreak)
                    app.sixshotScore.resetScoreIncrement()

def dotClicked(app, dot):
        app.dotsSet.remove(dot)
        newDot = generateDot(app)
        #prevent creating another instance of the dot that was just removed
        if isOverlapping(app, newDot, dot):
            newDot = generateDot(app)
        app.dotsSet.add(newDot)

def isOverlapping(app, newDot, oldDot):
    cx, cy, r = newDot.cx, newDot.cy, app.r
    if newDot == oldDot:
        return True
    for dot in app.dotsSet:
        oldCx, oldCy = dot.cx, dot.cy
        if (cx > oldCx-r and cx < oldCx+r and cy > oldCy-r and cy < oldCy+r):
            return True
    return False
            
def redrawAll(app, canvas):
    if app.gameStarted == False:
        canvas.create_text(app.width//2, app.height//2, 
        text=f'{3 - app.timePast//1000}', font='Arial 36 bold')
    canvas.create_text(app.width//2, 30, 
    text=f'Score: {app.sixshotScore.score}',font='Arial 28 bold')
    canvas.create_text(app.width//2, 60, text=f'{60 - app.gameTimePast//1000}')
    for dot in app.dotsSet:
        cx, cy, r = dot.cx, dot.cy, app.r
        canvas.create_oval(cx+r, cy+r, cx-r, cy-r, fill=app.exampleDot.color, 
        width=0)
    if app.gameOver:
        canvas.create_rectangle(0,0,app.width,app.height,fill='white')
        canvas.create_text(app.width//2,app.height//2,
        text = f'Your final score is: {app.sixshotScore.score}', 
        font = 'Arial 36 bold')

runApp(width=800,height=800)