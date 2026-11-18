import pygame

from .utils import create_sprite_sheet


class BonusFireBoost:
    def __init__(
        self,
        win: pygame.Surface,
        x: float,
        y: float,
        width: int,
        height: int,
        velocity: int,
        rate_of_fire_boost: int = 6,
    ):
        self.win = win
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity = velocity
        self.rate_of_fire_boost = rate_of_fire_boost

        # Sprite
        self.strip_count = 3
        self.sprite = create_sprite_sheet(
            "src/assets/img/banana2-strip3.png", self.strip_count, (20, 20), (32, 32)
        )
        # Collision
        self.collision = pygame.Rect(self.x, self.y, self.width, self.height)
        # Animation vars
        self.sprite_animation_speed = 1
        self.sprite_current_frame_index = 0
        self.sprite_last_change = pygame.time.get_ticks()

    def draw(self, delta: float):
        # Draw sprite current frame
        self.win.blit(self.sprite[self.sprite_current_frame_index], (self.x, self.y))
        # Go down
        self.y += self.velocity * delta
        # Update collision
        self.collision.topleft = (self.x, self.y)

        # Animation
        if (
            pygame.time.get_ticks() - self.sprite_last_change
            >= (1000 / self.strip_count) / self.sprite_animation_speed
        ):
            self.sprite_current_frame_index += 1
            # Back to 0 if frames end
            if self.sprite_current_frame_index == self.strip_count:
                self.sprite_current_frame_index = 0
            self.sprite_last_change = pygame.time.get_ticks()
