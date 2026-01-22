from typing import Optional, Tuple
from game.piece import Piece

Position = Tuple[int, int]

class Move:
    def __init__(
        self,
        start: Position,
        end: Position,
        piece: Piece,
        captured: Optional[Piece] = None,
        promotion: Optional[str] = None,
        is_castling: bool = False,
        is_en_passant: bool = False,
        previous_en_passant: Optional[Position] = None,
        previous_castling_rights: Optional[dict] = None,
        previous_has_moved: Optional[bool] = None
    ):
        self.start = start
        self.end = end
        self.piece = piece
        self.captured = captured
        self.promotion = promotion
        self.is_castling = is_castling
        self.is_en_passant = is_en_passant
        self.previous_en_passant = previous_en_passant
        self.previous_castling_rights = previous_castling_rights
        self.previous_has_moved = previous_has_moved

    def is_capture(self) -> bool:
        return self.captured is not None

    def notation(self) -> str:
        """Simple algebraic notation (without disambiguation)."""
        start_file = chr(self.start[1] + ord('a'))
        start_rank = str(8 - self.start[0])
        end_file = chr(self.end[1] + ord('a'))
        end_rank = str(8 - self.end[0])
        promo = f"={self.promotion.upper()}" if self.promotion else ""
        return f"{start_file}{start_rank}{end_file}{end_rank}{promo}"

    def __repr__(self):
        return f"<Move {self.notation()}>"
