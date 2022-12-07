import pygame

class Button():
    def __init__(self, cx, cy, length, height, color):
        pygame.init()
        self.cx, self.cy = cx, cy
        self.length, self.height = length, height
        self.color = color
        self.left = self.cx - self.length/2
        self.right = self.left + self.length
        self.top = self.cy - self.height/2
        self.bottom = self.top + self.height
        self.rect = pygame.Surface((self.length,self.height))
        self.rect.fill(self.color)
        self.storedRect = self.rect.get_rect()

    def pressed(self):
        if (pygame.mouse.get_pos()[0] >= self.left and 
        pygame.mouse.get_pos()[0] <= self.right and
        pygame.mouse.get_pos()[1] >= self.top and
        pygame.mouse.get_pos()[1] <= self.bottom):
            return True
        else:
            return False
