import pygame
from typing import TYPE_CHECKING
from arsenal import Arsenal

# Prevent circular imports for type hinting
if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class Ship:
    """A class to manage the ship."""
    def __init__(self, ai_game: 'AlienInvasion', arsenal: Arsenal) -> None:
        """Initialize the ship and set the starting position."""
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.boundaries = ai_game.screen.get_rect()
        # Load the ship image to the size defined in settings
        self.image = pygame.image.load(self.settings.ship_file)
        self.image = pygame.transform.scale(self.image, (self.settings.ship_width, self.settings.ship_height))
        self.rect = self.image.get_rect()

        # Start each ship at the bottom of the center
        self.rect.midbottom = self.boundaries.midbottom

        # Movement flags
        self.moving_right: bool = False
        self.moving_left: bool = False

        #Store decimal value for horizontal position
        self.x: float = float(self.rect.x)
        self.arsenal = arsenal

    def update(self) -> None:
        """Update the ship position based on movement flags and boundaries."""
        if self.moving_right and self.rect.right < self.boundaries.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        self.rect.x = int(self.x)
        self.arsenal.update_arsenal()

    def fire(self) -> bool:
        """Tell the arsenal to fire a bullet."""
        return self.arsenal.fire_bullet()

    def draw(self) -> None:
        """draw the ship at its current location"""
        self.screen.blit(self.image, self.rect)
        self.arsenal.draw()
    def center_ship(self) -> None:
        """Center the ship on the bottom of the screen."""
        self.rect.midbottom = self.boundaries.midbottom
        self.x = float(self.rect.x)