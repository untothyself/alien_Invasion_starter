import sys
import pygame
from settings import Settings
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
        self.running: bool = True


        
    def run_game(self) -> None:
        """Start the main loop for the game."""
        while self.running:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._quit_game()

            # Draw background at the origin
            self.screen.blit(self.bg, (0, 0))
            # Make the most recebtly drawn screen visible
            pygame.display.flip()
            #Make sure the game runs at the FPS
            self.clock.tick(self.settings.FPS)
    def _quit_game(self) -> None:
        """clean exit game."""
        pygame.quit()
        sys.exit()
            

if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
