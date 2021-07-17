import sys

import pygame
from const import *


class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        player_image = pygame.image.load("PNG\\Players\\bunny1_stand.png").convert()
        player_image.set_colorkey(BLACK)
        self.image = pygame.transform.scale(player_image, (40, 67))
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.pos = vec(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.speed = vec(0, 0)
        self.acc = vec(0, 0)

    def jump(self):
        self.rect.y += 1
        hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 1
        if hits:
            self.game.score += 1
            self.speed.y = JUMP_SPEED

    def update(self):
        self.acc = (0, GRAVITY)
        key_state = pygame.key.get_pressed()
        if key_state[pygame.K_LEFT]:
            self.acc = (-PLAYER_ACC, GRAVITY)
        if key_state[pygame.K_RIGHT]:
            self.acc = (PLAYER_ACC, GRAVITY)
        if key_state[pygame.K_SPACE]:
            self.jump()

        # применяем трение
        self.acc += self.speed * PLAYER_FRICTION
        # меняем скорость
        self.speed += self.acc
        # меняем положение
        self.pos += self.speed + 0.5*self.acc
        # контроль границ
        if self.pos.x < 0:
            self.pos.x = SCREEN_WIDTH
        if self.pos.x > SCREEN_WIDTH:
            self.pos.x = 0

        self.rect.midbottom = self.pos
        if self.rect.bottom > SCREEN_HEIGHT:
            self.kill()
            self.game.playing = False
            self.game.outro()
