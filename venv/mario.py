import pygame
from pygame.sprite import Sprite

class Mario:
    def __init__(self, ai_settings, screen):
        super(Mario, self).__init__()

        self.screen = screen
        self.ai_settings = ai_settings

        self.rect = pygame.Rect((40, ai_settings.screen_height - ai_settings.mario_height * 6), (ai_settings.mario_width, ai_settings.mario_height))
        self.screen_rect = screen.get_rect()

        self.is_on_ground = False
        self.is_jumping = False
        self.is_along_wall = False

        self.y = float(self.rect.y)
        self.x = float(self.rect.x)
        self.velocity_y = 6.0
        self.velocity_x = 0.0
        self.accel_x = 0.0
        self.max_speed_x = 6.0
        self.gravity = 0.5

        self.color = (10, 10, 10)

    def update(self, map):
        is_on_ground_check = self.is_on_ground
        if self.is_jumping:
            self.is_jumping = False
            #pygame.time.wait(1000)
        else:
            for b in map.block.blocks:
                is_on_ground_check = self.collide_with_blocks(b)
                if is_on_ground_check:
                    break

        if not is_on_ground_check:
            print(self.velocity_y)
            self.y += self.velocity_y
            self.velocity_y += self.gravity
            self.rect.y = self.y
        self.x += self.velocity_x
        if self.accel_x == 0:
            self.velocity_x *= 0.95
        self.velocity_x += self.accel_x
        for b in map.block.blocks:
            self.max_speed_x = self.side_of_blocks(b)
            if self.max_speed_x == 0:
                break
        if abs(self.velocity_x) >= self.max_speed_x:
            if not self.velocity_x == 0:
                self.velocity_x = (self.velocity_x/abs(self.velocity_x)) * self.max_speed_x
        self.rect.x = self.x

    def draw_mario(self):
        pygame.draw.rect(self.screen, self.color, self.rect)

    def collide_with_blocks(self, block):
        if block.collidepoint((self.rect.left + (self.rect.width / 2), self.rect.bottom + 10)) or block.collidepoint((self.rect.right - 8, self.rect.bottom + 10)) or block.collidepoint((self.rect.left + 8, self.rect.bottom + 10)):
            if self.velocity_y < 0:
                self.is_on_ground = False
                return False
            self.y = block.y - self.rect.height
            self.rect.y = self.y
            self.velocity_y = 0
            self.is_on_ground = True
            return True
        if block.collidepoint((self.rect.left + (self.rect.width / 2), self.rect.top - 1)) or block.collidepoint((self.rect.right - 8, self.rect.top - 1)) or block.collidepoint((self.rect.left + 8, self.rect.top - 1)):
            self.y = block.y + block.height + 1
            self.velocity_y = 0
        self.is_on_ground = False
        return False

    def side_of_blocks(self, block):
        if block.collidepoint((self.rect.left + 0.5, self.rect.top + 2)) or block.collidepoint((self.rect.left + 0.5, self.rect.top + (self.rect.height / 2))) or block.collidepoint((self.rect.left + 0.5, self.rect.bottom - 3)):
            self.x = block.x + self.rect.width + 0.6
            self.rect.x = self.x
            self.is_along_wall = True
            return 0
        if block.collidepoint((self.rect.right - 0.5, self.rect.top + 2))  or block.collidepoint((self.rect.right - 0.5, self.rect.top + (self.rect.height / 2))) or block.collidepoint((self.rect.right - 0.5, self.rect.bottom - 3)):
            self.x = block.x - self.rect.width - 0.6
            self.rect.x = self.x
            self.is_along_wall = True
            return 0
        self.is_along_wall = False
        return 6.0