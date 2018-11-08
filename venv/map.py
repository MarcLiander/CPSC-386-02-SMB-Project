import pygame
from enemies import Goomba
from brick import Block
from pygame.sprite import Sprite

class Map:
    def __init__(self, ai_settings, screen, mapfile):
        super(Map, self).__init__()
        self.ai_settings = ai_settings
        self.screen = screen
        self.goomba = Goomba(self.ai_settings, self.screen, mapfile, 700, 300)
        self.block = Block(self.screen, mapfile)

    def create_level(self):
        self.goomba.create_goombas()
        self.block.build()

    def draw_map(self):
        self.block.draw_blocks()
        self.goomba.draw_goomba()

    def update_map(self, mario):
        self.goomba.update(mario, self.block)

