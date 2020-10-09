import chess
import chess.pgn
import game
import heuristic
import AI

"""
This file runs a sample game, either between 2 AIs given in 
AI.py or between user input and a single AI. This is primarily meant to 
be used in order to test the AI.
"""

# TODO: Change this to your heuristic!
h = heuristic.heuristic()

def run_AI_game(b, h):
    white = AI.AI(b, 1, h)
    black = AI.AI(b, -1, h)
    while not b.is_game_over(claim_draw=True):
        if b.turn == chess.BLACK:
            m = black.best_move()
            b.push(m)
        else:
            m = white.best_move()
            b.push(m)
        print(b)
        print("Current static score:", h.static_score(b.fen()))
        print()

def run_human_AI_game(b, h, color):
    ai = AI.AI(b, color, h)
    while not b.is_game_over(claim_draw=True):
        if b.turn == chess.WHITE and color == 1 or b.turn == chess.BLACK and color == -1:
            print("AI is thinking...")
            m = ai.best_move()
        else:
            while True:
                try:
                    move = input("Enter your move: ")
                    m = b.parse_san(move)
                    break
                except ValueError as e:
                    print(e)
        b.push(m)
        print(b)
        print("Current static score:", h.static_score(b.fen()))
        print()

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

    if color:
        run_human_AI_game(b, h, color)
    else:
        run_AI_game(b, h)
    print(chess.pgn.Game().from_board(b))


if __name__ == "__main__":
    main()