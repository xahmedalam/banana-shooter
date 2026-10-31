import pygame


def main() -> None:
    pygame.init()
    win_width = 500
    win_height = 500

    win = pygame.display.set_mode((win_width, win_height))
    pygame.display.set_caption("Banana Shooter")

    x = 50
    y = 50
    width = 40
    height = 60
    vel = 100

    running = True

    while running:
        pygame.time.delay(50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            x -= vel

        if keys[pygame.K_RIGHT]:
            x += vel

        if keys[pygame.K_UP]:
            y -= vel

        if keys[pygame.K_DOWN]:
            y += vel

        # Clamping
        # Logic: if x is greater than 500 - 40 = 460 then x = 500 - 40 = 460 means maximum 460
        if x > win_width - width:
            x = win_width - width

        if x < 0:
            x = 0

        if y > win_height - height:
            y = win_height - height

        if y < 0:
            y = 0

        # Repainting the window means erasing past positioned drawings
        win.fill((0, 0, 0))
        # Drawing a rectangle
        pygame.draw.rect(win, (255, 0, 0), (x, y, width, height))
        pygame.display.update()

    pygame.quit()
