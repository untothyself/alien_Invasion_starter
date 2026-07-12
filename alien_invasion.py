import sys
import pygame
from settings import Settings
from ship import Ship # import new class
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
        #load and scale the background image to fit the screen
        self.bg = pygame.image.load(self.settings.bg_file)
        self.bg = pygame.transform.scale(
            self.bg, (self.settings.screen_width, self.settings.screen_height)
        )
        # initialize the ship instance
        self.ship = Ship(self)
        self.running: bool = True


        
    def run_game(self) -> None:
        """Start the main loop for the game."""
        while self.running:
            # Process events
            self._check_events()
            #update screem
            self._update_screen()
            #Make sure the game runs at the FPS
            self.clock.tick(self.settings.FPS)

    def _check_events(self) -> None:
        """respond to keys and mouse"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._quit_game()
    
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
