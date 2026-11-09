import pygame

from .utils import create_sprite_sheet


class Level:
    def __init__(self, win: pygame.Surface, health: int = 100, score: int = 0):
        self.win = win
        self.health = health
        self.score = score
        self.text_color = (0, 0, 0)

        # Load font
        try:
            self.font = pygame.font.Font("src/assets/PixelifySans-Medium.ttf", 20)
        except FileNotFoundError:
            self.font = pygame.font.Font(None, 24)

        # Heart
        self.heart_sprite = create_sprite_sheet(
            "src/assets/heart-strip3.png", 3, (18, 18), (24, 24)
        )
        self.health_last_change = pygame.time.get_ticks()

    def draw(self):
        text_surface = self.font.render(f"S{self.score}", True, self.text_color)
        self.win.blit(text_surface, (6 + 24, 5))

        if self.health == 100:
            self.win.blit(self.heart_sprite[0], (5, 6))
        elif self.health == 50:
            self.win.blit(self.heart_sprite[1], (5, 6))
        else:
            self.win.blit(self.heart_sprite[2], (5, 6))

    def score_up(self):
        self.score += 1

    def health_down(self):
        # Health minus with 1s cool down
        if (pygame.time.get_ticks() - self.health_last_change) >= 1000:
            self.health -= 50
            self.health_last_change = pygame.time.get_ticks()

    def reset(self):
        self.health = 100
        self.score = 0
