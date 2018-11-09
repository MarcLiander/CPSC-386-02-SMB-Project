import pygame
from pygame.sprite import Sprite

class Goomba:
    def __init__(self, ai_settings, screen, x, y):
        super(Goomba, self).__init__()

        self.screen = screen
        self.ai_settings = ai_settings

        self.rect = pygame.Rect((x, y), (ai_settings.mario_width, ai_settings.mario_height))
        self.screen_rect = screen.get_rect()

        self.y = float(self.rect.y)
        self.x = float(self.rect.x)
        self.velocity_y = 0.0
        self.velocity_x = -1.0
        self.max_speed_x = 6.0
        self.max_speed_y = 11.1
        self.gravity = 0.5

        self.color = (10, 200, 20)

    def update(self, mario, blocks):
        position_switch = self.side_of_blocks(blocks)
        self.x += self.velocity_x
        self.rect.x = self.x

        is_on_ground = self.collide_with_blocks(blocks)
        if not is_on_ground:
            self.y += self.velocity_y
            self.velocity_y += self.gravity
            if self.velocity_y > self.max_speed_y:
                self.velocity_y = self.max_speed_y
            self.rect.y = self.y

        self.collide_with_mario(mario)

    def draw_goomba(self):
        pygame.draw.rect(self.screen, self.color, self.rect)

    def collide_with_mario(self, mario):
        if self.rect.collidepoint((mario.rect.left + (mario.rect.width / 2), mario.rect.bottom)) or self.rect.collidepoint((self.rect.right, self.rect.bottom)) or self.rect.collidepoint((mario.rect.left, mario.rect.bottom)):
            mario.velocity_y = -4.0
        if self.rect.collidepoint(mario.rect.topright) or self.rect.collidepoint(mario.rect.midright):
            mario.velocity_x = -4.0
        if self.rect.collidepoint(mario.rect.topleft) or self.rect.collidepoint(mario.rect.midleft):
            mario.velocity_x = 4.0

    def collide_with_blocks(self, blocks):
        for block in blocks:
            if block.rect.collidepoint((self.rect.left + (self.rect.width / 2), self.rect.bottom + 5)) or block.rect.collidepoint((self.rect.right - 8, self.rect.bottom + 5)) or block.rect.collidepoint((self.rect.left + 8, self.rect.bottom + 5)):
                self.y = block.rect.y - self.rect.height
                self.velocity_y = 0
                self.rect.y = self.y
                return True
        return False

    def side_of_blocks(self, blocks):
        for block in blocks:
            if block.rect.collidepoint(self.rect.midleft) or block.rect.collidepoint(self.rect.midright):
                self.velocity_x *= -1
                return True
        return False
