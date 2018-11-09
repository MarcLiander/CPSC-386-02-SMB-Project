import sys
import pygame
import time

class EventLoop:
    def __init__(self, ai_settings, screen, mario, map, finished):
        self.finished = finished
        self.ai_settings = ai_settings
        self.screen = screen
        self.mario = mario
        self.map = map

    def check_input_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self.check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self.check_keyup_events(event)

    def check_keydown_events(self, event):
        if event.key == pygame.K_SPACE:
            if self.mario.is_on_ground:
                self.mario.velocity_y = -20.01
                self.mario.is_on_ground = False
                self.mario.is_jumping = True
        if event.key == pygame.K_LEFT:
            if not self.mario.is_along_wall:
                self.mario.accel_x -= 0.25
        if event.key == pygame.K_RIGHT:
            if not self.mario.is_along_wall:
                self.mario.accel_x += 0.25
        if event.key == pygame.K_q:
            sys.exit()

    def check_keyup_events(self, event):
        if event.key == pygame.K_SPACE:
            if (self.mario.velocity_y < -12.0):
                self.mario.velocity_y = -12.0
        if event.key == pygame.K_LEFT:
            self.mario.accel_x += 0.25
        if event.key == pygame.K_RIGHT:
            self.mario.accel_x -= 0.25

    def update_events(self):
        self.mario.update(self.map)
        self.map.update_map(self.mario)

    def update_screen(self):
        self.screen.fill(self.ai_settings.bg_color)
        self.map.draw_map()
        self.mario.draw_mario()
        pygame.display.flip()
