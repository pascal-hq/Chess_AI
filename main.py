from game.state import GameState
from game.piece import Color
from game.move import Move
from ai.engine import ChessAI


# ------------------------------
# Utilities
# ------------------------------
def print_board(state: GameState):
    """
    Simple ASCII board display.
    """
    print("  a b c d e f g h")
    for row in range(8):
        row_str = f"{8 - row} "
        for col in range(8):
            piece = state.board.get_piece((row, col))
            if piece:
                symbol = piece_symbol(piece)
            else:
                symbol = "."
            row_str += symbol + " "
        print(row_str + f"{8 - row}")
    print("  a b c d e f g h\n")


def piece_symbol(piece):
    """
    Returns single-character symbol for piece.
    Uppercase = White, Lowercase = Black
    """
    mapping = {
        "PAWN": "P",
        "ROOK": "R",
        "KNIGHT": "N",
        "BISHOP": "B",
        "QUEEN": "Q",
        "KING": "K",
    }
    sym = mapping[piece.type.name]
    return sym if piece.color == Color.WHITE else sym.lower()


def parse_move(user_input: str, state: GameState) -> Move:
    """
    Converts 'e2 e4' input into a Move object.
    """
    try:
        start_str, end_str = user_input.strip().split()
        start = (8 - int(start_str[1]), ord(start_str[0].lower()) - ord("a"))
        end = (8 - int(end_str[1]), ord(end_str[0].lower()) - ord("a"))
    except Exception:
        return None

    for move in state.get_legal_moves():
        if move.start == start and move.end == end:
            return move

    return None


# ------------------------------
# Main Game Loop
# ------------------------------
def main():
    state = GameState()

    # Example: Human (White) vs AI (Black)
    human_color = Color.WHITE
    ai_color = Color.BLACK
    ai_player = ChessAI(color=ai_color, depth=3)

    print("Welcome to Chess AI!")
    print_board(state)

    while True:
        # ---------------- Human Turn ----------------
        if state.turn == human_color:
            print("Your move (e.g., e2 e4): ")
            user_input = input("> ")
            move = parse_move(user_input, state)
            if move:
                state.make_move(move)
            else:
                print("Invalid move! Try again.")
                continue

        # ---------------- AI Turn ----------------
        else:
            print("AI is thinking...")
            move = ai_player.choose_move(state)
            if move:
                state.make_move(move)
                print(f"AI moves {move.start} -> {move.end}")
            else:
                # No legal moves
                print("AI has no moves left.")
                break

        # ---------------- Display ----------------
        print_board(state)

        # ---------------- Check for Game End ----------------
        if state.is_checkmate():
            if state.turn == human_color:
                print("Checkmate! AI wins.")
            else:
                print("Checkmate! You win.")
            break

        if state.is_stalemate():
            print("Stalemate! Draw.")
            break

        if state.is_in_check(state.turn):
            print(f"{state.turn.name} is in check!")


if __name__ == "__main__":
    main()
