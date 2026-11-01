import pygame

from .utils import create_sprite_sheet

# All assets
bg_image = pygame.image.load("src/assets/bg.png")
player_idle_sprite_sheet = create_sprite_sheet(
    "src/assets/monkey-idle-strip5.png", 5, 32, 64
)

# Config
win_width = 512
win_height = 512
player_x = 100
player_y = 398
player_width = 64
player_height = 64
player_velocity = 30

# Animation vars
player_idle_active_frame_index = 0


def paint_window(win: pygame.Surface) -> None:
    # Repainting the window means erasing past positioned drawings
    win.fill((0, 0, 0))
    # Background
    win.blit(pygame.transform.scale(bg_image, (win_width, win_height)), (0, 0))

    # Player
    win.blit(
        player_idle_sprite_sheet[player_idle_active_frame_index], (player_x, player_y)
    )

    # Player
    # monkey = player_idle_sprite_sheet.subsurface((32 * 1, 0, 32, 32))
    # win.blit(
    #     pygame.transform.scale(monkey, (player_width, player_height)), (player_x, 398)
    # )
    # Drawing a rectangle
    # pygame.draw.rect(
    #     win, (255, 0, 0), (player_x, player_y, player_width, player_height)
    # )
    pygame.display.update()


def main() -> None:
    global player_x, player_idle_active_frame_index
    pygame.init()

    win = pygame.display.set_mode((win_width, win_height))
    pygame.display.set_caption("Banana Shooter")

    last_change = pygame.time.get_ticks()

    running = True

    while running:
        pygame.time.delay(50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            player_x -= player_velocity

        if keys[pygame.K_RIGHT]:
            player_x += player_velocity

        # Clamping
        # Logic: if x is greater then 500 - 40 = 460 then x = 500 - 40 = 460 means maximum 460
        player_x = min(player_x, win_width - player_width)
        # Logic: if x is less-then 0 then x = 0
        player_x = max(player_x, 0)

        # Player idle animation
        # Simply frame += 1 on every 150ms
        if pygame.time.get_ticks() - last_change >= 150:
            player_idle_active_frame_index += 1
            # Back to 0 if frames end
            if player_idle_active_frame_index == len(player_idle_sprite_sheet) - 1:
                player_idle_active_frame_index = 0
            last_change = pygame.time.get_ticks()

        paint_window(win)

    pygame.quit()
