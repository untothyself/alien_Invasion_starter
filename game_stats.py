from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class GameStats:
    """Track volatile statistics for the game session."""

    def __init__(self, ai_game: 'AlienInvasion') -> None:
        """Initialize statistics based on game settings."""
        self.settings = ai_game.settings
        self.ships_left: int = self.settings.starting_ship_count
        self.game_active: bool = False