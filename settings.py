from pathlib import Path


class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self) -> None:
        """Initialize the game's static settings."""
        # Screen settings
        self.name: str = "Alien Invasion"
        self.screen_width: int = 1200
        self.screen_height: int = 800
        self.FPS: int = 60

        self.base_dir: Path = Path(__file__).resolve().parent
        self.assets_dir: Path = self._find_existing_dir(["Assets", "assets"])
        self.bg_file: str = self._resolve_asset_path(
            "images", ["Starbasesnow.png", "starbases_now.png", "starbasesnow.png"]
        )

        # ship Settings
        self.ship_file: str = self._resolve_asset_path(
            "images", ["ship.png", "ship2.png", "ship2(no bg).png", "ship_to_nob.png"]
        )
        self.ship_width: int = 60
        self.ship_height: int = 40
        self.bullet_file: str = self._resolve_asset_path(
            "images", ["laserBlast.png", "laser_blast.png", "beams.png"]
        )
        self.laser_sound: str = self._resolve_asset_path(
            "sound", ["laser.mp3", "impactSound.mp3"], fallback_subfolder="sound"
        )
        # bullet performance and limit
        self.bullet_width: int = 25
        self.bullet_height: int = 80
        self.bullet_amount: int = 5 # limit of how many bullets on screen at once.
        # alien settings
        self.alien_file: str = self._resolve_asset_path("images", ["enemy_4.png"])
        self.alien_w: int = 40
        self.alien_h: int = 40
        self.fleet_drop_speed: int = 10 # pixels alien fleet drops when hitting screen edge
        
        # difficulty scaling: multiplier for speed increases per level
        self.difficulty_scale: float = 1.05 
        
        self.impact_sound: str = self._resolve_asset_path("sound", ["impactSound.mp3"])
        self.starting_ship_count: int = 3
        
        # button settings
        self.button_w = 200
        self.button_h = 50
        self.button_color = (0, 135, 0) # green
        
        self.text_color = (255, 255, 255) # white
        self.button_font_size = 48
        self.HUD_font_size = 20
        self.font_file = Path.cwd() / 'Assets' / 'Fonts' / 'Silkscreen'
        
        # Initialize dynamic settings that change during gameplay
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self) -> None:
        """Set up settings that scale with difficulty as levels progress."""
        # Player and projectile speeds
        self.ship_speed: float = 5.0
        self.bullet_speed: float = 7.0
        # Alien fleet speed and direction
        self.alien_speed: float = 2.0
        self.fleet_direction: int = 1 # 1 = right; -1 = left

    def increase_difficulty(self) -> None:
        """Increase speed settings by difficulty scale when level cleared."""
        self.ship_speed *= self.difficulty_scale
        self.bullet_speed *= self.difficulty_scale
        self.alien_speed *= self.difficulty_scale

    def _find_existing_dir(self, candidates: list[str]) -> Path:
        """Return the first existing asset directory from the given candidates."""
        for name in candidates:
            path = self.base_dir / name
            if path.exists():
                return path
        return self.base_dir / candidates[0]

    def _resolve_asset_path(self, subfolder: str, candidates: list[str], fallback_subfolder: str | None = None) -> str:
        """Return the first existing asset path from a list of candidates."""
        folder = self.assets_dir / subfolder
        for name in candidates:
            candidate = folder / name
            if candidate.exists():
                return str(candidate)

        if fallback_subfolder is not None:
            fallback_folder = self.assets_dir / fallback_subfolder
            for name in candidates:
                candidate = fallback_folder / name
                if candidate.exists():
                    return str(candidate)

        return str(folder / candidates[0])
        
