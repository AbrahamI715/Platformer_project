import pygame


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, enemies_group: pygame.sprite.Group):
        super().__init__(enemies_group)

        width = 30
        height = 60
        self.image = pygame.Surface([width, height])
        self.image.fill('red')

        # Set a reference to the image rect.
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

    #def update(self, x_shift):
        #self.rect.x += x_shift

