import pygame

from .utils import create_sprite_sheet


class Player:
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
        # Sprites
        self.sprite_idle_strip_count = 5
        self.sprite_idle = create_sprite_sheet(
            "src/assets/monkey-idle-strip5.png", self.sprite_idle_strip_count, 32, 64
        )
        self.sprite_walk_strip_count = 6
        self.sprite_walk = create_sprite_sheet(
            "src/assets/monkey-walk-strip6.png", self.sprite_walk_strip_count, 32, 64
        )
        # Animation vars
        self.sprite_idle_animation_speed = 1.2
        self.sprite_walk_animation_speed = 1
        self.sprite_idle_current_frame_index = 0
        self.sprite_walk_current_frame_index = 0
        self.sprite_idle_last_change = pygame.time.get_ticks()
        self.sprite_walk_last_change = pygame.time.get_ticks()
        self.is_flip = False
        self.is_walking = False

    def draw(self):
        # Idle
        if not self.is_walking:
            sprite = pygame.transform.flip(
                self.sprite_idle[self.sprite_idle_current_frame_index],
                self.is_flip,
                False,
            )
        # Walk
        else:
            sprite = pygame.transform.flip(
                self.sprite_walk[self.sprite_walk_current_frame_index],
                self.is_flip,
                False,
            )

        # Draw sprite
        self.win.blit(sprite, (self.x, self.y))

        # Idle animation
        # Simply frame += 1 on every 200ms / speed
        if (
            not self.is_walking
            and pygame.time.get_ticks() - self.sprite_idle_last_change
            >= (1000 / self.sprite_idle_strip_count) / self.sprite_idle_animation_speed
        ):
            self.sprite_idle_current_frame_index += 1
            # Back to 0 if frames end
            if self.sprite_idle_current_frame_index == self.sprite_idle_strip_count:
                self.sprite_idle_current_frame_index = 0
            self.sprite_idle_last_change = pygame.time.get_ticks()
        # Walk animation
        elif (
            self.is_walking
            and pygame.time.get_ticks() - self.sprite_walk_last_change
            >= (1000 / self.sprite_walk_strip_count) / self.sprite_walk_animation_speed
        ):
            self.sprite_walk_current_frame_index += 1
            # Back to 0 if frames end
            if self.sprite_walk_current_frame_index == self.sprite_walk_strip_count:
                self.sprite_walk_current_frame_index = 0
            self.sprite_walk_last_change = pygame.time.get_ticks()

    def go_left(self):
        self.x -= self.velocity
        self.clamping()
        self.is_flip = True

    def go_right(self):
        self.x += self.velocity
        self.clamping()
        self.is_flip = False

    def clamping(self):
        self.x = min(self.x, self.win.width - self.width)
        self.x = max(self.x, 0)
