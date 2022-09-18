import pygame.draw
from settings import *
from tiles import Tile
from level import Level


class GameState:
    def __init__(self, display_surface):
        self.time_to_switch = False
        self.state_to_switch_to_id = ""
        self.display_surface = display_surface

        self.level = None

    def start(self):
        self.time_to_switch = False

        self.level = Level(level_map, self.display_surface)

    def update(self):
        self.level.run()

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.time_to_switch = True
            self.state_to_switch_to_id = "main_menu"

    def stop(self):
        pass

    def draw(self, display_surface):
        display_surface.fill((0, 0, 0))
        self.level.draw()

