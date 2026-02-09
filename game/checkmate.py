from typing import TYPE_CHECKING
from game.piece import Color

if TYPE_CHECKING:
    from game.state import GameState


def is_checkmate(state: "GameState", color: Color) -> bool:
    """
    Returns True if the player of `color` is in checkmate.

    Checkmate occurs when the king is in check and there are no legal moves.
    """
    return state.is_in_check(color) and len(state.get_legal_moves()) == 0


def is_stalemate(state: "GameState", color: Color) -> bool:
    """
    Returns True if the player of `color` is in stalemate.

    Stalemate occurs when the king is NOT in check, but there are no legal moves.
    """
    return not state.is_in_check(color) and len(state.get_legal_moves()) == 0
