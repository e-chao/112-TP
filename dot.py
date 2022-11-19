#from sound import Sound
from cmu_112_graphics import *
#import pygame

class Dot(object):
    def __init__(self, cx, cy, r):
        #sound code taken from 112 notes
        #pygame.mixer.init()
        #self.dotClickedSound = Sound("dotClicked.mp3")
        self.radius = r
        self.cx, self.cy = cx, cy
        self.color = "blue"
        self.health = 3

    def dotClicked(self):
        #self.dotClickedSound.start()
        pass

    def getHashables(self):
        return (self.cx, self.cy)
    
    def __hash__(self):
        return hash(self.getHashables())

    def __eq__(self, other):
        return ((self.cx == other.cx) and (self.cy == other.cy) 
        and isinstance((other, Dot)))
