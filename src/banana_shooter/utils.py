import pygame


def create_sprite_sheet(
    image_src: str, sprites_count: int, size: int, scale_size: int | None
) -> list[pygame.Surface]:
    """
    ## Create seperate sprites from a sprite sheet
    ### Example:
    ```python
    create_sprite_sheet(
    image_src="src/assets/monkey-idle-strip5.png",
    sprites_count=5,
    size=32,
    scale_size=64
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
            (size * index, 0, size, size)
        )  # Getting every sprite one-by-one from x direction
        sprite_sheet.append(pygame.transform.scale(img, (scale_size, scale_size)))

    return sprite_sheet


def load_image(src: str, scale_size: tuple[int, int] | None) -> pygame.Surface:
    img = pygame.image.load(src)

    if scale_size:
        return pygame.transform.scale(img, scale_size)
    else:
        return img
