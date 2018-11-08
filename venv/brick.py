import pygame
from pygame.sprite import Sprite

class Block:
    def __init__(self, screen, mapfile):
        self.screen = screen
        self.filename = mapfile
        with open(self.filename, 'r') as f:
            self.rows = f.readlines()

        self.blocks = []
        self.rect = pygame.Rect((0, 0), (32, 32))
        self.deltax = self.deltay = 32

        self.color = 80, 20, 200

    def build(self):
        r = self.rect
        w, h = r.width, r.height
        dx, dy = self.deltax, self.deltay

        for nrow in range(len(self.rows)):
            row = self.rows[nrow]
            for ncol in range(len(row)):
                col = row[ncol]
                if col == 'x':
                    self.blocks.append(pygame.Rect(ncol * dx, nrow * dy, w, h))

    def draw_blocks(self):
        for rect in self.blocks:
            pygame.draw.rect(self.screen, self.color, rect)