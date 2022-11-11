import pygame
from add_on import import_folder


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.character_assets()
        self.frame_index = 0  # used to pick out one of the anim frames
        self.anim_speed = 0.06
        self.image = self.anims['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)

        # player movement
        self.direction = pygame.math.Vector2(0, 0)  # movement is all in one neat variable :)
        self.speed = 8
        self.gravity = 0.8
        self.jump_speed = -16

    def character_assets(self):  # Allows us to access the path to character assets sheet
        path_to_char_folder = 'Character_assets/'
        self.anims = {'idle': [], 'jump': [], 'run': []}  # using a dictionary to easily access the folder we want

        for animations in self.anims.keys():
            complete_path = path_to_char_folder + animations    # the animations is one of the lists in the dictionary
            # which we attach to the back of the file path
            self.anims[animations] = import_folder(complete_path)  # to get the animation we want to work on

    def animate(self):
        current_anim = self.anims['idle']

        self.frame_index += self.anim_speed
        if self.frame_index >= len(current_anim):  # once frame index is greater than the number of items in the list
            self.frame_index = 0

        self.image = current_anim[int(self.frame_index)]

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
        self.animate()
        self.activate_gravity()

