from typing import List, Tuple
from game.piece import Piece, PieceType, Color
from game.board import Board
from game.move import Move, Position

class Rules:
    def __init__(self, board: Board):
        self.board = board

    # ---------- Helper ----------
    def in_bounds(self, pos: Position) -> bool:
        row, col = pos
        return 0 <= row < 8 and 0 <= col < 8

    def is_opponent(self, piece: Piece, other: Piece) -> bool:
        return piece.color != other.color

    # ---------- Move Generation ----------
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
            return self.straight_line_moves(piece, pos, directions=[(-1,0),(1,0),(0,-1),(0,1)])
        elif piece.type == PieceType.BISHOP:
            return self.straight_line_moves(piece, pos, directions=[(-1,-1),(-1,1),(1,-1),(1,1)])
        elif piece.type == PieceType.QUEEN:
            return self.straight_line_moves(piece, pos, directions=[(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)])
        elif piece.type == PieceType.KNIGHT:
            return self.knight_moves(piece, pos)
        elif piece.type == PieceType.KING:
            return self.king_moves(piece, pos)
        return []

    # ---------- Piece-specific move helpers ----------
    def pawn_moves(self, piece: Piece, pos: Position) -> List[Move]:
        moves = []
        row, col = pos
        direction = -1 if piece.color == Color.WHITE else 1
        start_row = 6 if piece.color == Color.WHITE else 1

        # Forward 1
        forward1 = (row + direction, col)
        if self.in_bounds(forward1) and self.board.is_empty(forward1):
            moves.append(Move(start=pos, end=forward1, piece=piece))
            # Forward 2 from start
            forward2 = (row + 2*direction, col)
            if row == start_row and self.board.is_empty(forward2):
                moves.append(Move(start=pos, end=forward2, piece=piece))

        # Captures
        for dc in [-1, 1]:
            capture_pos = (row + direction, col + dc)
            if self.in_bounds(capture_pos):
                target = self.board.get_piece(capture_pos)
                if target and self.is_opponent(piece, target):
                    moves.append(Move(start=pos, end=capture_pos, piece=piece, captured=target))

        # TODO: en passant / promotion handled later
        return moves

    def straight_line_moves(self, piece: Piece, pos: Position, directions: List[Tuple[int,int]]) -> List[Move]:
        moves = []
        for dr, dc in directions:
            r, c = pos
            while True:
                r += dr
                c += dc
                if not self.in_bounds((r, c)):
                    break
                target = self.board.get_piece((r, c))
                if target is None:
                    moves.append(Move(start=pos, end=(r, c), piece=piece))
                elif self.is_opponent(piece, target):
                    moves.append(Move(start=pos, end=(r, c), piece=piece, captured=target))
                    break
                else:  # Friendly piece blocks
                    break
        return moves

    def knight_moves(self, piece: Piece, pos: Position) -> List[Move]:
        moves = []
        row, col = pos
        deltas = [(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]
        for dr, dc in deltas:
            r, c = row + dr, col + dc
            if self.in_bounds((r,c)):
                target = self.board.get_piece((r,c))
                if target is None or self.is_opponent(piece, target):
                    moves.append(Move(start=pos, end=(r,c), piece=piece, captured=target if target else None))
        return moves

    def king_moves(self, piece: Piece, pos: Position) -> List[Move]:
        moves = []
        row, col = pos
        deltas = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
        for dr, dc in deltas:
            r, c = row + dr, col + dc
            if self.in_bounds((r,c)):
                target = self.board.get_piece((r,c))
                if target is None or self.is_opponent(piece, target):
                    moves.append(Move(start=pos, end=(r,c), piece=piece, captured=target if target else None))
        # TODO: castling handled later
        return moves
