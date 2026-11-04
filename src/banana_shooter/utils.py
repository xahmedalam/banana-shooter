import pygame


def create_sprite_sheet(
    image_src: str,
    sprites_count: int,
    size: tuple[int, int],
    scale_size: tuple[int, int] | None,
) -> list[pygame.Surface]:
    """
    ## Create seperate sprites from a sprite sheet
    ### Example:
    ```
    create_sprite_sheet(
    image_src="src/assets/monkey-idle-strip5.png",
    sprites_count=5,
    size=(32,32),
    scale_size=(64,64)
    )
    ```
    """
    if scale_size is None:
        scale_size = size

    main_image = pygame.image.load(image_src)
    sprite_sheet: list[pygame.Surface] = []

    for index in range(sprites_count):
        # img = main_image.subsurface((32 * 1, 0, 64, 64))
        img = main_image.subsurface(
            (size[0] * index, 0, size[0], size[1])
        )  # Getting every sprite one-by-one from x direction
        sprite_sheet.append(pygame.transform.scale(img, scale_size))

    return sprite_sheet


def load_image(src: str, scale_size: tuple[int, int] | None) -> pygame.Surface:
    img = pygame.image.load(src)

    if scale_size:
        return pygame.transform.scale(img, scale_size)
    else:
        return img
