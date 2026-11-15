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
        self.sfxs.append(self.bullet_sound)

        # Enemy damage
        self.enemy_damage_sound = pygame.mixer.Sound(
            "src/assets/audio/enemy-damage.ogg"
        )
        self.sfxs.append(self.enemy_damage_sound)

        # Player damage
        self.player_damage_sound = pygame.mixer.Sound(
            "src/assets/audio/player-damage.ogg"
        )
        self.player_damage_last_change = pygame.time.get_ticks()
        self.sfxs.append(self.player_damage_sound)

        # Bonus slurp
        self.bonus_slurp_sound = pygame.mixer.Sound("src/assets/audio/bonus-slurp.ogg")
        self.sfxs.append(self.bonus_slurp_sound)

        # Boss damage
        self.boss_damage_sound = pygame.mixer.Sound("src/assets/audio/boss-damage.ogg")
        self.sfxs.append(self.boss_damage_sound)

        # Boss health bar skull destroy
        self.boss_health_bar_skull_destroy_sound = pygame.mixer.Sound(
            "src/assets/audio/bone-break.ogg"
        )
        self.sfxs.append(self.boss_health_bar_skull_destroy_sound)

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

    def play_bg(self, boss_audio: bool = False):
        if boss_audio:
            pygame.mixer.music.load("src/assets/audio/bg-boss-fight.ogg")
            pygame.mixer.music.set_volume(1.0)
        pygame.mixer.music.play(-1)

    def stop_bg(self):
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

    def play_bonus_slurp(self):
        self.bonus_slurp_sound.play()

    def play_boss_damage(self):
        self.boss_damage_sound.play()

    def play_boss_health_bar_skull_destroy(self):
        self.boss_health_bar_skull_destroy_sound.play()
