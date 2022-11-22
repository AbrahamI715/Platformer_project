import pygame
from add_on import import_folder



class Player(pygame.sprite.Sprite):
    def __init__(self, pos, enemies_group: pygame.sprite.Group()):
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
        self.flip = False

        #player attacks
        self.attacking = False
        self.ready_to_attack = False
        self.attack_rate = 1.0
        self.attack_timer = 0.0
        self.attackCooldown = 0
        self.startAttackCooldown = False

        # enemy stuff
        self.enemies_group = enemies_group

    def character_assets(self):  # Allows us to access the path to character assets sheet
        path_to_char_folder = 'Character_assets/'
        self.anims = {'idle': [], 'jump': [], 'run': [], 'fall': [], 'attack': []}  # using a dictionary to easily access the folder we want

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

        if key_press[pygame.K_e] and self.attackCooldown == 0:
            self.attacking = True
            self.startAttackCooldown = True

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

        if self.attacking == True:
            self.player_status = 'attack'



    def jump(self):
        self.direction.y = self.jump_speed

    def activate_gravity(self):
        self.direction.y += self.gravity  # this is so gravity increases on each frame
        self.collision_rect.y += self.direction.y  # affects the player sprite here

    def update(self, time_delta):  # used to control sprite behaviour
        self.get_input()
        self.get_player_status()
        self.animate()

        enemy_collisions = pygame.sprite.spritecollide(self, self.enemies_group, False)
        if self.attacking and self.ready_to_attack:
            print("player attacking")
            self.attacking = False
            if enemy_collisions:
                print("collide")
                for enemy in enemy_collisions:
                    enemy.kill()
                    print("enemy killed")

        if self.attack_timer > self.attack_rate:
            self.ready_to_attack = True
        else:
            self.attack_timer += time_delta

        if self.startAttackCooldown == True:
            self.attackCooldown +=1
            if self.attackCooldown == 60:
                self.attackCooldown = 0
                self.startAttackCooldown = False



