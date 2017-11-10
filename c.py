import pygame
from pygame.locals import *
import random

print(random.randint(0, 5))

FPS = 60

# pygame을 초기화
pygame.init()
screen = pygame.display.set_mode((1280, 1024), FULLSCREEN)
clock = pygame.time.Clock()
image = pygame.image.load("images.jpg")
background = pygame.image.load("Desktop4_1280x1024.jpg")

font = pygame.font.Font("C:\Windows\Fonts\malgun.ttf", 32)
x = 0
y = 0
up_pressed = 0
down_pressed = 0
while True:
    # 1초당 60번 실행됨

    # 화면 칠하기
    screen.fill((255,255,255))
    screen.blit(background, (0,0))

    # ================ 이벤트 받기 ================
    events = pygame.event.get()
    for event in events:
        if event.type == QUIT:
            pygame.quit()
            exit()

    if pygame.key.get_pressed()[K_DOWN]:
        y = y + 10

    # ================ 그림 그리기 ================
    screen.blit(image, (x, y))

    text = font.render("안녕하세요", 1, (255, 255, 255))

    screen.blit(text, (10, 10))
    pygame.display.flip()

    # ================ 시간 맞추기 ================
    clock.tick(FPS)
    screen.blit(image, (x, y))

    text = font.render("안녕하세요", 1, (255, 255, 255))

    screen.blit(text, (10, 10))
    pygame.display.flip()

    # ================ 시간 맞추기 ================
    clock.tick(FPS)