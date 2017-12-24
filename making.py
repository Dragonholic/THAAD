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
title = pygame.image.load("title.png")
button = pygame.image.load('button.png')
warning_tape = pygame.image.load('warning_tape.png')
background = pygame.image.load('back.jpg')
city_img = pygame.image.load("usa.png")
gameover = pygame.image.load("kim.png")
img_explosion = pygame.image.load('explosion.png')

mw, mh = button.get_size()
button = pygame.transform.scale(button, (int(mw * 0.72), int(mh * 0.5)))

mw, mh = gameover.get_size()
gameover = pygame.transform.scale(gameover, (int(mw * 1.01), int(mh * 1.01)))

game_seq = 0
dest_text_lim = 0
printscore = 0

global dest
dest = 0

global gamescore
gamescore = 0

global city
city = 52

global explosion
explosion = []



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
        self.gravity = 0.6


        resize_factor = 0.7





        mw, mh = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (int(mw * resize_factor), int(mh * resize_factor)))



        self.speed_x = math.cos(math.pi * 7 / 4 ) * 40
        self.speed_y = math.sin(math.pi * 7 / 4 ) * 30




    def do_update(self, events):
        self.locx -= self.speed_x
        self.locy += self.speed_y
        self.speed_y += self.gravity
        self.angle += math.pi * 1/150

        if self.locx > 1380 or self.locx < -100 or self.locy < -100 or self.locy > 1124:
            kill(self)
            global city
            city -= 1
            global dest
            dest += 1


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
    if game_object in game_objects:
        game_objects.remove(game_object)
        explosion.append([game_object.locx, game_object.locy, 0])
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
endt = 0
lv = 1
lv_list = [lv1, lv2, lv3, lv4, lv5, lv6]
t_list = [30, 50, 40, 35, 25, 45]
city_list = ["워싱턴 D.C.","알라바마 주 Alabama","알래스카 주 Alaska","아리조나 주 Arizona","아칸사스 주 Arkansas","캘리포니아 주 California","콜로라도 주 Colorado","코넷티컷 주 Connecticut","델라웨어 주 Delaware","플로리다 주 Florida" ,"조지아 주 Georgia","하와이 주 Hawaii" ,"아이다호 주 Idaho" ,"일리노이 주 Illinois" ,"인디아나 주 Indiana" ,"아이오와 주 Iowa" ,"캔사스 주 Kansas","켄터키 주 Kentucky" ,"루지아나 주 Louisiana" ,"메인 주 Maine" ,"메릴랜드 주 Maryland","메사추세스 주 Massachusetts" ,"미시건 주 Michigan" ,"미네소타 주 Minnesota" ,"미시시피 주 Mississippi" ,"미주리 주 Missouri" ,"몬타나 주 Montana" ,"네브라스카 주 Nebraska" ,"네바다 주 Nevada" ,"뉴 헹프셔 주 New Hampshire" ,"뉴 저지 주 New Jersey","뉴 멕시코 주 New Mexico" ,"뉴욕 주 New York" ,"노스 캐롤라이나 주 North Carolina" ,"노스 다코타 주 North Dakota" ,"오하이오 주 Ohio" ,"오클라호마 주 Oklahoma" ,"오레곤 주 Oregon","펜실베니아 주 Pennsylvania" ,"로드 아일랜드 주 Rhode Island" ,"사우스 캐롤라이나 주 South Carolina" ,"사우스 다코타 주 South Dakota" ,"테네시 주 Tennesee" ,"텍사스 주 Texas" ,"유타 주 Utah" ,"버몬트 주 Vermont" ,"버지니아 주 Virginia" ,"워싱턴 주 Washington" ,"웨스트 버지니아 주 West Virginia" ,"위스콘신 주 Wisconsin" ,"와이오밍 주 Wyoming", "남한 South Korea"]
spawnready = 0

#폰트 리스트
font_list = [("arialbd.ttf"), ("NanumSquareB.ttf")]
fontsize_list = [40, 40, 20, 30]

font = pygame.font.Font(font_list[0], fontsize_list[0])
cityfont = pygame.font.Font(font_list[1], fontsize_list[1])
scorefont = pygame.font.Font(font_list[1], fontsize_list[1])
gamestarttext = pygame.font.Font(font_list[1], fontsize_list[1])
timerfont = pygame.font.Font(font_list[1], fontsize_list[1])
dest_text = pygame.font.Font(font_list[1], fontsize_list[2])
gameovertext = pygame.font.Font(font_list[1], fontsize_list[3])


text = font.render("X", True, (0, 0, 0), (1242, 3))
starttextrender = gamestarttext.render("작전 시작", True, (230, 230, 230), 0)

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


    if city < 0 :
        city = 0

#게임 순서별 실행

