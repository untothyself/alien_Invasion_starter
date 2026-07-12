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
    

    def _find_existing_dir(self, candidates: list[str]) -> Path:
        """Return the first existing asset directory from the given candidates."""
        for name in candidates:
            path = self.base_dir / name
            if path.exists():
                return path
        return self.base_dir / candidates[0]

    def _resolve_asset_path(self, subfolder: str, candidates: list[str]) -> str:
        """Return the first existing asset path from a list of candidates."""
        folder = self.assets_dir / subfolder
        for name in candidates:
            candidate = folder / name
            if candidate.exists():
                return str(candidate)
        return str(folder / candidates[0])
        
