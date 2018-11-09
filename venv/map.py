import pygame
from enemies import Goomba
from brick import Block
from pygame.sprite import Sprite

class Map:
    def __init__(self, ai_settings, screen, mapfile):
        super(Map, self).__init__()
        self.filename = mapfile
        with open(self.filename, 'r') as f:
            self.rows = f.readlines()

        self.ai_settings = ai_settings
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.goombas = []
        self.blocks = []
        self.max_x_value = 0

    def create_level(self):
        dx = dy = 32

        for nrow in range(len(self.rows)):
            row = self.rows[nrow]
            for ncol in range(len(row)):
                col = row[ncol]
                if col == 'x':
                    self.blocks.append(Block(self.screen, ncol * dx, nrow * dy))
                if col == 'g':
                    self.goombas.append(Goomba(self.ai_settings, self.screen, ncol * dx, nrow * dy))
                if ncol * dx > self.max_x_value:
                    self.max_x_value = ncol * dx

    def draw_map(self):
        for block in self.blocks:
            if block.rect.left < self.screen_rect.right:
                block.draw_block()
        for goomba in self.goombas:
            if goomba.rect.left < self.screen_rect.right:
                goomba.draw_goomba()

    def update_map(self, mario):
        for goomba in self.goombas:
            if goomba.rect.top > self.screen_rect.height or goomba.rect.right < self.screen_rect.left:
                self.goombas.remove(goomba)
            elif goomba.x < self.screen_rect.right:
                goomba.update(mario, self.blocks)
        for block in self.blocks:
            if block.rect.top > self.screen_rect.height or block.rect.right < self.screen_rect.left:
                self.blocks.remove(block)
            elif block.x < self.screen_rect.right:
                block.update()
        print(self.max_x_value)
        if mario.x >= self.screen_rect.width / 2 and abs(mario.velocity_x) > 0 and self.screen_rect.right < self.max_x_value:
            mario.x = self.screen_rect.width / 2
            for block in self.blocks:
                block.x -= mario.velocity_x
            for goomba in self.goombas:
                goomba.x -= mario.velocity_x
            self.max_x_value -= mario.velocity_x