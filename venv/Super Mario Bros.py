import sys
import pygame
from settings import Settings
from mario import Mario
from enemies import Goomba
from map import Map
from brick import Block
from game_events import EventLoop

class Game:
        def __init__(self):
            pygame.init()
            self.ai_settings = Settings()
            self.screen = pygame.display.set_mode((self.ai_settings.screen_width, self.ai_settings.screen_height))
            pygame.display.set_caption("Super Mario Bros Clone")
            self.mario_player = Mario(self.ai_settings, self.screen)
            self.map = Map(self.ai_settings, self.screen, mapfile='Levels/first_level.txt')
            self.clock = pygame.time.Clock()

        def play(self):
            eloop = EventLoop(self.ai_settings, self.screen, self.mario_player, self.map, finished = False)
            self.map.create_level()

            while not eloop.finished:
                eloop.update_events()
                eloop.check_input_events()
                eloop.update_screen()
                self.clock.tick(30)


game = Game()
game.play()