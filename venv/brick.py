import pygame
from pygame.sprite import Sprite

class Block:
    def __init__(self, screen, x, y, type):
        self.screen = screen
        self.rect = pygame.Rect((x, y), (32, 32))

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.velocity_y = 3.0
        self.gravity = 0.3
        self.original_y = float(self.rect.y)

        self.type = type

        self.is_headbutt = False

        self.color = 80, 20, 200

    def update(self):
        self.rect.x = int(self.x)

        if self.is_headbutt and self.type == 1:
            self.velocity_y += self.gravity
            self.rect.y += int(self.velocity_y)

        if self.rect.y >= self.original_y:
            self.is_headbutt = False
            self.rect.y = int(self.original_y)

    def draw_block(self, block_image):
        self.screen.blit(block_image, self.rect)