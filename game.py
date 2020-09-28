import chess
import chess.pgn
import game
import heuristic
import AI

def main():
    num_AI = int(input("Enter your desired number of AIs (1 or 2): "))
    assert num_AI == 1 or num_AI == 2
    color = None
    if num_AI == 1:
        color = int(input("Enter color for AI, WHITE=1 and BLACK=-1: "))

    new = input('Would you like to load from a FEN? (y/n): ')
    fen = chess.STARTING_FEN
    if new == 'y':
        fen = input('Enter your FEN: ')
    b = chess.Board(fen)
    h = heuristic.heuristic()

    game = chess.pgn.Game()
    node = None
    if color:
        ai = AI.AI(b, color, h)
        while not b.is_game_over():
            if b.turn == chess.WHITE and color == 1 or b.turn == chess.BLACK and color == -1:
                print("AI is thinking...")
                m = ai.best_move()
            else:
                move = input("Enter your move: ")
                m = b.parse_san(move) 
            if node:
                node = node.add_variation(m)
            else:
                node = game.add_variation(m)
            b.push(m)
            print(b)
            print("Current static score:", h.static_score(b))
            print()
    else:
        white = AI.AI(b, 1, h)
        black = AI.AI(b, -1, h)
        m = white.best_move()
        b.push(m)
        node = game.add_variation(m)
        while not b.is_game_over():
            m = black.best_move()
            b.push(m)
            node = node.add_variation(m)
            print(b)
            print()
            if b.is_game_over():
                break
            m = white.best_move()
            b.push(m)
            node = node.add_variation(m)
            print(b)
            print()
    print(game)


if __name__ == "__main__":
    main()