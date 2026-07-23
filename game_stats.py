from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion


class GameStats:
    """Track statistics that can change while the game is running."""

    def __init__(self, ai_game: 'AlienInvasion') -> None:
        """Initialize the game's statistics."""
        self.settings = ai_game.settings
        self.high_score: int = 0
        self.game_active: bool = False
        self.reset_stats()

    def reset_stats(self) -> None:
        """Reset statistics that should restart with each new game."""
        self.ships_left: int = self.settings.starting_ship_count
        self.score: int = 0
        self.max_score: int = 0
