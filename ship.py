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

        def update(self) -> None:
            """Update the ship position based on movement flags and boundries"""
            #check flags and boundries before moving
            if self.moving_right and self.rect.right < self.boundaries.right: self.x += self.settings.ship_speed
            if self.moving_left and self.rect.left > 0: self.x -= self.settings.ship_speed

            # Update rect object from float position
            self.rect.x = int(self.x)

    def draw(self) -> None:
        """draw the ship at its current location"""
        self.screen.blit(self.image, self.rect)