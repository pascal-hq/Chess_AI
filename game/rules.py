from typing import List, Tuple
from game.piece import Piece, PieceType, Color
from game.board import Board, Position
from game.move import Move

class Rules:
    def __init__(self, board: Board):
        self.board = board

    # ---------------- Helpers ----------------
    def in_bounds(self, pos: Position) -> bool:
        row, col = pos
        return 0 <= row < 8 and 0 <= col < 8

    def is_opponent(self, piece: Piece, other: Piece) -> bool:
        return other is not None and piece.color != other.color

    # ---------------- Move Generation ----------------
    def generate_pseudo_legal_moves(self, color: Color) -> List[Move]:
        moves = []
        for row in range(8):
            for col in range(8):
                piece = self.board.get_piece((row, col))
                if piece and piece.color == color:
                    moves.extend(self.get_piece_moves(piece, (row, col)))
        return moves

    def get_piece_moves(self, piece: Piece, pos: Position) -> List[Move]:
        if piece.type == PieceType.PAWN:
            return self.pawn_moves(piece, pos)
        elif piece.type == PieceType.ROOK:
            return self.straight_line_moves(piece, pos, [(-1,0),(1,0),(0,-1),(0,1)])
        elif piece.type == PieceType.BISHOP:
            return self.straight_line_moves(piece, pos, [(-1,-1),(-1,1),(1,-1),(1,1)])
        elif piece.type == PieceType.QUEEN:
            return self.straight_line_moves(piece, pos, [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)])
        elif piece.type == PieceType.KNIGHT:
            return self.knight_moves(piece, pos)
        elif piece.type == PieceType.KING:
            return self.king_moves(piece, pos)
        return []

    # ---------------- Pawn Moves ----------------
    def pawn_moves(self, piece: Piece, pos: Position) -> List[Move]:
        moves = []
        row, col = pos
        direction = -1 if piece.color == Color.WHITE else 1
        start_row = 6 if piece.color == Color.WHITE else 1

        # Forward 1
        forward1 = (row + direction, col)
        if self.in_bounds(forward1) and self.board.is_empty(forward1):
            # Promotion
            if forward1[0] in [0, 7]:
                for promo in ['q','r','b','n']:
                    moves.append(Move(start=pos, end=forward1, piece=piece, promotion=promo))
            else:
                moves.append(Move(start=pos, end=forward1, piece=piece))

            # Forward 2
            forward2 = (row + 2*direction, col)
            if row == start_row and self.board.is_empty(forward2):
                moves.append(Move(start=pos, end=forward2, piece=piece))

        # Captures
        for dc in [-1,1]:
            capture_pos = (row + direction, col + dc)
            if self.in_bounds(capture_pos):
                target = self.board.get_piece(capture_pos)
                if self.is_opponent(piece, target):
                    # Promotion capture
                    if capture_pos[0] in [0,7]:
                        for promo in ['q','r','b','n']:
                            moves.append(Move(start=pos, end=capture_pos, piece=piece, captured=target, promotion=promo))
                    else:
                        moves.append(Move(start=pos, end=capture_pos, piece=piece, captured=target))

        # En passant
        if self.board.en_passant_target:
            ep_row, ep_col = self.board.en_passant_target
            if ep_row == row + direction and abs(ep_col - col) == 1:
                captured = self.board.get_piece((row, ep_col))
                moves.append(Move(start=pos, end=(ep_row, ep_col), piece=piece, captured=captured, is_en_passant=True))

        return moves

    # ---------------- Straight-line Moves (Rook, Bishop, Queen) ----------------
    def straight_line_moves(self, piece: Piece, pos: Position, directions: List[Tuple[int,int]]) -> List[Move]:
        moves = []
        for dr, dc in directions:
            r, c = pos
            while True:
                r += dr
                c += dc
                if not self.in_bounds((r,c)):
                    break
                target = self.board.get_piece((r,c))
                if target is None:
                    moves.append(Move(start=pos, end=(r,c), piece=piece))
                elif self.is_opponent(piece, target):
                    moves.append(Move(start=pos, end=(r,c), piece=piece, captured=target))
                    break
                else:
                    break
        return moves

    # ---------------- Knight Moves ----------------
    def knight_moves(self, piece: Piece, pos: Position) -> List[Move]:
        moves = []
        row, col = pos
        deltas = [(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]
        for dr, dc in deltas:
            r, c = row + dr, col + dc
            if self.in_bounds((r,c)):
                target = self.board.get_piece((r,c))
                if target is None or self.is_opponent(piece, target):
                    moves.append(Move(start=pos, end=(r,c), piece=piece, captured=target))
        return moves

    # ---------------- King Moves ----------------
    def king_moves(self, piece: Piece, pos: Position) -> List[Move]:
        moves = []
        row, col = pos
        deltas = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
        for dr, dc in deltas:
            r, c = row + dr, col + dc
            if self.in_bounds((r,c)):
                target = self.board.get_piece((r,c))
                if target is None or self.is_opponent(piece, target):
                    moves.append(Move(start=pos, end=(r,c), piece=piece, captured=target))

        # Castling
        if not piece.has_moved:
            if self.can_castle_kingside(piece.color):
                moves.append(Move(start=pos, end=(row, col+2), piece=piece, is_castling=True))
            if self.can_castle_queenside(piece.color):
                moves.append(Move(start=pos, end=(row, col-2), piece=piece, is_castling=True))

        return moves

    # ---------------- Castling Helpers ----------------
    def can_castle_kingside(self, color: Color) -> bool:
        row = 7 if color == Color.WHITE else 0
        # Rook exists and unmoved
        rook = self.board.get_piece((row,7))
        if rook is None or rook.has_moved or rook.type != PieceType.ROOK or rook.color != color:
            return False
        # Squares between king and rook empty
        if not all(self.board.is_empty((row,c)) for c in [5,6]):
            return False
        return True

    def can_castle_queenside(self, color: Color) -> bool:
        row = 7 if color == Color.WHITE else 0
        rook = self.board.get_piece((row,0))
        if rook is None or rook.has_moved or rook.type != PieceType.ROOK or rook.color != color:
            return False
        if not all(self.board.is_empty((row,c)) for c in [1,2,3]):
            return False
        return True
