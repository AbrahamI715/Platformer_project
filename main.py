import pygame
import pygame_gui
from main_menu import MainMenuState
from game_state import GameState
from options_state import OptionsState
from settings import *


class MyGameApp:
    def __init__(self):
        pygame.init()
        self.display_size = (screen_width, screen_height)
        self.display_surface = pygame.display.set_mode(self.display_size)

        self.clock = pygame.time.Clock()

        self.ui_manager = pygame_gui.UIManager(self.display_size)
        self.states = {'main_menu': MainMenuState(self.ui_manager),
                       'game': GameState(self.display_surface), 'options': OptionsState(self.ui_manager)}
        self.active_state = self.states['main_menu']
        self.active_state.start()

        self.running = True

    def run(self):
        while self.running:
            time_delta = self.clock.tick(90)/1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                self.active_state.handle_event(event)
                self.ui_manager.process_events(event)

            self.ui_manager.update(time_delta)
            self.active_state.update()

            self.active_state.draw(self.display_surface)

            pygame.display.flip()

            self.check_time_to_switch_state()

    def check_time_to_switch_state(self):
        if self.active_state.time_to_switch:
            self.active_state.stop()
            self.active_state = self.states[self.active_state.state_to_switch_to_id]
            self.active_state.start()


my_game = MyGameApp()
my_game.run()


