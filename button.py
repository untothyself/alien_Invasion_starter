import pygame.font
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class Button:
    """A class to build buttons for the game."""
    def __init__(self, ai_game: 'AlienInvasion', msg: str) -> None:
        """Initialize button attributes."""
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.font = pygame.font.Font(None, 48)
        
        # Center the button on the screen
        self.rect = pygame.Rect(0, 0, self.settings.button_w, self.settings.button_h)
        self.rect.center = self.screen.get_rect().center
        
        # Prep the button message
        self._prep_msg(msg)

    def _prep_msg(self, msg: str) -> None:
        """Turn msg into a rendered image and center text on the button."""
        self.msg_image = self.font.render(msg, True, self.settings.text_color, self.settings.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self) -> None:
        """Draw blank button and then draw message."""
        self.screen.fill(self.settings.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

    def check_clicked(self, mouse_pos: tuple[int, int]) -> bool:
        """Return True if the mouse click position is within the button."""
        return self.rect.collidepoint(mouse_pos)