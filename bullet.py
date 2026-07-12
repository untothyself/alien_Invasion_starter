import pygame
from pygame.sprite import Sprite
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class Bullet(Sprite):
    """A class to manage bullets fired from the ship."""

    def __init__(self, ai_game: 'AlienInvasion') -> None:
        """Create a bullet object at the ship's current position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Load and scale bullet image
        self.image = pygame.image.load(self.settings.bullet_file)
        self.image = pygame.transform.scale(
            self.image, (self.settings.bullet_width, self.settings.bullet_height)
        )
        self.rect = self.image.get_rect()
        
        # Start each new bullet at the midtop of the ship
        self.rect.midtop = ai_game.ship.rect.midtop
        self.y: float = float(self.rect.y)

    def update(self) -> None:
        """Move the bullet up the screen."""
        self.y -= self.settings.bullet_speed
        self.rect.y = int(self.y)

    def draw_bullet(self) -> None:
        """Draw the bullet to the screen."""
        self.screen.blit(self.image, self.rect)