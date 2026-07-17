import pygame
from pygame.sprite import Sprite
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class Alien(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, ai_game: 'AlienInvasion', x: float, y: float) -> None:
        """Initialize the alien and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Load the alien image and get its rect
        self.image = pygame.image.load(self.settings.alien_file)
        self.image = pygame.transform.scale(
            self.image, (self.settings.alien_w, self.settings.alien_h)
        )
        self.rect = self.image.get_rect()

        # Start each new alien at the coordinates passed in
        self.rect.x = int(x)
        self.rect.y = int(y)

        # Store the alien's exact horizontal position
        self.x = float(self.rect.x)

    def draw_alien(self) -> None:
        """Draw the alien at its current location."""
        self.screen.blit(self.image, self.rect)