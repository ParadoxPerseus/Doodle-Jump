import random
from const import *


class Platform(pygame.sprite.Sprite):
    def __init__(self, image_list, x, y, size):
        super().__init__()
        platform_image = random.choice(image_list)
        self.image = pygame.transform.scale(platform_image, size)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.moving = False
        self.speed_x = 0
        self.speed_x = random.choice([-100, -5, -4, -3, -2, 2, 3, 4, 5, 100])

    def update(self, *args, **kwargs) -> None:
        if self.moving:
            self.rect.x += self.speed_x
            if self.rect.right >= SCREEN_WIDTH:
                self.speed_x = -self.speed_x
            if self.rect.left <= 0:
                self.speed_x = -self.speed_x

