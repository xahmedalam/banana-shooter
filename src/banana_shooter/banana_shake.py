import pygame

from .utils import load_image


class BananaShake:
    def __init__(
        self,
        win: pygame.Surface,
        x: float,
        y: float,
        width: int,
        height: int,
        velocity: int,
        bonus: int = 50,
    ):
        self.win = win
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity = velocity
        self.bonus = bonus

        # Sprite
        self.sprite = load_image("src/assets/img/banana-shake.png", (32, 32))
        # Collision
        self.collision = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, delta: float):
        # Draw sprite
        self.win.blit(self.sprite, (self.x, self.y))
        # Go down
        self.y += self.velocity * delta
        # Update collision
        self.collision.topleft = (self.x, self.y)
