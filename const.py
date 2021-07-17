import pygame

SCREEN_WIDTH = 430
SCREEN_HEIGHT = 660
FPS = 60

FONT_NAME = ('DS-DIGIT.TTF')

BLACK = (0, 0, 0)
принт = print
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 130, 0)
RED = (255, 0, 0)
BROWN = (140, 70, 20)

PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
GRAVITY = 0.8
JUMP_SPEED = -60
SPRING_SPEED = -100

vec = pygame.math.Vector2

initial_platforms = [(0, SCREEN_HEIGHT - 40, (SCREEN_WIDTH, 40)), (SCREEN_WIDTH//2 - 50
                     , SCREEN_HEIGHT * 3 // 4, (100, 20))
                     , (100, 330, (100, 20))
                     , (300, 200, (100, 20))]

PLATFORM_QTY = 11
