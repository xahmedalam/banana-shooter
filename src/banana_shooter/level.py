import pygame

from .utils import create_sprite_sheet, load_image


class Level:
    def __init__(
        self, win: pygame.Surface, health: int = 100, level: int = 4, score: int = 0
    ):
        self.win = win
        self.health = health
        self.level = level
        self.score = score
        self.level_text_color = (0, 128, 0)
        self.score_text_color = (128, 0, 128)

        # Load font
        try:
            self.font = pygame.font.Font("src/assets/font/PixelifySans-Medium.ttf", 20)
        except FileNotFoundError:
            self.font = pygame.font.Font(None, 24)

        # Heart
        self.heart_sprite = create_sprite_sheet(
            "src/assets/img/heart-strip3.png", 3, (18, 18), (24, 24)
        )
        self.health_last_change = pygame.time.get_ticks()

        # Star
        self.star_sprite = load_image("src/assets/img/star.png", (24, 24))

    def draw(self):
        # Health
        if self.health == 100:
            self.win.blit(self.heart_sprite[0], (5, 6))
        elif self.health == 50:
            self.win.blit(self.heart_sprite[1], (5, 6))
        else:
            self.win.blit(self.heart_sprite[2], (5, 6))

        # Level
        level_text_surface = self.font.render(
            f"L{self.level}", True, self.level_text_color
        )
        self.win.blit(level_text_surface, (6 + 24, 5))

        # Score
        score_text_surface = self.font.render(
            f"S{self.score}", True, self.score_text_color
        )
        self.win.blit(score_text_surface, (6 + (24 * 2), 5))

        # Star for levels
        for i in range(self.level):
            self.win.blit(self.star_sprite, (6 + (26 * i), 6 + 24))

    def score_up(self):
        self.score += 1

    def health_up(self, value: int):
        if self.health == 100:
            return
        # Health is between 0 to 50 here
        elif value == 100:
            self.health = 100
        elif value == 50:
            self.health += 50

    def health_down(self):
        # Health minus with 1s cool down
        if (pygame.time.get_ticks() - self.health_last_change) >= 1000:
            self.health -= 50
            self.health_last_change = pygame.time.get_ticks()

    def reset(self):
        self.health = 100
        self.score = 0
