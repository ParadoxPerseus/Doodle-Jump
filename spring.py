import random
from const import *


class Spring(pygame.sprite.Sprite):
    def __init__(self, x, y, width):
        super().__init__()
        img = pygame.image.load('PNG//Items//spring.png')
        img = pygame.transform.scale(img, (40, 20)).convert_alpha()
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.x = random.randint(x, x + width - self.rect.width)

    def worked(self):
        img = pygame.image.load('PNG//Items//spring_in.png')
        img = pygame.transform.scale(img, (40, 29)).convert_alpha()
        self.image = img
        self.rect = self.image.get_rect()
        pygame.time.delay(100)
        img = pygame.image.load('PNG//Items//spring_out.png')
        img = pygame.transform.scale(img, (40, 13)).convert_alpha()
        self.image = img
        self.rect = self.image.get_rect()
        # pygame.time.delay(200)
