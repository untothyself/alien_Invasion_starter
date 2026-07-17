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
        #added ship speed
        self.ship_speed: float = 5.0
        self.bullet_file: str = self._resolve_asset_path(
            "images", ["laserBlast.png", "laser_blast.png", "beams.png"]
        )
        self.laser_sound: str = self._resolve_asset_path(
            "sound", ["laser.mp3", "impactSound.mp3"], fallback_subfolder="sounds"
        )
        # bullet performance and limit
        self.bullet_speed: float = 7.0
        self.bullet_width: int = 25
        self.bullet_height: int = 80
        self.bullet_amount: int = 5# limit of how many bullets on screen at once.
        #alien settings
        self.alien_file: str = self._resolve_asset_path("images", ["enemy_4.png"])
        self.alien_w: int = 40
        self.alien_h: int = 40
        self.fleet_speed: float = 2.0 
        self.fleet_direction: int = 1 #1= right, -1 = left
        self.fleet_drop_speed: int = 10 
    

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
        
