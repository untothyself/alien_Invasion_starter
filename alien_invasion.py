import sys
import pygame
from settings import Settings
from ship import Ship
from arsenal import Arsenal
from alien_fleet import AlienFleet

class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self) -> None:
        """Initialize the game, load settings, and create game resources."""
        pygame.init()
        self.settings = Settings()
        self.clock = pygame.time.Clock()

        # Set screen dimensions and title from localized settings
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        pygame.display.set_caption(self.settings.name)

        # Load and scale the background image to fit the screen dimensions 
        self.bg = pygame.image.load(self.settings.bg_file)
        self.bg = pygame.transform.scale(
            self.bg, (self.settings.screen_width, self.settings.screen_height)
        )

        # Initialize game objects using dependency injection
        self.arsenal = Arsenal(self)
        self.ship = Ship(self, self.arsenal)
        
        # Replace the single alien with the AlienFleet 
        self.alien_fleet = AlienFleet(self)
        
        # Generate the centered grid of aliens
        self.alien_fleet.create_fleet()

        self.running: bool = True
        pygame.mixer.init()
        self.impact_sound = pygame.mixer.Sound(self.settings.impact_sound)

    def run_game(self) -> None:
        """Start the main loop for the game."""
        while self.running:
            # Process user inputs 
            self._check_events()

            # Update states (ship and arsenal movement)
            self.ship.update() 
            
            #  Coordinate the entire fleet's movement as a single unit
            self.alien_fleet.update_fleet()

            # Refresh and render the display 
            self._update_screen()

            # Ensure the game runs at the frame rate 
            self.clock.tick(self.settings.FPS)

    def _check_events(self) -> None:
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._quit_game()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event: pygame.event.Event) -> None:
        """Respond to specific keypress events."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            self._quit_game()
        elif event.key == pygame.K_SPACE:
            # Tell the ship to attempt to fire a bullet 
            self.ship.fire()

    def _check_keyup_events(self, event: pygame.event.Event) -> None:
        """Respond to key releases to stop movement flags ."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _update_screen(self) -> None:
        """Update images on the screen, and flip to the new screen."""
        # DRAWING ORDER: Background -> Ship (including arsenal) -> Alien Fleet 
        self.screen.blit(self.bg, (0, 0))
        self.ship.draw()
        
        # Draw the programmatically generated fleet 
        self.alien_fleet.draw()

        # Make the most recently drawn screen visible 
        pygame.display.flip()

    def _quit_game(self) -> None:
        """Cleanly exit the game and system process [21]."""
        pygame.quit()
        sys.exit()
    def _ship_hit(self) -> None:
        """Respond to the ship being hit by an alien."""
        # Reset the level for a new attempt
        self._reset_level()
        # Recenter the player ship
        self.ship.center_ship()

    def _reset_level(self) -> None:
        """Clear existing game objects and regenerate the fleet."""
        self.ship.arsenal.bullets.empty()
        self.alien_fleet.fleet.empty()
        self.alien_fleet.create_fleet()
    def _check_collisions(self) -> None:
        """Manage interactions between game entities."""
        # Detect many-to-many collisions between bullets and aliens
        collisions = pygame.sprite.groupcollide(
            self.ship.arsenal.bullets, self.alien_fleet.fleet, True, True
        )
        
        if collisions:
            self.impact_sound.play()

        # Check if any alien hit the ship (one-to-many)
        if self.alien_fleet.check_destroyed_status():
                self._reset_level()
        
        # Check if any alien reached the bottom
        elif self.alien_fleet.check_fleet_bottom():
            self._ship_hit()
if __name__ == '__main__':
    # Create a game instance and run it 
    ai = AlienInvasion()
    ai.run_game()
