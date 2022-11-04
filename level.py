import pygame
from tiles import Tile
from player import Player
from settings import tile_size, screen_width


class Level:
    def __init__(self, level_data, surface):
        # level setup
        self.tiles = pygame.sprite.Group()
        self.player_group = pygame.sprite.GroupSingle()
        self.player = None

        self.setup_level(level_data)
        self.display_surface = surface
        self.world_shift = 0

    def setup_level(self, layout):
        for row_index, row in enumerate(layout):  # so we know exactly where each X has to be (which col and which  row)
            for col_index, cell in enumerate(row):
                x = col_index * tile_size  # otherwise too small as eg y in between 0-10
                y = row_index * tile_size

                if cell == 'X':
                    tile = Tile((x, y), tile_size)
                    self.tiles.add(tile)
                elif cell == 'P':
                    self.player = Player((x, y))
                    self.player_group.add(self.player)

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

    def horiz_collision(self):
        player = self.player
        player.rect.x += player.direction.x * player.speed

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):  # more convenient so we have access to each of the tiles
                if player.direction.x < 0:  # if the player is moving left
                    player.rect.left = sprite.rect.right
                    # collision happening on left side of player moves player to right side of obstacle it collided with
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left

    def vert_collision(self):
        player = self.player
        player.activate_gravity()

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):  # more convenient so we have access to each of the tiles
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0  # gravity cancels out
                elif player.direction.y < 0:  # if the player is jumping
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0

    def run(self):
        # tiles
        self.tiles.update(self.world_shift)  # 0 is the default position but when put at -1 or 1 level will shift

        # player
        self.player_group.update()
        self.horiz_collision()
        self.vert_collision()

    def draw(self):
        self.tiles.draw(self.display_surface)
        self.player_group.draw(self.display_surface)
        self.scroll_x()

