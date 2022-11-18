import pygame


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.frame_index = 0
        # used to pick out one of the anim frames (in this class used for the animation of the enemy)
        self.anim_speed = 0.07

        width = 30
        height = 30
        self.image = pygame.Surface([width, height])
        self.image.fill('blue')

        # Set a reference to the image rect.
        self.rect = self.image.get_rect()
        self.rect.topleft = pos



