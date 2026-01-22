from typing import List, Optional
from game.board import Board, Position
from game.piece import Piece, Color, PieceType
from game.move import Move
from game.rules import Rules
import copy

class GameState:
    def __init__(self):
        self.board = Board()
        self.rules = Rules(self.board)
        self.turn = Color.WHITE
        self.move_history: List[Move] = []
        self.castling_rights = {
            Color.WHITE: {'K': True, 'Q': True},
            Color.BLACK: {'K': True, 'Q': True}
        }
        self.en_passant_target: Optional[Position] = None

    # ---------- Legal Move Generation ----------
    def get_legal_moves(self) -> List[Move]:
        pseudo_moves = self.rules.generate_pseudo_legal_moves(self.turn)
        legal_moves = []
        for move in pseudo_moves:
            self.make_move(move)
            if not self.is_in_check(self.turn):
                legal_moves.append(move)
            self.undo_move()
        return legal_moves

    def is_in_check(self, color: Color) -> bool:
        king_pos = self.board.white_king_pos if color == Color.WHITE else self.board.black_king_pos
        opponent = Color.BLACK if color == Color.WHITE else Color.WHITE
        opponent_moves = self.rules.generate_pseudo_legal_moves(opponent)
        for move in opponent_moves:
            if move.end == king_pos:
                return True
        return False

    # ---------- Move Execution ----------
    def make_move(self, move: Move):
        # Save previous state for undo
        move.previous_en_passant = self.board.en_passant_target
        move.previous_castling_rights = copy.deepcopy(self.castling_rights)
        move.previous_has_moved = move.piece.has_moved

        # Move the piece on board
        self.board.move_piece(move.start, move.end)

        # Update special state
        self.board.en_passant_target = None  # TODO: set for double pawn moves
        # TODO: handle castling, en passant, promotion

        # Update castling rights if king or rook moved
        if move.piece.type == PieceType.KING:
            self.castling_rights[move.piece.color]['K'] = False
            self.castling_rights[move.piece.color]['Q'] = False
        elif move.piece.type == PieceType.ROOK:
            # TODO: update correct rook side
            pass

        # Add to history and switch turn
        self.move_history.append(move)
        self.turn = Color.BLACK if self.turn == Color.WHITE else Color.WHITE

    # ---------- Undo ----------
    def undo_move(self):
        if not self.move_history:
            return
        move = self.move_history.pop()

        # Restore piece positions
        self.board.set_piece(move.start, move.piece)
        self.board.set_piece(move.end, move.captured)

        # Restore piece flags
        move.piece.has_moved = move.previous_has_moved

        # Restore castling rights and en passant
        self.castling_rights = move.previous_castling_rights
        self.board.en_passant_target = move.previous_en_passant

        # Restore king position if necessary
        if move.piece.type == PieceType.KING:
            if move.piece.color == Color.WHITE:
                self.board.white_king_pos = move.start
            else:
                self.board.black_king_pos = move.start

        # Restore turn
        self.turn = Color.BLACK if self.turn == Color.WHITE else Color.WHITE
