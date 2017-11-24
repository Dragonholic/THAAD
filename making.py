
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
    def __init__(self, image, locx, locy, angle):
        self.image = pygame.image.load(image)
        w, h = self.image.get_size();
        resizefactor = 0.5
        self.image = pygame.transform.scale(self.image, (int(w*resizefactor), int(h*resizefactor)))
        self.locx = locx
        self.locy = locy
        self.angle = angle

    def launch(self):
        pass

    def transform_angle(self, number):
            self.angle = self.angle + number
            self.image = pygame.transform.rotate(self.image, self.angle)




class Enemy ():
    def __init__(self, image, locx, locy, angle):
        self.image = pygame.image.load(image)
        self.locx = locx
        self.locy = locy
        self.angle = angle


    def transform_angle(self):
            self.angle = self.angle + 1
            self.image = pygame.transform.rotate(self.image, self.angle)




thaad_m = Character('THAAD_MAIN.png', 130, 600, 0)
thaad_a = Character('THAAD_A.png', 0, 590, 0)

def rot_center(image , angle):
#    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()

    rot_image = pygame.transform.rotate(image, angle)
    #thaad_a.image = rot_image

    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()



#rotated = pygame.transform.rotate(thaad_a.image, thaad_a.angle)
#rect = rotated.get_rect()
#rect.center = (rot_center)

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
        thaad_m.locx = thaad_m.locx + 10
        thaad_a.locx = thaad_a.locx + 10

    if pygame.key.get_pressed()[K_LEFT]:
        thaad_m.locx = thaad_m.locx - 10
        thaad_a.locx = thaad_a.locx - 10

    if pygame.key.get_pressed()[K_UP]:
        rot_center(thaad_a, math.pi//60)

    if pygame.key.get_pressed()[K_DOWN]:
        rot_center(thaad_a, - math.pi//60)


    screen.blit(thaad_m.image, (thaad_m.locx,thaad_m.locy))
    screen.blit(thaad_a.image, (thaad_a.locx, thaad_a.locy))
    screen.blit(lv1.image, (lv1.locx, lv1.locy))


    pygame.display.flip()
    clock.tick(FPS)

