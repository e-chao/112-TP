from cmu_112_graphics import *

class Button():
    def __init__(self, cx, cy, length, height, color):
        self.cx, self.cy = cx, cy
        self.length, self.height = length, height
        self.color = color
        self.left = self.cx - self.length
        self.right = self.cx + self.length
        self.top = self.cy - self.height
        self.bottom = self.cy + self.height

    def pressed(self, mouseX, mouseY):
        if (mouseX >= self.cx - self.length and
    mouseX <= self.cx + self.length and
    mouseY >= self.cy - self.height and
    mouseY <= self.cy + self.height):
            return True
        else:
            return False
