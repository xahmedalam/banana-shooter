import pygame

from .utils import load_image


class Bullet:
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
        self.sprite = load_image("src/assets/banana.png", (self.width, self.height))

    def draw(self):
        self.win.blit(self.sprite, (self.x, self.y))
        # Fire up
        self.y -= self.velocity
