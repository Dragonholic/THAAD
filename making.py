import sys
import random
import math
from functools import reduce
import pygame
from pygame.locals import *


pygame.init()
screen = pygame.display.set_mode((1280, 1024), DOUBLEBUF | FULLSCREEN)
pygame.display.set_caption('THAAD')
clock = pygame.time.Clock()


FPS = 60
start = pygame.image.load('ktm.png')
camo = pygame.image.load('camo.png')
warning_tape = pygame.image.load('warning_tape.png')
background = pygame.image.load('back.jpg')
city_img = pygame.image.load("usa.png")



game_seq = 0
gameover = 0

global gamescore
gamescore = 0

global city
city = 52


def get_axis(polygon):
    sides = []

    def get_side(p1, p2):
        angle = math.atan2(p1[0] - p2[0], p1[1] - p2[1])
        sides.append(angle)
        sides.append(angle + math.pi / 2)
        return p2

    reduce(get_side, polygon, polygon[-1])

    return sides


def collision(o1, o2):
    axes = get_axis(o1) + get_axis(o2)
    collides = True

    for axis in axes:

        def convert_axis(point):
            point_atan = math.atan2(point[0], point[1])

            return math.cos(axis - point_atan) * math.sqrt(point[0] ** 2 + point[1] ** 2)

        o1_points = list(map(convert_axis, o1))
        o2_points = list(map(convert_axis, o2))

        if not (min(o1_points) < max(o2_points) and min(o2_points) < max(o1_points)):
            collides = False

    return collides

#게임 오브젝트 클래스
class GameObject(object):
    locx = 0
    locy = 0
    angle = 0
    image = None
    tick = 0
    rect = pygame.Rect(0, 0, 0, 0)

    def update(self, events):
        self.tick += 1
        self.do_update(events)

    def do_update(self, events):
        pass

    def draw(self, surface):
        rot_image = pygame.transform.rotate(self.image, self.angle / math.pi * 180)
        rect = rot_image.get_rect()
        rect.center = (self.locx, self.locy)
        self.rect = rect

        surface.blit(rot_image, rect)

    def get_polygon(self):
        return self.rect.topleft, self.rect.bottomleft, self.rect.bottomright, self.rect.topright


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

        if pygame.key.get_pressed()[K_SPACE] and self.tick % 20 == 0:
            fire_x = self.locx + 140 + math.cos(math.pi * 7 / 4 - self.angle) * 100
            fire_y = self.locy + 240 + math.sin(math.pi * 7 / 4 - self.angle) * 100
            spawn(Bullet(fire_x, fire_y, self.angle))

        # 0 < locx < 1280
        self.locx = max((-100, min((self.locx, 800))))

        # - pi / 6 < rotation < pi / 2
        self.angle = max((- math.pi / 6, min((self.angle, math.pi / 2))))




#적 미사일 클래스


class Enemy (GameObject):
    images = [pygame.image.load('lodong%d.png' % (i + 1)) for i in range(6)]

    def __init__(self, image, locx, locy, angle):
        self.image = self.images[image]
        self.locx = locx
        self.locy = locy
        self.angle = angle
        self.gravity = 0.5


        resize_factor = 0.7





        mw, mh = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (int(mw * resize_factor), int(mh * resize_factor)))



        self.speed_x = math.cos(math.pi * 7 / 4 ) * 40
        self.speed_y = math.sin(math.pi * 7 / 4 ) * 30



    def do_update(self, events):
        self.locx -= self.speed_x
        self.locy += self.speed_y
        self.speed_y += self.gravity
        self.angle += math.pi * 1/120

        if self.locx > 1380 or self.locx < -100 or self.locy < -100 or self.locy > 1124:
            kill(self)
            global city
            city -= 1


#사드 탄환 클래스
class Bullet (GameObject):
    image = pygame.image.load("park.png")

    def __init__(self, locx, locy, angle):
        self.locx = locx
        self.locy = locy
        self.angle = angle
        self.gravity = 0.6
        self.ro_angle = 0

        resize_factor = 0.4

        mw, mh = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (int(mw * resize_factor), int(mh * resize_factor)))


        self.speed_x = math.cos(math.pi * 7 / 4 - self.angle) * 30
        self.speed_y = math.sin(math.pi * 7 / 4 - self.angle) * 35


    def do_update(self, events):
        self.locx += self.speed_x
        self.locy += self.speed_y
        self.speed_y += self.gravity
        self.angle += self.gravity

        if self.locx > 1380 or self.locx < -100 or self.locy < -100 or self.locy > 1124:
            kill(self)

#충돌 시 반응
        for enemy in game_objects:
            if isinstance(enemy, Enemy):
                if collision(enemy.get_polygon(), self.get_polygon()):
                    kill(enemy)
                    kill(self)
                    global gamescore
                    gamescore += 1000







game_objects = []


#스폰 함수
def spawn(game_object):
    game_objects.append(game_object)
    return game_object

