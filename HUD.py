import pygame.font
import json
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion


class HUD:
    """A class to report scoring information on the game screen."""
    
    def __init__(self, ai_game: 'AlienInvasion') -> None:
        """Initialize scorekeeping attributes."""
        self.screen = ai_game.screen
        self.stats = ai_game.stats
        self.settings = ai_game.settings
        
        # Set up font for rendering score text
        self.font = pygame.font.Font(None, self.settings.HUD_font_size)
        
        # Score file path for persistent storage
        self.score_file: Path = self.settings.base_dir / 'Assets' / 'file' / 'scores.json'
        
        # Load high score from JSON file
        self._load_high_score()
        
        # Initialize rendered score images
        self.score_image = None
        self.max_score_image = None
        self.high_score_image = None
        self.score_rect = None
        self.max_score_rect = None
        self.high_score_rect = None
        
        # Initial render of all score images
        self.update_scores()

    def _load_high_score(self) -> None:
        """Load high score from JSON file; default to 0 if file is empty or missing."""
        try:
            if self.score_file.exists() and self.score_file.stat().st_size > 0:
                with open(self.score_file, 'r') as f:
                    data = json.load(f)
                    self.stats.high_score = data.get('high_score', 0)
            else:
                self.stats.high_score = 0
        except (json.JSONDecodeError, FileNotFoundError):
            # If file is corrupted or missing, start with 0
            self.stats.high_score = 0

    def _save_high_score(self) -> None:
        """Save high score to JSON file for persistence."""
        self.score_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.score_file, 'w') as f:
            json.dump({'high_score': self.stats.high_score}, f)

    def update_scores(self) -> None:
        """Update the rendered images for current score, max score, and high score."""
        # Render current score in white
        self.score_image = self.font.render(
            f"Score: {self.stats.score}", True, self.settings.text_color
        )
        self.score_rect = self.score_image.get_rect()
        self.score_rect.topleft = (10, 10)
        
        # Render max score (current level) in yellow
        self.max_score_image = self.font.render(
            f"Max: {self.stats.max_score}", True, (255, 255, 0)
        )
        self.max_score_rect = self.max_score_image.get_rect()
        self.max_score_rect.topleft = (10, 35)
        
        # Render high score in cyan
        self.high_score_image = self.font.render(
            f"High: {self.stats.high_score}", True, (0, 255, 255)
        )
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.topleft = (10, 60)

    def draw_scores(self) -> None:
        """Display score, max score, and high score on screen."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.max_score_image, self.max_score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)

    def check_high_score(self) -> None:
        """Check if current score exceeds high score; update and save if needed."""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self._save_high_score()
            self.update_scores()
