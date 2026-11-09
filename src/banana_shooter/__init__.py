import random

import pygame

from .bullet import Bullet
from .enemy import Enemy
from .level import Level
from .player import Player
from .utils import load_image


class Game:
    def __init__(self) -> None:
        self.width = 512
        self.height = 512
        self.fps = 60
        self.running = False

        # Fix sound lag
        pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=4096)

        pygame.init()
        pygame.font.init()
        pygame.display.set_caption("Banana Shooter")
        self.win = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()

        # Settings
        self.player_velocity = 400
        self.bullet_velocity = 400
        self.enemy_velocity = 250
        self.rate_of_fire = 2  # Fires per second
        self.rate_of_enemies = 1.5  # Enemies per second

        # Level init
        self.level = Level(self.win)

        # Player init
        self.player = Player(self.win, 0.0, 220.0, 398.0, 64, 64, self.player_velocity)

        # Bullets
        self.bullets: list[Bullet] = []
        self.bullet_last_change = pygame.time.get_ticks()

        # Enemies
        self.enemies: list[Enemy] = []
        self.enemy_last_change = pygame.time.get_ticks()

        # Game over
        self.is_gameover = False

        # Sound bg
        pygame.mixer.music.load("src/assets/EternityLivesLoop.wav")
        pygame.mixer.music.set_volume(1)
        pygame.mixer.music.play(-1)

    def run(self):
        self.running = True

        while self.running:
            # FPS and Delta
            self.delta = self.clock.tick(self.fps) / 1000
            self.player.delta = self.delta

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            keys = pygame.key.get_pressed()

            # Continue: reset the game
            if keys[pygame.K_RETURN] and self.is_gameover:
                self.player.x = 220.0
                self.player.is_flip = False
                self.bullets = []
                self.enemies = []
                self.level.reset()
                self.is_gameover = False

            # Player moves if not game over
            if keys[pygame.K_LEFT] or keys[pygame.K_a] and not self.is_gameover:
                self.player.go_left()
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d] and not self.is_gameover:
                self.player.go_right()

            self.player.is_walking = (
                keys[pygame.K_LEFT]
                or keys[pygame.K_RIGHT]
                or keys[pygame.K_a]
                or keys[pygame.K_d]
            )

            # Fire Bullet
            if (
                not self.is_gameover  # No fire if game over
                and keys[pygame.K_SPACE]
                and pygame.time.get_ticks() - self.bullet_last_change
                >= 1000 / self.rate_of_fire
            ):
                bullet = Bullet(
                    self.win,
                    self.delta,
                    self.player.x + 20,
                    self.player.y,
                    24,
                    24,
                    self.bullet_velocity,
                )
                self.bullets.append(bullet)
                self.bullet_last_change = pygame.time.get_ticks()

            # Cleanup: destroy bullet if out off window
            for index, bullet in enumerate(self.bullets):
                if bullet.y <= 0 - bullet.height:
                    self.bullets.pop(index)

            # Enemy: add an enemy on every 1000ms / rate_of_enemy
            if (
                pygame.time.get_ticks() - self.enemy_last_change
                >= 1000 / self.rate_of_enemies
            ):
                random_x = random.randint(32, self.width - 32)
                enemy = Enemy(
                    self.win, self.delta, random_x, -32.0, 32, 32, self.enemy_velocity
                )
                self.enemies.append(enemy)
                self.enemy_last_change = pygame.time.get_ticks()

            # Cleanup: destroy enemy if out off window
            for index, enemy in enumerate(self.enemies):
                if enemy.y >= self.height:
                    self.enemies.pop(index)

            # Destroy when bullet and enemy collides
            for bullet_index, bullet in enumerate(self.bullets):
                # Check 1 bullet on all enemies
                for enemy_index, enemy in enumerate(self.enemies):
                    # If bullet touch the enemy then remove both
                    if bullet.collision.colliderect(enemy.collision):
                        self.bullets.pop(bullet_index)
                        self.enemies.pop(enemy_index)
                        # Score up
                        self.level.score_up()
                        # Skip left enemies check for this bullet
                        break

            # Health minus if enemy touches the player
            for enemy in self.enemies:
                if (
                    self.player.collision.colliderect(enemy.collision)
                    and not self.is_gameover
                ):
                    self.level.health_down()

            # Game over if health is less than 0
            if self.level.health < 0:
                self.is_gameover = True

            self.paint()

        pygame.quit()

    def paint(self):
        # Repainting the window means erasing past positioned drawings
        self.win.fill((0, 0, 0))
        # Background
        self.win.blit(
            load_image("src/assets/bg.png", (self.width, self.height)), (0, 0)
        )
        # Player: draw player if not game over
        if not self.is_gameover:
            self.player.draw()

        # Enemy
        for enemy in self.enemies:
            enemy.draw()

        # Bullet
        for bullet in self.bullets:
            bullet.draw()

        # Level
        self.level.draw()

        # Game over? then draw game over image
        if self.is_gameover:
            gameover_img_scale = 10
            gameover_img_width = 32 * gameover_img_scale
            gameover_img_height = 17 * gameover_img_scale
            self.win.blit(
                load_image(
                    "src/assets/game-over.png",
                    (
                        gameover_img_width,
                        gameover_img_height,
                    ),
                ),
                (
                    (self.width / 2) - (gameover_img_width / 2),
                    (self.height / 2) - (gameover_img_height / 2),
                ),
            )

        # Update display
        pygame.display.update()


def main() -> None:
    game = Game()
    game.run()