# 1.게임 시작 화면
    if game_seq == 0:
        screen.blit(warning_tape, (0, 0))
        screen.blit(warning_tape, (0, 886))
        screen.blit(start, (0, 150))
        screen.blit(button, (550, 790))
        screen.blit(title, (360, 150))


        screen.blit(starttextrender, (560, 800))

        if 550+180 > mouse[0] > 550 and 790 + 62 > mouse[1] > 790 :
            starttextrender = gamestarttext.render("작전 시작", True, (230, 230, 30), 0)

            if click[0]:
                game_seq += 1
        else:
            starttextrender = gamestarttext.render("작전 시작", True, (230, 230, 230), 0)

# 2. 메인 게임
    if game_seq == 1:
        screen.blit(background, (0, 0))
        screen.blit(city_img, (18, 108))






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

        if t > 100 and t % 600 == 0:
            lv += 1

        if endt == 1 :
            kill(thaad)
            spawnready -= 1

            pygame.time.wait(1000)

            game_seq += 1


        if city == 0 and endt == 0:
            dest_textrender = dest_text.render(city_list[dest - 1] + "이 파괴되었습니다.", True, (0, 0, 0,), 0)
            screen.blit(dest_textrender, (0, 160))

            endt += 1

        if dest > 0 and endt == 0:
                if dest == 1:
                    dest_textrender = dest_text.render("도시 " + city_list[dest - 1] + "가 파괴되었습니다.", True, (0, 0, 0,), 0)
                    screen.blit(dest_textrender, (0, 160))
                if 52 > dest > 1:
                    dest_textrender = dest_text.render("%s번째 주 : " % (dest - 1) + city_list[dest - 1] + "가 파괴되었습니다.",
                                                       True, (0, 0, 0,), 0)
                    screen.blit(dest_textrender, (0, 160))

                    #            if dest == 52:
                    #                dest_textrender = dest_text.render(city_list[dest - 1] + "이 파괴되었습니다.", True, (0, 0, 0,), 0)
                    #                screen.blit(dest_textrender, (0, 160))


        # 폰트 정의
        if gamescore < 10000 :
            scorerender = scorefont.render("세금 : " + str(gamescore) + "억", True, (0, 0, 0), (0, 0))
        else:
            scorerender = scorefont.render("세금 : " + str(gamescore//10000) + "조" + str(gamescore%10000) + "억", True, (0, 0, 0), (0, 0))




        #UI
        cityrender = cityfont.render("X " + str(city), True, (0,0,0), (100, 50))
        timerrender = timerfont.render(str(int(t/60)) + "초", True, (0,0,0),0)


        #메인 게임 내 폰트 render
        screen.blit(scorerender, (0, 60))
        screen.blit(cityrender, (100, 110))
        screen.blit(timerrender, (1190, 60))

        t += 1

        if gamescore < 10000 :
            scorerender_result = scorefont.render("총 세금 : " + str(gamescore) + "억", True, (230, 230, 230), (0, 0))
        else:
            scorerender_result = scorefont.render("총 세금 : " + str(gamescore//10000) + "조" + str(gamescore%10000) + "억", True, (230, 230, 230), (0, 0))


    #게임 오버
    if game_seq == 2:
        screen.blit(gameover, (0,0))
        screen.blit(scorerender_result, (500, 850))

        if printscore == 0:
            print("kakin:do-method:score:%d" % (gamescore))
            printscore = 1

        gameoverrender = gameovertext.render("처음으로 돌아가기", True, (230, 230, 230), 0)
        screen.blit(gameoverrender, (530, 900))
        gamescore = 0
        city = 52
        t = 0
        endt = 0
        dest = 0
        lv = 1


        if 530 + 270 > mouse[0] > 530 and 900 + 30 > mouse[1] > 900 and click[0]:
            game_seq = 0
            printscore = 0


    events = pygame.event.get()
    for event in events:
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    for entity in game_objects:
        entity.update(events)
        entity.draw(screen)

    w, h = img_explosion.get_size()
    for i, ex in enumerate(explosion):
        ex[2] += 0.05
        img = pygame.transform.scale(img_explosion, (int(w * ex[2]), int(h * ex[2])))

        screen.blit(img, (ex[0], ex[1]))

        if ex[2] > 1:
            explosion.pop(i)



    # 게임 종료 버튼
    if 1230 + 50 > mouse[0] > 1230 and 0 + 50 > mouse[1] > 0:
        pygame.draw.rect(screen, (255, 0, 0), (1230, 0, 50, 50))

    else:
        pygame.draw.rect(screen, (155, 0, 0), (1230, 0, 50, 50))



    if 1230 + 50 > mouse[0] > 1230 and 0 + 50 > mouse[1] > 0 and click[0]:
        pygame.quit()
        sys.exit()



    screen.blit(text, (1242, 3))


    pygame.display.flip()

    clock.tick(FPS)

