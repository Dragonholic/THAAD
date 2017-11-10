import math, sys
import pygame
from pygame.locals import *

pygame.init()

screen = pygame.display.set_mode((1024, 768), DOUBLEBUF)
#player = pygame.image.load("plane.png")
pygame.display.set_caption('AIRPLANE')


FPS = 60


class Sprite(pygame.sprite.Sprite):
    def __init__(self, image, position):
        pygame.sprite.Sprite.__init__(self)
        self.user_src_image = pygame.image.load(image)
        self.user_position = position
#        self.user_rotation = 30
#        self.user_speed = 0
#        self.user_rotation_speed = 0

    def update(self, deltat):
        # 속도, 회전 속도에 따라 위치 정보를 업데이트한다
#        self.user_rotation += self.user_rotation_speed
        x, y = self.user_position
#        rad = self.user_rotation * math.pi / 180
#        x += -self.user_speed * math.sin(rad)
#        y += -self.user_speed * math.cos(rad)
        self.user_position = (x, y)

        self.image = pygame.transform.rotate(self.user_src_image)
        self.rect = self.image.get_rect()
        self.rect.center = self.user_position

rect = screen.get_rect()
simple = Sprite('plane.png', rect.center)
simple_group = pygame.sprite.RenderPlain(simple)


while True:
    screen.fill((255, 255, 255))

    events = pygame.event.get()
    for event in events:
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    if hasattr(event, 'key'):
        down = event.type == KEYDOWN
        if event.key == K_RIGHT:
            simple.user_rotation_speed = down * -5  # 시계 방향이 마이너스인 것에 유의
        elif event.key == K_LEFT:
            simple.user_rotation_speed = down * 5
        elif event.key == K_UP:
            simple.user_speed = down * 10
        elif event.key == K_DOWN:
            simple.user_speed = down * -10

#    screen.blit(player, (100, 100))
#    rotated = pygame.transform.rotate(player, rect.center)
#    rect = rotated.get_rect()
#    rect.center = (x, y)

    pygame.display.flip()

    clock = pygame.time.Clock()


clock.tick(FPS)