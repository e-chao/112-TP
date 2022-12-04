from cmu_112_graphics import *

def appStarted(app):
    app.count = 0
    app.timerDelay = 5

def mousePressed(app, event):
    app.count += 1

def mouseReleased(app, event):
    app.count = 0

def redrawAll(app, canvas):
    canvas.create_text(app.width//2, app.height//2, text = f'{app.count}')

runApp(width = 1920, height = 1080)
