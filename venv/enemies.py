import pygame
from pygame.sprite import Sprite

class Goomba:
    def __init__(self, ai_settings, screen, x, y, id, type):
        super(Goomba, self).__init__()

        self.screen = screen
        self.ai_settings = ai_settings

        self.rect = pygame.Rect((x, y), (ai_settings.mario_width, ai_settings.mario_height))
        self.screen_rect = screen.get_rect()

        self.y = float(self.rect.y)
        self.x = float(self.rect.x)
        self.velocity_y = 0.0
        self.velocity_x = -0.5
        self.max_speed_x = 6.0
        self.max_speed_y = 8.0
        self.gravity = 0.3

        self.id = id
        self.type = type

        self.is_bounced_on = False
        self.is_dead = False
        self.time_alive = 30

        self.color = (10, 200, 20)

    def update(self, mario, blocks, goombas, stats):
        self.side_of_blocks(blocks)
        if self.is_bounced_on or self.is_dead:
            self.velocity_x = 0
        self.x += self.velocity_x
        self.rect.x = int(self.x)

        is_on_ground = False
        if not self.is_dead:
            is_on_ground = self.collide_with_blocks(blocks, stats)
        if not is_on_ground:
            self.y += self.velocity_y
            self.velocity_y += self.gravity
            if self.velocity_y > self.max_speed_y:
                self.velocity_y = self.max_speed_y
            self.rect.y = self.y

        if not self.is_bounced_on and not self.is_dead:
            self.collide_with_mario(mario, stats)
            self.collide_with_other_goomba(goombas)

    def draw_goomba(self):
        pygame.draw.rect(self.screen, self.color, self.rect)

    def collide_with_mario(self, mario, stats):
        if self.rect.collidepoint((mario.rect.left + (mario.rect.width / 2), mario.rect.bottom)) or self.rect.collidepoint((mario.rect.right, mario.rect.bottom)) or self.rect.collidepoint((mario.rect.left, mario.rect.bottom)):
            mario.velocity_y = -6.0
            stats.score += 100
            self.is_bounced_on = True
        if self.rect.collidepoint((mario.rect.right - 1, mario.rect.top + 7)) or self.rect.collidepoint(mario.rect.right - 1, mario.rect.top + (mario.rect.height / 2)) or self.rect.collidepoint(mario.rect.right - 1, mario.rect.bottom - 7):
            mario.velocity_y = -4.0
            mario.is_dead = True
        if self.rect.collidepoint((mario.rect.left + 1, mario.rect.top + 7)) or self.rect.collidepoint(mario.rect.left +  1, mario.rect.top + (mario.rect.height / 2)) or self.rect.collidepoint(mario.rect.left + 1, mario.rect.bottom - 7):
            mario.velocity_y = -4.0
            mario.is_dead = True

    def collide_with_blocks(self, blocks, stats):
        for block in blocks:
            if block.rect.collidepoint((self.rect.left + (self.rect.width / 2), self.rect.bottom + 5)) or block.rect.collidepoint((self.rect.right - 2, self.rect.bottom + 5)) or block.rect.collidepoint((self.rect.left + 2, self.rect.bottom + 5)):
                self.y = block.rect.y - self.rect.height
                self.velocity_y = 0
                self.rect.y = self.y
                if block.is_headbutt and not block.velocity_y == 0 and block.type == 1:
                    self.is_dead = True
                    self.velocity_y = -3.5
                    stats.score += 100
                return True
        return False

    def side_of_blocks(self, blocks):
        for block in blocks:
            if block.rect.collidepoint(self.rect.midleft) or block.rect.collidepoint(self.rect.midright):
                self.velocity_x *= -1

    def collide_with_other_goomba(self, goombas):
        for goomba in goombas:
            if (goomba.rect.collidepoint(self.rect.midleft) or goomba.rect.collidepoint(self.rect.midright)) and not self.id == goomba.id and not self.is_bounced_on and not goomba.is_bounced_on:
                self.velocity_x *= -1