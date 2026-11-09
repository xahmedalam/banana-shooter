import pygame


class AudioManager:
    @classmethod
    def pre_init(cls):
        # Fix sound lag
        pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=4096)

    def __init__(self) -> None:
        # Bg sound
        pygame.mixer.music.load("src/assets/EternityLivesLoop.wav")
        pygame.mixer.music.set_volume(1)

    def bg_play(self):
        pygame.mixer.music.play(-1)

    def bg_stop(self):
        pygame.mixer.music.stop()
