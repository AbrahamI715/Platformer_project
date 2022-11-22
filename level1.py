import pygame
from tiles import Tile
from player import Player
from enemy import Enemy
from settings import tile_size, screen_width


class Level:
    def __init__(self, level_data, surface):
        # level setup
        self.tiles = pygame.sprite.Group()
        self.player_group = pygame.sprite.GroupSingle()
        self.enemies = pygame.sprite.Group()
        self.player = None

        self.setup_level(level_data)
        self.display_surface = surface
        self.world_shift = 0
        self.world_scroll = 0

    def setup_level(self, layout):
        for row_index, row in enumerate(layout):  # so we know exactly where each X has to be (which col and which  row)
            for col_index, cell in enumerate(row):
                x = col_index * tile_size  # otherwise too small as eg y in between 0-10
                y = row_index * tile_size

                if cell == 'X':
                    tile = Tile((x, y), tile_size)
                    self.tiles.add(tile)
                elif cell == 'P':
                    self.player = Player((x, y), self.enemies)
                    self.player_group.add(self.player)
                elif cell == 'E':
                    enemy = Enemy((x, y), self.enemies)
                    self.enemies.add(enemy)

        self.background_images = []
        for i in range(1, 4):
            self.background_image = pygame.transform.smoothscale(
                pygame.image.load(f'background_layer_{i}.png').convert_alpha(), (1200, 720))
            self.background_images.append(self.background_image)
        self.background_width = self.background_images[0].get_width()


    def scroll_x(self):
        # scrolling camera for player
        player = self.player
        player_x = player.rect.centerx  # where player is on x coord
        direction_x = player.direction.x  # what direction player is moving in

        if player_x < screen_width / 4 and direction_x < 0:  # if player is heading left
            self.world_shift = 4
            player.speed = 0

        elif player_x > screen_width - (screen_width / 4) and direction_x > 0:  # if player is heading right
            self.world_shift = -4
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 4

        self.world_scroll += self.world_shift

    def horiz_collision(self):
        player = self.player
        player.collision_rect.x += player.direction.x * player.speed

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.collision_rect):  # more convenient so we have access to each of the tiles
                if player.direction.x < 0:  # if the player is moving left
                    player.collision_rect.left = sprite.rect.right
                    # collision happening on left side of player moves player to right side of obstacle it collided with
                elif player.direction.x > 0:
                    player.collision_rect.right = sprite.rect.left

    def vert_collision(self):
        player = self.player
        player.activate_gravity()

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.collision_rect):  # more convenient so we have access to each of the tiles
                if player.direction.y > 0:
                    player.collision_rect.bottom = sprite.rect.top
                    player.direction.y = 0  # gravity cancels out
                elif player.direction.y < 0:  # if the player is jumping
                    player.collision_rect.top = sprite.rect.bottom
                    player.direction.y = 0

    def run(self, time_delta):
        # tiles
        self.tiles.update(self.world_shift)  # 0 is the default position but when put at -1 or 1 level will shift
        self.enemies.update(self.world_shift)
        # player
        self.player_group.update(time_delta)
        self.vert_collision()
        self.horiz_collision()

    def draw(self):
        self.draw_background()
        self.tiles.draw(self.display_surface)
        self.enemies.draw(self.display_surface)
        self.player_group.draw(self.display_surface)
        self.scroll_x()
        #pygame.draw.rect(self.display_surface, pygame.Color('#FF0000'), self.player.rect, 1)
        #pygame.draw.rect(self.display_surface, pygame.Color('#FF00FF'), self.player.collision_rect, 1)

    def draw_background(self):
        for x in range(8):
            self.speed = 0.5
            for i in self.background_images:
                position = ((x * self.background_width) + self.world_scroll * self.speed, 0)
                self.display_surface.blit(i, position)
                self.speed += 0.12

