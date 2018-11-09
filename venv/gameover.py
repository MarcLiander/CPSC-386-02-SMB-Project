import pygame.font

class Gameover:
    def __init__(self, ai_settings, screen):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.font = pygame.font.SysFont(None, 200)
        self.text_color = (255, 255, 255)

        self.gameover_text = "GAME OVER"
        self.gameover_text_image = self.font.render(self.gameover_text, True, self.text_color, (0, 0, 0))
        self.gameover_text_rect = self.gameover_text_image.get_rect()
        self.gameover_text_rect.center = self.screen_rect.center

    def show_gameover(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.gameover_text_image, self.gameover_text_rect)
        pygame.display.flip()