#제거 함수
def kill(game_object):
    game_objects.remove(game_object)
    return game_object

#충돌 축 함수
def get_axis(polygon):
    sides = []

    def get_side(p1, p2):
        angle = math.atan2(p1[0] - p2[0], p1[1] - p2[1])
        sides.append(angle)
        sides.append(angle + math.pi / 2)
        return p2

    reduce(get_side, polygon, polygon[-1])

    return sides





# 적 미사일 종류별 스폰 함수
def lv1():
    random_y = random.randrange(500,800)
    spawn(Enemy(0, 1300, random_y, math.pi * 1/4))
def lv2():
    random_y = random.randrange(300, 600)
    spawn(Enemy(1, 1300, random_y, math.pi * 1/4))
def lv3():
    random_y = random.randrange(400, 700)
    spawn(Enemy(2, 1300, random_y, math.pi * 1/4))
def lv4():
    random_y = random.randrange(400, 800)
    spawn(Enemy(3, 1300, random_y, math.pi * 1/4))
def lv5():
    random_y = random.randrange(400, 800)
    spawn(Enemy(4, 1300, random_y, math.pi * 1/4))
def lv6():
    random_y = random.randrange(400, 800)
    spawn(Enemy(5, 1300, random_y, math.pi * 1/4))

t = 0
lv = 1
lv_list = [lv1, lv2, lv3, lv4, lv5, lv6]
t_list = [30, 50, 40, 35, 25, 45]
spawnready = 0

#폰트 리스트
font_list = [("arialbd.ttf"), ("NanumSquareB.ttf")]
fontsize_list = [40, 40]

font = pygame.font.Font(font_list[0], fontsize_list[0])
cityfont = pygame.font.Font(font_list[1], fontsize_list[1])
scorefont = pygame.font.Font(font_list[1], fontsize_list[1])
gamestarttext = pygame.font.Font(font_list[1], fontsize_list[1])
timerfont = pygame.font.Font(font_list[1], fontsize_list[1])

text = font.render("X", True, (0, 0, 0), (1242, 3))

mouse = pygame.mouse.get_pos()
click = pygame.mouse.get_pressed()

#실행
while True:
    screen.fill((255, 255, 255))

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    # 사드 메인 캐릭터 스폰
    if game_seq == 1 and spawnready == 0:
        thaad = spawn(Character(130, 720))
        spawnready += 1

#게임 순서별 실행

# 1.게임 시작 화면
    if game_seq == 0:
        screen.blit(warning_tape, (0, 0))
        screen.blit(warning_tape, (0, 886))
        screen.blit(start, (0, 150))
        screen.blit(camo, (550, 790))


        starttextrender = gamestarttext.render("작전 시작", True, (230,230,230), 0)
        screen.blit(starttextrender, (560, 800))

        if 550+180 > mouse[0] > 550 and 790 + 62 > mouse[1] > 790 :
            if click[0]:
                game_seq += 1


# 2. 메인 게임
    if game_seq == 1:
        screen.blit(background, (0, 0))
        screen.blit(city_img, (18, 48))






    #적 미사일 주기
        if t % t_list[0] == 0:
            lv_list[0]()

        if lv > 1 and t % t_list[1] == 0:
            lv_list[1]()

        if lv > 2 and t % t_list[2] == 0:
            lv_list[2]()

        if lv > 3 and t % t_list[3] == 0:
            lv_list[3]()

        if lv > 4 and t % t_list[4] == 0:
            lv_list[4]()

        if lv > 5 and t % t_list[5] == 0:
            lv_list[5]()

        if t % 600 == 0:
            lv += 1

        # 폰트 정의

        if gamescore < 10000 :
            scorerender = scorefont.render("세금 : " + str(gamescore) + "억", True, (0, 0, 0), (0, 0))
        else:
            scorerender = scorefont.render("세금 : " + str(gamescore//10000) + "조" + str(gamescore%10000) + "억", True, (0, 0, 0), (0, 0))



        #게임 오버
        if city == 0:
            pass


        #UI
        cityrender = cityfont.render("X " + str(city), True, (0,0,0), (100, 50))
        timerrender = timerfont.render(str(t/60) + "초", True, (0,0,0),0)


        #메인 게임 내 폰트 render
        screen.blit(scorerender, (0, 0))
        screen.blit(cityrender, (100, 50))
        screen.blit(timerrender, (1130, 100))


    events = pygame.event.get()
    for event in events:
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    for entity in game_objects:
        entity.update(events)
        entity.draw(screen)


    # 게임 종료 버튼
    if 1230 + 50 > mouse[0] > 1230 and 0 + 50 > mouse[1] > 0:
        pygame.draw.rect(screen, (255, 0, 0), (1230, 0, 50, 50))

        if click[0]:
            pygame.quit()
            sys.exit()
    else:
        pygame.draw.rect(screen, (155, 0, 0), (1230, 0, 50, 50))
        t += 1

    screen.blit(text, (1242, 3))


    pygame.display.flip()

    clock.tick(FPS)
