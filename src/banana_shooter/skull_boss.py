import pygame

from .player import Player
from .utils import load_image

# How skull attacks?
# 1. -Y to Y30, and X center
# 2. X start to end >< loop 5
# 3. Detect player's X then attack


class SkullBoss:
    def __init__(
        self,
        win: pygame.Surface,
        player: Player,
        x: float,
        y: float,
        width: int,
        height: int,
        velocity: int,
        damage: int = 100,
    ) -> None:
        self.win = win
        self.player = player
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity = velocity
        self.damage = damage
        self.health = 100

        # Sprite
        self.sprite = load_image(
            "src/assets/img/skull-boss.png", (self.width, self.height)
        )
        # Collision
        self.collision = pygame.Rect(self.x, self.y, self.width, self.height)
        # Animation vars
        self.stage = 1
        self.count = 0
        self.animation_last_change = pygame.time.get_ticks()

        # HP
        self.hp_sprite = pygame.transform.scale(self.sprite, (24, 24))
        self.hp_count = 5

    def draw(self, delta: float):
        # Draw sprite
        self.win.blit(self.sprite, (self.x, self.y))
        # Update collision
        self.collision.topleft = (self.x, self.y)

        # HP
        if self.health > 80:
            self.hp_count = 5
        elif self.health > 60:
            self.hp_count = 4
        elif self.health > 40:
            self.hp_count = 3
        elif self.health > 20:
            self.hp_count = 2
        elif self.health > 0:
            self.hp_count = 1
        else:
            self.hp_count = 0
        # HP Bar
        for i in range(self.hp_count):
            i += 1
            self.win.blit(self.hp_sprite, ((self.win.width - (24 * i)) - 6, 6))

        # Animation BEGIN
        # 1. Show by moving Y30
        # +Y2 on every 50ms, for 60 counts
        if (
            self.stage == 1
            and (pygame.time.get_ticks() - self.animation_last_change) >= 10
        ):
            self.count += 1
            # Go down
            self.y += 2
            # Move to stage 2 if count is 60
            if self.count == 60:
                self.stage = 2
                # Reset count
                self.count = 0
            self.animation_last_change = pygame.time.get_ticks()
        # 2. Move left and right for 5 times
        elif (
            self.stage == 2
            and (pygame.time.get_ticks() - self.animation_last_change) >= 10
        ):
            # Left: if count is even
            if self.count % 2 == 0:
                self.x -= 3
            # Right: if count is odd
            elif self.count % 2 == 1:
                self.x += 3
            # Clamp: Stop going out from window
            self.clamp()
            # Count+ if hit the wall
            if self.x == 0 or self.x == self.win.width - self.width:
                self.count += 1

            # Attack: if count is greater then 5 and is_player_in_range
            if self.count == 5 and self.is_player_in_range():
                # Stage up
                self.stage = 3
                # Reset count
                self.count = 0

            self.animation_last_change = pygame.time.get_ticks()
        # 3. Attack and back
        if (
            self.stage == 3
            and pygame.time.get_ticks() - self.animation_last_change >= 10
        ):
            # Down: if count is even
            if self.count % 2 == 0:
                self.y += 3
            # Up: if count is odd
            if self.count % 2 == 1:
                self.y -= 3
            # Reverse: if hit the bottom
            if self.y >= self.win.height - self.height:
                self.count += 1
            # Back: if count is odd and Y is less than 56
            if self.count % 2 == 1 and self.y <= 56:
                self.count = 0
                self.stage = 2

    def is_player_in_range(self):
        """
        It will check that the Boss can touch the Player
        Example:
        - Boss: X100
        - Player: X100 + W64
        If Boss X is between 100 to 164 then return true
        """
        if self.x >= self.player.x and self.x <= (self.player.x + self.player.width):
            return True

    def clamp(self):
        self.x = min(self.x, self.win.width - self.width)
        self.x = max(self.x, 0)

    def health_down(self):
        self.health -= 2
