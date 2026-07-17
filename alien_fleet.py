import pygame
from alien import Alien
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class AlienFleet:
    """A class to manage the entire alien fleet and its movement."""

    def __init__(self, ai_game: 'AlienInvasion') -> None:
        """Initialize the fleet and its movement settings."""
        self.game = ai_game
        self.settings = ai_game.settings
        self.fleet = pygame.sprite.Group()
        
        # Initialize fleet direction from settings (1 for right, -1 for left)
        self.fleet_direction: int = self.settings.fleet_direction

    def create_fleet(self) -> None:
        """Coordinate the calculation and generation of the centered grid of aliens."""
        # Determine how many aliens fit based on screen and alien dimensions
        fleet_w, fleet_h = self._calculate_fleet_size()
        
        # Calculate centering offsets for the grid
        x_offset, y_offset = self._calculate_offsets(fleet_w, fleet_h)
        
        # Generate the actual fleet objects in a rectangle pattern
        self._create_rectangle_fleet(fleet_w, fleet_h, x_offset, y_offset)

    def _calculate_fleet_size(self) -> tuple[int, int]:
        """Determine the number of aliens that fit horizontally and vertically."""
        # Calculate horizontal count based on screen width
        width_count = self.settings.screen_width // self.settings.alien_w
        
        # Calculate vertical count, filling only the top half of the screen
        available_h = self.settings.screen_height // 2
        height_count = available_h // self.settings.alien_h
        
        # Adjust counts to ensure they are odd to facilitate better centering 
        width_count -= 1 if width_count % 2 == 0 else 2 
        height_count -= 1 if height_count % 2 == 0 else 2
        
        return int(width_count), int(height_count)

    def _calculate_offsets(self, fleet_w: int, fleet_h: int) -> tuple[int, int]:
        """Determine centering offsets for the fleet grid."""
        # Horizontal space occupied by the fleet
        horizontal_space = fleet_w * self.settings.alien_w
        x_offset = (self.settings.screen_width - horizontal_space) // 2
        
        # Vertical space occupied by the fleet in the top half of the screen
        half_screen_h = self.settings.screen_height // 2
        vertical_space = fleet_h * self.settings.alien_h
        y_offset = (half_screen_h - vertical_space) // 2
        
        return int(x_offset), int(y_offset)

    def _create_rectangle_fleet(self, fleet_w: int, fleet_h: int, x_off: int, y_off: int) -> None:
        """Use nested loops to place individual aliens with proper spacing."""
        for row in range(fleet_h):
            for col in range(fleet_w):
                # Skip even indices to create gaps between individual aliens
                if row % 2 == 0 or col % 2 == 0:
                    continue
                
                # Calculate current position including the initial offset 
                curr_x = col * self.settings.alien_w + x_off
                curr_y = row * self.settings.alien_h + y_off
                
                # Create and add the alien to the group 
                new_alien = Alien(self, curr_x, curr_y)
                self.fleet.add(new_alien)

    def update_fleet(self) -> None:
        """Respond to edge hits, then drop and update all aliens in the group."""
        # Check if any member of the fleet has hit a screen edge 
        if self._check_fleet_edges():
            self._drop_fleet()
            self.fleet_direction *= -1  # Reverse direction for the whole group 
            
        # Call the update method on the entire sprite group 
        self.fleet.update()

    def _check_fleet_edges(self) -> bool:
        """Return True if any alien in the fleet has hit a boundary."""
        for alien in self.fleet.sprites():
            if alien.check_edges():
                return True  # Break early once any single alien hits an edge 
        return False

    def _drop_fleet(self) -> None:
        """Shift every alien in the fleet downward."""
        for alien in self.fleet.sprites():
            # Update the internal float position and then sync the rect
            alien.y += self.settings.fleet_drop_speed
            alien.rect.y = int(alien.y)

    def draw(self) -> None:
        """Draw all aliens currently in the fleet group to the screen."""
        for alien in self.fleet.sprites():
            alien.draw_alien()
    def check_fleet_bottom(self) -> bool:
        """Return True if any alien has reached the bottom of the screen."""
        for alien in self.fleet.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                return True
        return False
