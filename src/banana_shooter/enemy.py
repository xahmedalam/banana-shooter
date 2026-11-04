import pygame

from .utils import create_sprite_sheet


class Enemy:
    def __init__(
        self,
        win: pygame.Surface,
        x: int,
        y: int,
        width: int,
        height: int,
        velocity: int,
    ) -> None:
        self.win = win
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity = velocity
        # Sprite
        self.strip_count = 3
        self.sprite = create_sprite_sheet(
            "src/assets/bat-idle-strip3.png",
            self.strip_count,
            (24, 24),
            (self.width, self.height),
        )
        # Animation vars
        self.sprite_animation_speed = 6
        self.sprite_current_frame_index = 0
        self.sprite_last_change = pygame.time.get_ticks()

    def draw(self):
        # Draw sprite current frame
        self.win.blit(self.sprite[self.sprite_current_frame_index], (self.x, self.y))
        # Go down
        self.y += self.velocity

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
