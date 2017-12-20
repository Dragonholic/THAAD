import sys
import random
import math
import pygame
from pygame.locals import *


pygame.init()

screen = pygame.display.set_mode((1280, 1024), FULLSCREEN)
pygame.display.set_caption('THAAD')
clock = pygame.time.Clock()


FPS = 60
start = pygame.image.load('ktm.png')
background = pygame.image.load('back.jpg')


#게임 오브젝트 클래스
class GameObject(object):
    locx = 0
    locy = 0
    angle = 0
    image = None
    tick = 0

    def update(self, events):
        self.tick += 1
        self.do_update(events)

    def do_update(self, events):
        pass

    def draw(self, surface):
        rot_image = pygame.transform.rotate(self.image, self.angle / math.pi * 180)
        rect = rot_image.get_rect()
        rect.center = (self.locx, self.locy)

        surface.blit(rot_image, rect)



#메인캐릭터 클래스
class Character (GameObject):
    THAAD_MAIN = 'THAAD_MAIN.png'
    THAAD_TURN = 'thaad_turn.png'

    def __init__(self, locx, locy):
        self.main_image = pygame.image.load(self.THAAD_MAIN)
        self.turn_image = pygame.image.load(self.THAAD_TURN)

        resize_factor = 0.5

        mw, mh = self.main_image.get_size()
        self.main_image = pygame.transform.scale(self.main_image, (int(mw * resize_factor), int(mh * resize_factor)))

        tw, th = self.turn_image.get_size()
        self.turn_image = pygame.transform.scale(self.turn_image, (int(tw * resize_factor), int(th * resize_factor)))

        self.locx = locx
        self.locy = locy

        # Using radian
        self.angle = math.pi / 3

        self.tick = 0

    def draw(self, surface):
        surface.blit(self.main_image, (self.locx + 130, self.locy + 100))
        rot_image = pygame.transform.rotate(self.turn_image, self.angle / math.pi * 180)
        rect = rot_image.get_rect()
        rect.center = (self.locx + 140, self.locy + 240)

        surface.blit(rot_image, rect)

    def do_update(self, events):
        if pygame.key.get_pressed()[K_RIGHT]:
            self.locx += 10

        if pygame.key.get_pressed()[K_LEFT]:
            self.locx -= 10

        if pygame.key.get_pressed()[K_UP]:
            self.angle += math.pi / 90

        if pygame.key.get_pressed()[K_DOWN]:
            self.angle -= math.pi / 90

        if pygame.key.get_pressed()[K_SPACE] and self.tick % 10 == 0:
            fire_x = self.locx + 140 + math.cos(math.pi * 7 / 4 - self.angle) * 100
            fire_y = self.locy + 240 + math.sin(math.pi * 7 / 4 - self.angle) * 100
            spawn(Bullet(fire_x, fire_y, self.angle))

        # 0 < locx < 1280
        self.locx = max((-100, min((self.locx, 800))))

        # - pi / 6 < rotation < pi / 2
        self.angle = max((- math.pi / 6, min((self.angle, math.pi / 2))))




#적 미사일 클래스
class Enemy (GameObject):
    def __init__(self, image, locx, locy, angle):
        self.image = pygame.image.load(image)
        self.locx = locx
        self.locy = locy
        self.angle = angle
 #      self.alpha = alpha
        self.gravity = 0.5
#        self.image = image.set_alpha(1)

        resize_factor = 0.8

        mw, mh = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (int(mw * resize_factor), int(mh * resize_factor)))



        self.speed_x = math.cos(math.pi * 7 / 4 - self.angle) * 30
        self.speed_y = math.sin(math.pi * 7 / 4 - self.angle) * 30



    def do_update(self, events):
        self.locx -= self.speed_x
        self.locy += self.speed_y
        self.speed_y += self.gravity

        if self.locx > 1380 or self.locx < -100 or self.locy < -100 or self.locy > 1124:
            kill(self)


#사드 탄환 클래스
class Bullet (GameObject):
    def __init__(self, locx, locy, angle):
        self.locx = locx
        self.locy = locy
        self.angle = angle
        self.image = pygame.image.load("park.png")
        self.gravity = 0.4


        resize_factor = 0.4

        mw, mh = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (int(mw * resize_factor), int(mh * resize_factor)))


        self.speed_x = math.cos(math.pi * 7 / 4 - self.angle) * 30
        self.speed_y = math.sin(math.pi * 7 / 4 - self.angle) * 30


    def do_update(self, events):
        self.locx += self.speed_x
        self.locy += self.speed_y
        self.speed_y += self.gravity

        if self.locx > 1380 or self.locx < -100 or self.locy < -100 or self.locy > 1124:
            kill(self)



game_objects = []


#스폰 함수
def spawn(game_object):
    game_objects.append(game_object)
    return game_object

#제거 함수
def kill(game_object):
    game_objects.remove(game_object)
    return game_object


#사드 메인 캐릭터 스폰
thaad = spawn(Character(130, 720))



# 적 미사일 종류별 스폰 함수
def lv1():
    random_y = random.randrange(500,800)
    spawn(Enemy('lodong1.png', 1200, random_y, 0))

def lv2():
    random_y = random.randrange(500,800)
    spawn(Enemy('lodong2.png', 1200, random_y, 0))
def lv3():
    random_y = random.randrange(500,800)
    spawn(Enemy('lodong3.png', 1200, random_y, 0))
def lv4():
    random_y = random.randrange(500,800)
    spawn(Enemy('lodong4.png', 1200, random_y, 0))
def lv5():
    random_y = random.randrange(500,800)
    spawn(Enemy('lodong5.png', 1200, random_y, 0))


t=0
init = 0

#실행
while True:
    screen.fill((255, 255, 255))
    screen.blit(start, (0,0))



    if init == 1:
        screen.blit(background, (0, 0))



        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()



        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()


        for entity in game_objects:
            entity.update(events)
            entity.draw(screen)


        if t%30 == 0:
            lv1()

#게임 종료 버튼
        if 1230+50 > mouse[0] > 1230 and 0+50 > mouse[1] > 0 :
            pygame.draw.rect(screen, (255, 0, 0), (1230, 0, 50, 50))

            if click[0]:
                 pygame.quit()
                 sys.exit()
        else:
            pygame.draw.rect(screen, (155, 0, 0), (1230, 0, 50, 50))

        font = pygame.font.Font("arialbd.ttf", 40)
        text = font.render("X", True, (0,0,0), (1242,3))
        screen.blit(text,(1242,3))


    pygame.display.flip()
    t += 1
    clock.tick(FPS)

