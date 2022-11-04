import pygame.draw
from settings import *
from tiles import Tile
from level import Level
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
        self.world_shift = 0

        self.level = None

    def start(self):
        self.time_to_switch = False
        self.background_images = []
        for i in range(1,4):
            self.background_image = pygame.transform.smoothscale(
                pygame.image.load(f'background_layer_{i}.png').convert_alpha(), (1200, 720))
            self.background_images.append(self.background_image)
        self.background_width = self.background_images[0].get_width()

        self.level = Level(level_map, self.display_surface)

    def draw_background(self):
        for x in range(3):
            self.speed = 1
            for i in self.background_images:
                self.display_surface.blit(i, ((x * self.background_width) - self.world_shift * self.speed, 0))
                self.speed += 0.2

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
        self.draw_background()
        self.level.draw()
