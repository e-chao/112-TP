import pygame

class InputRect():
    def __init__(self, cx, cy, width, height, button, text, textRect):
        self.rect = pygame.Rect(cx-width, cy-height, width, height)
        self.activity = False
        self.textColor = (255,255,255)
        self.button = button
        self.text = text
        self.textRect = textRect
        self.input = ''

    def backspace(self):
        self.input = self.input[:-1]

    def add(self, addition):
        self.input += addition

    def changeActivity(self):
        self.activity = not self.activity

    def getSurface(self, font):
        surface = font.render(self.input,False,(0,0,0))
        return surface

    def clearInput(self):
        self.input = ''