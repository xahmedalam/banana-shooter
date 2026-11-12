import pygame


class AudioManager:
    @classmethod
    def pre_init(cls):
        # Fix sound lag
        pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=4096)

    def __init__(
        self, mute: bool = False, bg_volume: float = 0.5, sfx_volume: float = 1.0
    ) -> None:
        # Settings
        self.mute = mute
        self.bg_volume = bg_volume
        self.sfx_volume = sfx_volume
        # SFXs
        self.sfxs: list[pygame.mixer.Sound] = []

        # Bg sound
        pygame.mixer.music.load("src/assets/audio/bg.ogg")
        pygame.mixer.music.set_volume(self.bg_volume)

        # Fire
        self.bullet_sound = pygame.mixer.Sound("src/assets/audio/bullet.ogg")
        self.bullet_sound.set_volume(self.sfx_volume)
        self.sfxs.append(self.bullet_sound)

        # Enemy damage
        self.enemy_damage_sound = pygame.mixer.Sound(
            "src/assets/audio/enemy-damage.ogg"
        )
        self.enemy_damage_sound.set_volume(self.sfx_volume)
        self.sfxs.append(self.enemy_damage_sound)

        # Player damage
        self.player_damage_sound = pygame.mixer.Sound(
            "src/assets/audio/player-damage.ogg"
        )
        self.player_damage_sound.set_volume(self.sfx_volume)
        self.player_damage_last_change = pygame.time.get_ticks()
        self.sfxs.append(self.player_damage_sound)

    def toggle_mute(self):
        if self.mute:
            self.mute = False
        else:
            self.mute = True

    def check_mute(self):
        if self.mute:
            pygame.mixer.music.set_volume(0)
            for sfx in self.sfxs:
                sfx.set_volume(0)
        else:
            pygame.mixer.music.set_volume(self.bg_volume)
            for sfx in self.sfxs:
                sfx.set_volume(self.sfx_volume)

    def bg_play(self):
        pygame.mixer.music.play(-1)

    def bg_stop(self):
        pygame.mixer.music.stop()

    def play_bullet(self):
        self.bullet_sound.play()

    def play_enemy_damage(self):
        self.enemy_damage_sound.play()

    def play_player_damage(self):
        # Play with 500ms cool down
        if pygame.time.get_ticks() - self.player_damage_last_change >= 500:
            self.player_damage_sound.play()
            self.player_damage_last_change = pygame.time.get_ticks()
