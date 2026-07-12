import sys
import pygame
from settings import Settings
from ship import Ship # import new class
from arsenal import Arsenal
class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self) -> None:
        """Intialize the game and create rescources"""
        pygame.init()
        self.settings = Settings()
        #control frame rate
        self.clock = pygame.time.Clock()
        #set screen dimensions and tit;e from settings
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        pygame.display.set_caption(self.settings.name)

        #background setup
        self.bg = pygame.image.load(self.settings.bg_file)
        self.bg = pygame.transform.scale(
            self.bg, (self.settings.screen_width, self.settings.screen_height)
        )
        self.running: bool = True
        pygame.mixer.init()
        self.laser_sound = pygame.mixer.Sound(self.settings.laser_sound)
        self.laser_sound.set_volume(0.7)
        # intialize aresenal and inject in ship
        self.arsenal = Arsenal(self)
        # initialize the ship instance
        self.ship = Ship(self, self.arsenal)
    


        
    def run_game(self) -> None:
        """Start the main loop for the game."""
        while self.running:
            # Process events
            self._check_events()
            self.ship.update()
            #update screem
            self._update_screen()
            #Make sure the game runs at the FPS
            self.clock.tick(self.settings.FPS)

    def _check_events(self) -> None:
        """respond to keys and mouse"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._quit_game()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event: pygame.event.Event) -> None:
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:  # Quick quit shortcut
            self._quit_game()
        if event.key == pygame.K_SPACE:
            # Safely call ship.fire if it exists to satisfy static analyzers
            fire_method = getattr(self.ship, "fire", None)
            if callable(fire_method) and fire_method():
                self.laser_sound.play()

    def _check_keyup_events(self, event: pygame.event.Event) -> None:
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
    
    def _update_screen(self) -> None:
        """update images on screen to flip the new screen"""
        #draw background
        self.screen.blit(self.bg, (0, 0))
        #draw ship
        self.ship.draw()
        # make most recent drawn screen visable
        pygame.display.flip()
    
    

    def _quit_game(self) -> None:
        """clean exit game."""
        pygame.quit()
        sys.exit()
            

if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
