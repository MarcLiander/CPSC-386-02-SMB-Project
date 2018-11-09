import pygame
from pygame.sprite import Sprite

class Mario:
    def __init__(self, ai_settings, screen):
        super(Mario, self).__init__()

        self.screen = screen
        self.ai_settings = ai_settings

        self.rect = pygame.Rect((ai_settings.mario_width * 3, ai_settings.screen_height - ai_settings.mario_height * 9), (ai_settings.mario_width, ai_settings.mario_height))
        self.screen_rect = screen.get_rect()

        self.is_on_ground = False
        self.is_jumping = False
        self.is_along_wall = False

        self.x = float(self.rect.x)

        self.velocity_y = 6.0
        self.velocity_x = 0.0
        self.accel_x = 0.0
        self.max_speed_x = 6.5
        self.max_speed_y = 16.0
        self.gravity = 1.5

        self.color = (10, 10, 10)

    def update(self, map):
        self.x += self.velocity_x
        if self.accel_x == 0:
            self.velocity_x *= 0.9
        if abs(self.velocity_x) < 0.05:
            self.velocity_x = 0
        self.velocity_x += self.accel_x
        self.side_of_blocks(map.blocks)
        if abs(self.velocity_x) >= self.max_speed_x:
            if not self.velocity_x == 0:
                self.velocity_x = (self.velocity_x / abs(self.velocity_x)) * self.max_speed_x
        if self.x < self.screen_rect.left:
            self.x = self.screen_rect.left
        self.rect.x = self.x
        self.side_of_blocks(map.blocks)

        if self.is_jumping:
            self.is_jumping = False
        else:
            self.collide_with_blocks(map.blocks)

        if not self.is_on_ground:
            self.velocity_y += self.gravity
            if self.velocity_y > self.max_speed_y:
                self.velocity_y = self.max_speed_y
            self.rect.y += self.velocity_y
            self.collide_with_blocks(map.blocks)

    def draw_mario(self):
        pygame.draw.rect(self.screen, self.color, self.rect)

    def collide_with_blocks(self, blocks):
        for block in blocks:
            if block.rect.collidepoint((self.rect.left + (self.rect.width / 2), self.rect.bottom)) or block.rect.collidepoint((self.rect.right - 4, self.rect.bottom)) or block.rect.collidepoint((self.rect.left + 4, self.rect.bottom)):
                if self.velocity_y < 0:
                    self.is_on_ground = False
                    return False
                self.rect.y = block.rect.y - self.rect.height
                self.velocity_y = 0
                self.is_on_ground = True
                return True
            if block.rect.collidepoint((self.rect.left + (self.rect.width / 2), self.rect.top)) or block.rect.collidepoint((self.rect.right - 4, self.rect.top)) or block.rect.collidepoint((self.rect.left + 4, self.rect.top)):
                self.rect.y = block.rect.y + block.rect.height
                if not self.velocity_y >= 0:
                    self.velocity_y = 0
        self.is_on_ground = False
        return False

    def side_of_blocks(self, blocks):
        for block in blocks:
            if (block.rect.collidepoint((self.rect.left, self.rect.top + 6)) or block.rect.collidepoint((self.rect.left, self.rect.top + (self.rect.height / 2))) or block.rect.collidepoint((self.rect.left, self.rect.bottom - 6))) and self.velocity_x < 0:
                self.x = block.rect.x + self.rect.width
                self.rect.x = self.x
                self.velocity_x = 0
                self.is_along_wall = True
                self.max_speed_x = 0
            if (block.rect.collidepoint((self.rect.right, self.rect.top + 6))  or block.rect.collidepoint((self.rect.right, self.rect.top + (self.rect.height / 2))) or block.rect.collidepoint((self.rect.right, self.rect.bottom - 6))) and self.velocity_x > 0:
                self.x = block.rect.x - self.rect.width
                self.rect.x = self.x
                self.velocity_x = 0
                self.is_along_wall = True
                self.max_speed_x = 0
        self.is_along_wall = False
        self.max_speed_x = 6.5