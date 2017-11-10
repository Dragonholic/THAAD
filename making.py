
import math, sys
import pygame
from pygame.locals import *

pygame.init()

screen = pygame.display.set_mode((1024, 768), DOUBLEBUF)
#player = pygame.image.load("plane.png")
pygame.display.set_caption('THAAD')
font = pygame.font.Font("")


FPS = 60

class Character ():
    def __init__(self, image, loc):
        self.image = pygame.image.load(image)
        self.loc = loc


thaad = Character("plane.png", 100)

while True:
    screen.fill((255, 255, 255))

    events = pygame.event.get()
    for event in events:
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

 #       if pygame.key.get_pressed()[K_RIGHT]:


    screen.blit(thaad, (100.,100))

    pygame.display.flip()

    clock = pygame.time.Clock()
