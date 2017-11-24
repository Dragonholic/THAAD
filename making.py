
import sys, threading, math
import pygame
from pygame.locals import *

pygame.init()

screen = pygame.display.set_mode((1280, 1024), DOUBLEBUF)
pygame.display.set_caption('THAAD')
clock = pygame.time.Clock()

FPS = 60
background = pygame.image.load('back.jpg')


class Character ():
    def __init__(self, image, locx, locy):
        self.image = pygame.image.load(image)
        self.locx = locx
        self.locy = locy

    def launch(self):
        pass

class Enemy ():
    def __init__(self, image, locx, locy, angle):
        self.image = pygame.image.load(image)
        self.locx = locx
        self.locy = locy
        self.angle = angle


    def transform_angle(self):
        while True:
            self.angle = self.angle + 0.1
            self.image = pygame.transform.rotate(self.image, self.angle)
             9j 0



thaad = Character('THAAD.jpg', 100, 500)
lv1 = Enemy('plane.png', 900, 200, 0)





while True:
    screen.fill((255, 255, 255))
    screen.blit(background,(0,0))


    events = pygame.event.get()
    for event in events:
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    if pygame.key.get_pressed()[K_RIGHT]:
        thaad.locx = thaad.locx + 10

    if pygame.key.get_pressed()[K_LEFT]:
        thaad.locx = thaad.locx - 10




    screen.blit(thaad.image, (thaad.locx,thaad.locy))
    screen.blit(lv1.image, (lv1.locx, lv1.locy))


    pygame.display.flip()
    clock.tick(FPS)

