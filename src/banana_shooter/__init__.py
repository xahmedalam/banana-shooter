import pygame

from .bullet import Bullet
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
        self.bullets: list[Bullet] = []
        self.rate_of_fire = 2
        self.bullet_last_change = pygame.time.get_ticks()

    def run(self):
        self.running = True

        while self.running:
            self.clock.tick(self.fps)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            keys = pygame.key.get_pressed()

            # Player
            if keys[pygame.K_LEFT]:
                self.player.go_left()
            elif keys[pygame.K_RIGHT]:
                self.player.go_right()

            self.player.is_walking = keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]

            # Fire Bullet
            if (
                keys[pygame.K_SPACE]
                and pygame.time.get_ticks() - self.bullet_last_change
                >= 1000 / self.rate_of_fire
            ):
                bullet = Bullet(self.win, self.player.x + 32, self.player.y, 16, 16, 15)
                self.bullets.append(bullet)
                self.bullet_last_change = pygame.time.get_ticks()

            # Destroy Bullet
            for index, bullet in enumerate(self.bullets):
                if bullet.y <= 0 - bullet.height:
                    self.bullets.pop(index)

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

        # Bullet
        for bullet in self.bullets:
            bullet.draw()

        # Update display
        pygame.display.update()


def main() -> None:
    game = Game()
    game.run()
