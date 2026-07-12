import pygame
from typing import TYPE_CHECKING

# Prevent circular imports for type hinting
if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class Ship:
    """A class to manage the ship."""
    def __init__(self, ai_game: 'AlienInvasion') -> None:
        """Initialize the ship and set the starting position."""
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()
        # Load the ship image to the size definrf in settings
        self.image = pygame.transform.scale(self.image, (self.settings.ship_width, self.settings.ship_height))
        self.rect = self.image.get_rect()

        # Start each ship at the bottom of the center
        self.rect.midbottom = self.screen_rect.midbottom
    def draw(self) -> None:
        """draw the ship at its current location"""
        self.screen.blit(self.image, self.rect)