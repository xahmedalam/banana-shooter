import pygame

from .utils import create_sprite_sheet


class Player:
    def __init__(
        self,
        win: pygame.Surface,
        delta: float,
        x: float,
        y: float,
        width: int,
        height: int,
        velocity: int,
    ) -> None:
        self.win = win
        self.delta = delta
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity = velocity
        # Sprites
        self.sprite_idle_strip_count = 5
        self.sprite_idle = create_sprite_sheet(
            "src/assets/monkey-idle-strip5.png",
            self.sprite_idle_strip_count,
            (32, 32),
            (64, 64),
        )
        self.sprite_walk_strip_count = 6
        self.sprite_walk = create_sprite_sheet(
            "src/assets/monkey-walk-strip6.png",
            self.sprite_walk_strip_count,
            (32, 32),
            (64, 64),
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
        # Collision
        self.collision = pygame.Rect((self.x, self.y, self.width, self.height))
        # Effect vars
        self.effect_blink_count = 0
        self.effect_blink_on = False
        self.effect_blink_last_change = pygame.time.get_ticks()
        self.is_blinking = False

    def draw(self):
        # Update collision
        self.collision.topleft = (self.x, self.y)

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

        # Effect blink: if effect_blink_on is true then increase sprite light
        if self.effect_blink_on:
            sprite = pygame.transform.hsl(sprite, 0, 0, 0.6)

        # Effect blink: if blinking is true then on every 30ms turn on and off effect_blink_on
        if (
            self.is_blinking
            and (pygame.time.get_ticks() - self.effect_blink_last_change) >= 30
        ):
            # If true then false, If false then true
            self.effect_blink_on = not self.effect_blink_on
            # Count + 1
            self.effect_blink_count += 1
            # After 6 counts stop blinking, it actually blinks half of the count
            if self.effect_blink_count == 6:
                self.effect_blink_count = 0
                self.is_blinking = False
            # Finally update last change time
            self.effect_blink_last_change = pygame.time.get_ticks()

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
        self.x -= self.velocity * self.delta
        self.clamping()
        self.is_flip = True

    def go_right(self):
        self.x += self.velocity * self.delta
        self.clamping()
        self.is_flip = False

    def clamping(self):
        self.x = min(self.x, self.win.width - self.width)
        self.x = max(self.x, 0)

    def effect_blink(self):
        self.is_blinking = True
