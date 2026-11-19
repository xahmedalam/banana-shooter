import pygame

from .utils import create_sprite_sheet, load_image


class Level:
    def __init__(
        self, win: pygame.Surface, health: int = 100, level: int = 1, score: int = 0
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

        # BonusFireBoost
        self.hits_count = 0
        # Life line
        self.banana_life_ms = 0
        self.banana_life_count = 0
        self.banana_life_last_change = pygame.time.get_ticks()
        # Sprite
        self.banana_sprite_strip_count = 3
        self.banana_sprite = create_sprite_sheet(
            "src/assets/img/banana2-strip3.png",
            self.banana_sprite_strip_count,
            (20, 20),
            (24, 24),
        )
        # Animation vars
        self.banana_sprite_animation_speed = 3
        self.banana_sprite_current_frame_index = 0
        self.banana_sprite_animation_last_change = pygame.time.get_ticks()

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

        # BonusFireBoost: run for 4 times with 1000ms gap
        if (
            self.banana_life_count != 0
            and pygame.time.get_ticks() - self.banana_life_last_change
            >= self.banana_life_ms / 4
        ):
            # Minus count
            self.banana_life_count -= 1
            self.banana_life_last_change = pygame.time.get_ticks()

        # BonusFireBoost life line
        for i in range(self.banana_life_count):
            self.win.blit(
                self.banana_sprite[self.banana_sprite_current_frame_index],
                (6 + (26 * i), 6 + (24 * 2)),
            )

        # BonusFireBoost animation
        if (
            pygame.time.get_ticks() - self.banana_sprite_animation_last_change
            >= (1000 / self.banana_sprite_strip_count)
            / self.banana_sprite_animation_speed
        ):
            self.banana_sprite_current_frame_index += 1
            # Back to 0 if frames end
            if self.banana_sprite_current_frame_index == self.banana_sprite_strip_count:
                self.banana_sprite_current_frame_index = 0
            self.banana_sprite_animation_last_change = pygame.time.get_ticks()

    def score_up(self):
        self.score += 1
        # Level up
        if self.score == 5:
            self.level = 2
        # BonusFireBoost
        self.hits_count += 1

    def health_up(self, value: int):
        if self.health == 100:
            return
        # Health is between 0 to 50 here
        elif value == 100:
            self.health = 100
        elif value == 50:
            self.health += 50

    def health_down(self, damage: int = 50):
        # Health minus with 1s cool down
        if (pygame.time.get_ticks() - self.health_last_change) >= 1000:
            self.health -= damage
            self.health_last_change = pygame.time.get_ticks()

    def reset(self):
        self.health = 100
        self.score = 0
        self.hits_count = 0

    def start_fire_boost_life_line(self, life_ms: int):
        self.banana_life_ms = life_ms
        self.banana_life_count = 4
        self.banana_life_last_change = pygame.time.get_ticks()
