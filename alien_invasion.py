import sys
import pygame
from settings import Settings
from ship import Ship
from arsenal import Arsenal
from alien_fleet import AlienFleet
from game_stats import GameStats
from button import Button
from HUD import HUD
from time import sleep

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
        self.stats = GameStats(self)
        self.play_button = Button(self, "Play")
        self.hud = HUD(self)

    def run_game(self) -> None:
        """Main game loop."""
        while self.running:
            self._check_events()
            
            # Only update movement and collisions if game is active
            if self.stats.game_active:
                self.ship.update()
                self.alien_fleet.update_fleet()
                self._check_collisions()

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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos: tuple[int, int]) -> None:
        """Start a new game when the player clicks Play."""
        if self.play_button.check_clicked(mouse_pos) and not self.stats.game_active:
            self.stats.game_active = True
            pygame.mouse.set_visible(False) # Hide the cursor
            # Reset scores for new game
            self.stats.score = 0
            self.stats.max_score = 0
            self.settings.initialize_dynamic_settings()  # Reset difficulty to base
            self._reset_level(level_up=False)

    def _check_keydown_events(self, event: pygame.event.Event) -> None:
        """Respond to specific keypress events."""
        if self.stats.game_active:
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
        # DRAWING ORDER: Background -> Ship (including arsenal) -> Alien Fleet -> HUD
        self.screen.blit(self.bg, (0, 0))
        self.ship.draw()
        
        # Draw the programmatically generated fleet 
        self.alien_fleet.draw()
        
        # Draw score HUD during gameplay
        if self.stats.game_active:
            self.hud.draw_scores()

        # Draw the Play button when the game is inactive
        if not self.stats.game_active:
            self.play_button.draw_button()

        # Make the most recently drawn screen visible 
        pygame.display.flip()

    def _quit_game(self) -> None:
        """Cleanly exit the game and system process"""
        pygame.quit()
        sys.exit()
    def _ship_hit(self) -> None:
        """Respond to ship collision by reducing lives or ending game."""
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self._reset_level(level_up=False)
            self.ship.center_ship()
            sleep(0.5) # Pause to let the player react
        else:
            self.stats.game_active = False # Trigger Game Over stat
            pygame.mouse.set_visible(True)

    def _reset_level(self, level_up: bool = True) -> None:
        """Clear existing game objects and regenerate the fleet."""
        # Update max_score and check for high score before resetting
        if self.stats.score > self.stats.max_score:
            self.stats.max_score = self.stats.score
        self.hud.check_high_score()
        
        # Increase difficulty only when leveling up (not on initial game start)
        if level_up:
            self.settings.increase_difficulty()
        
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
            # Add 10 points per alien destroyed
            for aliens_hit in collisions.values():
                self.stats.score += len(aliens_hit) * 10
            self.hud.update_scores()  # Refresh HUD display

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
