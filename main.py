import sys
import os

import pygame

from bullet import Bullet
from spring import Spring
from const import *
import random
from platform import Platform
from player import Player


def AutoFire(boo=True):
    if boo:
        bullet = Bullet(game.player.rect.centerx, game.player.rect.top)
        game.bullets.add(bullet)
        game.all_sprites.add(bullet)


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = FONT_NAME
        self.all_sprites = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.player = Player(self)
        self.score = 0
        self.bullet = Bullet(self.player.rect.x, self.player.rect.y)
        self.bullets.add(self.bullet)
        self.springs = pygame.sprite.Group()
        self.all_sprites.add(self.bullet)
        self.all_sprites.add(self.player)
        self.create_platform()
        self.platforms = pygame.sprite.Group()
        self.playing = True
        self.pause = False

        for plat_param in initial_platforms:
            platform1 = Platform(self.platform_image_list, *plat_param)
            self.platforms.add(platform1)
            self.all_sprites.add(platform1)

        self.high_score = 0
        self.load_high_score()

    def load_high_score(self):
        self.folder = os.path.dirname(__file__)
        with open(os.path.join(self.folder, 'high.txt'), 'r') as file:
            try:
                self.high_score = int(file.read())
            except:
                self.high_score = 0

    def AutoScore(self, boo=True):
        if boo:
            self.score += 10

    def create_platform(self):
        platform_file_list = ['ground_grass.png', 'ground_sand.png', 'ground_snow.png', 'ground_stone.png',
                              'ground_cake.png']
        self.platform_image_list = []
        for file_name in platform_file_list:
            img = pygame.image.load('PNG\\Environment\\' + file_name).convert()
            img.set_colorkey(BLACK)
            self.platform_image_list.append(img)

    def draw_text(self, text, size, x, y):
        font = pygame.font.Font('DS-DIGIT.TTF', size)
        text_surf = font.render(text, True, YELLOW)
        text_rect = text_surf.get_rect()
        text_rect.centerx = x
        text_rect.top = y
        self.screen.blit(text_surf, text_rect)

    def intro(self):
        # text = pygame.font.Font('DS-DIGIT.TTF', 45)
        self.draw_text('Doodle Jump', 45, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 5)
        self.draw_text('press <-, -> to move', 45,  SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)
        self.draw_text('your Doodler', 45,  SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
        self.draw_text('Good Luck', 45, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        pygame.display.update()
        wait = True
        while wait:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYUP:
                    wait = False

    def run(self, boo=True):
        if boo:
            self.bg = pygame.image.load('PNG//Background//purple.png')
            self.bg_rect = self.bg.get_rect()
            self.screen.blit(self.bg, self.bg_rect)
            self.intro()
            while self.playing:
                self.clock.tick(FPS)
                self.check_events()
                self.update()
                self.draw()
                key = pygame.key.get_pressed()
                if key[pygame.K_RSHIFT]:
                    AutoFire(True)
                if key[pygame.K_RSHIFT]:
                    AutoFire(False)
                if key[pygame.K_a]:
                    self.AutoScore(True)
                if key[pygame.K_a]:
                    self.AutoScore(False)
    def draw_score(self):
        # global score
        self.text = pygame.font.Font('DS-DIGIT.TTF', 32)
        text_score = str(self.score)
        text_score_render = self.text.render('SCORE:' + text_score, True, YELLOW)
        self.screen.blit(text_score_render, (0, 0))

    def outro(self):
        self.screen.fill(RED)
        # text = pygame.font.Font('DS-DIGIT.TTF', 45)
        self.draw_text('game over!', 45, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 5)
        self.draw_text('press key to escape', 45,  SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)
        if self.score > self.high_score:
            self.draw_text('high score:' + str(self.score), 22, SCREEN_WIDTH // 2, 20)
            with open(os.path.join(self.folder, 'high.txt'), 'w') as file:
                file.write(str(self.score))

        pygame.display.update()
        wait = True
        while wait:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            key = pygame.key.get_pressed()
            if key[pygame.K_e]:
                wait = False

    # цикл обработки событий
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.bullet = Bullet(self.player.rect.centerx, self.player.rect.top)
                self.bullets.add(self.bullet)
                self.all_sprites.add(self.bullet)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_q:
                    self.pause = not self.pause

    # изменение объектов
    def update(self):
        self.all_sprites.update()
        if self.player.speed.y > 0:
            player_hit_platforms = pygame.sprite.spritecollide(self.player, self.platforms, False)
            if player_hit_platforms:
                self.player.speed.y = 0
                self.player.pos.y = player_hit_platforms[0].rect.top
            player_hit_platforms_and_spring = pygame.sprite.spritecollide(self.player, self.springs, False)
            for hit in player_hit_platforms_and_spring:
                hit.worked()
                self.player.speed.y = SPRING_SPEED
        if self.player.rect.top <= SCREEN_HEIGHT // 4:
            self.player.pos.y += abs(self.player.speed.y)
            for sprite in self.all_sprites:
                sprite.rect.y += abs(self.player.speed.y)
                if isinstance(sprite, Platform) and sprite.rect.top >= SCREEN_HEIGHT:
                    sprite.kill()
                    self.score += 10
        while len(self.platforms) < PLATFORM_QTY:
            width = random.randint(40, 100)
            height = 20
            x = random.randint(0, SCREEN_WIDTH - width)
            y = random.randint(-100, 0)
            platform = Platform(self.platform_image_list, x, y, (width, height))
            if random.random() > 0.8:
                platform.moving = True
            self.all_sprites.add(platform)
            self.platforms.add(platform)
            if random.random() > 0.8 and not platform.moving:
                spring = Spring(platform.rect.x, platform.rect.top, platform.rect.width)
                self.all_sprites.add(spring)
                self.springs.add(spring)

    # обновление экрана

    def draw(self):
        if self.pause:
            self.draw_text('PAUSE', 48, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        else:
            bg = pygame.image.load('PNG//Background//purple.png')
            bg_rect = self.bg.get_rect()
            self.screen.blit(bg, bg_rect)
            self.all_sprites.draw(self.screen)
            self.draw_score()
        pygame.display.flip()


game = Game()
game.run()
