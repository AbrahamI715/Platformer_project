import pygame
from add_on import import_folder


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.character_assets()
        self.frame_index = 0  # used to pick out one of the anim frames
        self.anim_speed = 0.07
        self.image = self.anims['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.collision_rect = pygame.Rect(0, 0, 40, 64)
        self.collision_rect.midbottom = self.rect.midbottom

        # player movement
        self.direction = pygame.math.Vector2(0, 0)  # movement is all in one neat variable :)
        self.speed = 8
        self.gravity = 0.6
        self.jump_speed = -15

        self.player_status = 'idle'  # the player animation starting point with no inputs
        self.ceiling = False
        self.ground = False
        self.left = False
        self.right = False
        self.flip = False

    def character_assets(self):  # Allows us to access the path to character assets sheet
        path_to_char_folder = 'Character_assets/'
        self.anims = {'idle': [], 'jump': [], 'run': [], 'fall': []}  # using a dictionary to easily access the folder we want

        for animations in self.anims.keys():
            complete_path = path_to_char_folder + animations    # the animations is one of the lists in the dictionary
            # which we attach to the back of the file path
            self.anims[animations] = import_folder(complete_path)  # to get the animation we want to work on

    def animate(self):
        current_anim = self.anims[self.player_status]

        self.frame_index += self.anim_speed
        if self.frame_index >= len(current_anim):  # once frame index is greater than the number of items in the list
            self.frame_index = 0

        image = current_anim[int(self.frame_index)]  # setting image to be a local variable
        if self.flip == False:
            self.image = image
        elif self.flip == True:
            self.image = pygame.transform.flip(image, True, False)

        # if self.ground:
        #     self.collision_rect = self.image.get_rect(midbottom=self.collision_rect.midbottom)
        # elif self.ceiling:
        #     self.collision_rect = self.image.get_rect(midtop=self.collision_rect.midtop)
        # else:
        #     self.collision_rect = self.image.get_rect(center=self.collision_rect.center)

        self.rect.midbottom = self.collision_rect.midbottom


    def get_input(self):  # to get all the keys the player presses
        key_press = pygame.key.get_pressed()

        if key_press[pygame.K_d]:  # right
            self.direction.x = 1
            self.flip = False
        elif key_press[pygame.K_a]:  # left
            self.direction.x = -1
            self.flip = True
        else:  # no movement
            self.direction.x = 0

        if key_press[pygame.K_SPACE] and self.direction.y == 0:  # to jump
            self.jump()

    def get_player_status(self):  # will check the current status of the player then set the animation appropriately
        if self.direction.y < 0:  # if player jumping
            self.player_status = 'jump'
        elif self.direction.y > 1:  # player is falling
            self.player_status = 'fall'
        else:
            if self.direction.x > 0 or self.direction.x < 0:
                self.player_status = 'run'
            else:
                self.player_status = 'idle'

    def jump(self):
        self.direction.y = self.jump_speed

    def activate_gravity(self):
        self.direction.y += self.gravity  # this is so gravity increases on each frame
        self.collision_rect.y += self.direction.y  # affects the player sprite here

    def update(self):  # used to control sprite behaviour
        self.get_input()
        self.get_player_status()
        self.animate()