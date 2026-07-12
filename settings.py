from pathlib import Path
import os

class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self) -> None:
        """Initialize the game's static settings."""
        # Screen settings
        self.name: str = "Alien Invasion"
        self.screen_width: int=1200
        self.screen_height: int = 800
        self.FPS: int=60
        # File path using path-library
        self.cwd: Path = Path(os.getcwd())
        self.assets_dir: Path = self.cwd / 'assets'
        self.bg_file: str = str(self.assets_dir / 'images' / 'starbases_now.png')

        #ship Settings 1
        self.ship_file: str = str(self.assets.dir / 'images' / 'ship_to_nob.png')
        self.ship_width: int=60
        self.ship_height: int=40
        
