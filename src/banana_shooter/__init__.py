import pygame

win_width = 500
win_height = 500
player_x = 100
player_y = 400
player_width = 40
player_height = 60
player_velocity = 20


def paintWindow(win: pygame.Surface) -> None:
    # Repainting the window means erasing past positioned drawings
    win.fill((0, 0, 0))
    # Drawing a rectangle
    pygame.draw.rect(
        win, (255, 0, 0), (player_x, player_y, player_width, player_height)
    )
    pygame.display.update()


def main() -> None:
    global player_x, player_y
    pygame.init()

    win = pygame.display.set_mode((win_width, win_height))
    pygame.display.set_caption("Banana Shooter")

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
        player_y = min(player_y, win_height - player_height)
        player_y = max(player_y, 0)

        paintWindow(win)

    pygame.quit()
