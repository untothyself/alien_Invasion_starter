import pygame
from bullet import Bullet
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class Arsenal:
    """A class to manage the ship's armament loadout."""

    def __init__(self, ai_game: 'AlienInvasion') -> None:
        self.ai_game = ai_game
        self.settings = ai_game.settings
        self.bullets = pygame.sprite.Group()

    def update_arsenal(self) -> None:
        """Update bullet positions and remove off-screen bullets."""
        self.bullets.update()
        
        # Clean up bullets that moved off the top of the screen
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    def fire_bullet(self) -> bool:
        """Create a new bullet and add it to the bullets group if limit allows."""
        if len(self.bullets) < self.settings.bullet_amount:
            new_bullet = Bullet(self.ai_game)
            self.bullets.add(new_bullet)
            return True
        return False

    def draw(self) -> None:
        """Draw all bullets in the arsenal."""
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()