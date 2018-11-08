import pygame
from pygame.sprite import Sprite

class Goomba:
    def __init__(self, ai_settings, screen, mapfile, x, y):
        super(Goomba, self).__init__()
        self.filename = mapfile
        with open(self.filename, 'r') as f:
            self.rows = f.readlines()

        self.screen = screen
        self.ai_settings = ai_settings

        self.goombas = []

        self.rect = pygame.Rect((x, y), (ai_settings.mario_width, ai_settings.mario_height))
        self.screen_rect = screen.get_rect()

        self.y = float(self.rect.y)
        self.x = float(self.rect.x)
        self.velocity_y = 0.0
        self.velocity_x = -1.0
        self.max_speed_x = 6.0
        self.gravity = 0.5

        self.deltax = self.deltay = 32

        self.color = (10, 200, 20)

    def create_goombas(self):
        r = self.rect
        w, h = r.width, r.height
        dx, dy = self.deltax, self.deltay

        for nrow in range(len(self.rows)):
            row = self.rows[nrow]
            for ncol in range(len(row)):
                col = row[ncol]
                if col == 'g':
                    self.goombas.append(pygame.Rect(ncol * dx, nrow * dy, w, h))

    def update(self, mario, block):
        for goomba in self.goombas:
            position_switch = False
            for b in block.blocks:
                position_switch = self.side_of_blocks(b, goomba)
                if position_switch == True:
                    break
            goomba.x += self.velocity_x
            self.rect.x = goomba.x
            is_on_ground = False

            for b in block.blocks:
                is_on_ground = self.collide_with_blocks(b, goomba)
                if is_on_ground:
                    break

            if not is_on_ground:
                goomba.y += self.velocity_y
                self.velocity_y += self.gravity
                self.rect.y = goomba.y
            print(self.velocity_y)

            self.collide_with_mario(goomba, mario)


    def draw_goomba(self):
        for goomba in self.goombas:
            pygame.draw.rect(self.screen, self.color, goomba)

    def collide_with_mario(self, enemy, mario):
        if enemy.collidepoint((mario.rect.left + (mario.rect.width / 2), mario.rect.bottom)) or enemy.collidepoint((self.rect.right, self.rect.bottom)) or enemy.collidepoint((mario.rect.left, mario.rect.bottom)):
            mario.velocity_y = -4.0
        if enemy.collidepoint(mario.rect.topright) or enemy.collidepoint(mario.rect.midright):
            mario.velocity_x = -4.0
        if enemy.collidepoint(mario.rect.topleft) or enemy.collidepoint(mario.rect.midleft):
            mario.velocity_x = 4.0

    def collide_with_blocks(self, block, goomba):
        if block.collidepoint(goomba.midbottom) or block.collidepoint(goomba.bottomright) or block.collidepoint(goomba.bottomleft):
                goomba.y = block.y - goomba.height
                self.rect.y = goomba.y
                return True
        return False

    def side_of_blocks(self, block, goomba):
        if block.collidepoint(goomba.midleft) or block.collidepoint(goomba.midright):
            self.velocity_x *= -1
            return True
        return False
