import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((32, 64))
        self.image.fill('#33adff')
        self.rect = self.image.get_rect(topleft=pos)

        # player movement
        self.direction = pygame.math.Vector2(0, 0)  # movement is all in one neat variable :)
        self.speed = 8
        self.gravity = 0.8
        self.jump_speed = -16

    def character_assets(self):  # Allows us to access the path to character assets sheet
        path_to_char_folder = 'Character_assets/character_sheet.png'

    def get_input(self):  # to get all the keys the player presses
        key_press = pygame.key.get_pressed()

        if key_press[pygame.K_d]:  # right
            self.direction.x = 1
        elif key_press[pygame.K_a]:  # left
            self.direction.x = -1
        else:  # no movement
            self.direction.x = 0

        if key_press[pygame.K_SPACE]:  # to jump
            self.jump()

    def jump(self):
        self.direction.y = self.jump_speed

    def activate_gravity(self):
        self.direction.y += self.gravity  # this is so gravity increases on each frame
        self.rect.y += self.direction.y  # affects the player sprite here

    def update(self):  # used to control sprite behaviour
        self.get_input()
        self.activate_gravity()

