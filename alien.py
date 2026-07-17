import pygame
from pygame.sprite import Sprite
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_fleet import AlienFleet

class Alien(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, fleet: 'AlienFleet', x: float, y: float) -> None:
        """Initialize the alien at the fleet-calculated position."""
        super().__init__()
        self.fleet = fleet
        self.settings = fleet.settings
        self.screen = fleet.game.screen
        self.boundaries = self.screen.get_rect()

        self.image = pygame.image.load(self.settings.alien_file)
        self.image = pygame.transform.scale(
            self.image, (self.settings.alien_w, self.settings.alien_h)
        )
        self.rect = self.image.get_rect()

        # Position synchronization
        self.x = x
        self.y = y
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def check_edges(self) -> bool:
        """Return True if alien is at the left or right edge."""
        return (self.rect.right >= self.boundaries.right or self.rect.left <= 0)

    def update(self) -> None:
        """Move the alien horizontally based on fleet coordination."""
        self.x += self.settings.fleet_speed * self.fleet.fleet_direction
        self.rect.x = int(self.x)

    def draw_alien(self) -> None:
        """Draw the alien to the screen."""
        self.screen.blit(self.image, self.rect)