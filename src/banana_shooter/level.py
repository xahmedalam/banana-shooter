import pygame


class Level:
    def __init__(self, win: pygame.Surface):
        self.win = win
        self.score = 0
        self.text_color = (0, 0, 0)

        # Load font
        try:
            self.font = pygame.font.Font("src/assets/PixelifySans-Medium.ttf", 20)
        except FileNotFoundError:
            self.font = pygame.font.Font(None, 24)

    def draw(self):
        text_surface = self.font.render(f"Score: {self.score}", True, self.text_color)
        self.win.blit(text_surface, (5, 5))

    def score_up(self):
        self.score += 1

    def score_reset(self):
        self.score = 0
