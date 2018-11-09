import pygame
from pygame.sprite import Sprite

class Block:
    def __init__(self, screen, x, y):
        self.screen = screen
        self.rect = pygame.Rect((x, y), (32, 32))

        self.x = float(self.rect.x)

        self.color = 80, 20, 200

    def update(self):
        self.rect.x = self.x

    def draw_block(self):
        pygame.draw.rect(self.screen, self.color, self.rect)