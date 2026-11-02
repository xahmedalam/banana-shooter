import pygame

from .utils import create_sprite_sheet

# All assets
bg_image = pygame.image.load("src/assets/bg.png")
banana_image = pygame.image.load("src/assets/banana.png")
player_idle_sprite_sheet = create_sprite_sheet(
    "src/assets/monkey-idle-strip5.png", 5, 32, 64
)
player_walk_sprite_sheet = create_sprite_sheet(
    "src/assets/monkey-walk-strip6.png", 6, 32, 64
)

# Config
win_width = 512
win_height = 512
game_fps = 30

# Player config
player_x = 100
player_y = 398
player_width = 64
player_height = 64
player_velocity = 10
is_player_direction_left = False
is_player_walking = False
# Animation vars
player_idle_animation_speed = 1.5
player_walk_animation_speed = 2
player_idle_active_frame_index = 0
player_walk_active_frame_index = 0

# Banana config
banana_x = 120
banana_y = 380
banana_width = 28
banana_height = 28
banana_velocity = 10
# Animation vars
banana_rotate_animation_speed = 8
banana_rotate_deg = 0


def paint_window(win: pygame.Surface) -> None:
    # Repainting the window means erasing past positioned drawings
    win.fill((0, 0, 0))
    # Background
    win.blit(pygame.transform.scale(bg_image, (win_width, win_height)), (0, 0))

    if not is_player_walking:
        # Player idle
        win.blit(
            pygame.transform.flip(
                player_idle_sprite_sheet[player_idle_active_frame_index],
                is_player_direction_left,
                False,
            ),
            (player_x, player_y),
        )
    else:
        # Player walking
        win.blit(
            pygame.transform.flip(
                player_walk_sprite_sheet[player_walk_active_frame_index],
                is_player_direction_left,
                False,
            ),
            (player_x, player_y),
        )

    # Banana
    win.blit(
        pygame.transform.rotate(
            pygame.transform.scale(banana_image, (banana_width, banana_height)),
            banana_rotate_deg,
        ),
        (banana_x, banana_y),
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
    global \
        player_x, \
        player_idle_active_frame_index, \
        player_walk_active_frame_index, \
        is_player_direction_left, \
        is_player_walking, \
        banana_rotate_deg
    pygame.init()
    clock = pygame.time.Clock()

    win = pygame.display.set_mode((win_width, win_height))
    pygame.display.set_caption("Banana Shooter")

    player_idle_last_change = pygame.time.get_ticks()
    player_walk_last_change = pygame.time.get_ticks()
    banana_rotate_last_change = pygame.time.get_ticks()

    running = True

    while running:
        clock.tick(game_fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            player_x -= player_velocity
            is_player_direction_left = True

        if keys[pygame.K_RIGHT]:
            player_x += player_velocity
            is_player_direction_left = False

        is_player_walking = keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]

        # Clamping
        # Logic: if x is greater then 500 - 40 = 460 then x = 500 - 40 = 460 means maximum 460
        player_x = min(player_x, win_width - player_width)
        # Logic: if x is less-then 0 then x = 0
        player_x = max(player_x, 0)

        # Player idle animation
        # Simply frame += 1 on every 200ms / speed
        if (pygame.time.get_ticks() - player_idle_last_change) >= (
            1000 / 5
        ) / player_idle_animation_speed:
            player_idle_active_frame_index += 1
            # Back to 0 if frames end
            if player_idle_active_frame_index == len(player_idle_sprite_sheet):
                # print(player_idle_active_frame_index)
                player_idle_active_frame_index = 0
            player_idle_last_change = pygame.time.get_ticks()
        # Player walk animation
        if (pygame.time.get_ticks() - player_walk_last_change) >= (
            1000 / 6
        ) / player_walk_animation_speed:
            player_walk_active_frame_index += 1
            # Back to 0 if frames end
            if player_walk_active_frame_index == len(player_walk_sprite_sheet):
                player_walk_active_frame_index = 0
            player_walk_last_change = pygame.time.get_ticks()

        # Banana rotating animation
        if (pygame.time.get_ticks() - banana_rotate_last_change) >= (
            1000 / 4
        ) / banana_rotate_animation_speed:
            banana_rotate_deg -= 90
            if banana_rotate_deg == -360:
                banana_rotate_deg = 0
            # print(banana_rotate_deg)
            banana_rotate_last_change = pygame.time.get_ticks()

        paint_window(win)

    pygame.quit()
