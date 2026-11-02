import pygame

from .player import Player
from .utils import load_image


class Game:
    def __init__(self) -> None:
        self.width = 512
        self.height = 512
        self.fps = 30
        self.running = False

        pygame.init()
        pygame.display.set_caption("Banana Shooter")
        self.win = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()

        self.player = Player(self.win, 100, 398, 64, 64, 10)

    def run(self):
        self.running = True

        while self.running:
            self.clock.tick(self.fps)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            keys = pygame.key.get_pressed()

            if keys[pygame.K_LEFT]:
                self.player.go_left()
            elif keys[pygame.K_RIGHT]:
                self.player.go_right()

            self.player.is_walking = keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]

            self.paint()

        pygame.quit()

    def paint(self):
        # Repainting the window means erasing past positioned drawings
        self.win.fill((0, 0, 0))
        # Background
        self.win.blit(
            load_image("src/assets/bg.png", (self.width, self.height)), (0, 0)
        )
        # Player
        self.player.draw()
        # Update display
        pygame.display.update()


def main() -> None:
    game = Game()
    game.run()
