import pygame.draw
from level import Level
from tiles import Tile


class OptionsState:
    def __init__(self):
        self.time_to_switch = False
        self.state_to_switch_to_id = ""

    def start(self):
        self.time_to_switch = False

    def update(self):
        pass

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.time_to_switch = True
            self.state_to_switch_to_id = "main_menu"

    def stop(self):
        pass

    def draw(self, display_surface):
        display_surface.fill((0, 0, 0))



