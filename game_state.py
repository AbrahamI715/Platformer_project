import pygame.draw
from settings import *
from tiles import Tile
from level1 import Level
from player import Player


"""scroll = 0
key = pygame.key.get_pressed()
if key[pygame.K_a] and scroll > 0:
    scroll -= 5
if key[pygame.K_d] and scroll < 3000:
    scroll += 5"""


class GameState:
    def __init__(self, display_surface):
        self.time_to_switch = False
        self.state_to_switch_to_id = ""
        self.display_surface = display_surface
        self.level = None

    def start(self):
        self.time_to_switch = False
        self.level = Level(level_map, self.display_surface)

    def update(self, time_delta):
        self.level.run(time_delta)

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.time_to_switch = True
            self.state_to_switch_to_id = "main_menu"

    def stop(self):
        pass

    def draw(self, display_surface):
        display_surface.fill((0, 0, 0))
        self.level.draw()
