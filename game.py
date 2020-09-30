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

def run_AI_game(b, h, game):
    white = AI.AI(b, 1, h)
    black = AI.AI(b, -1, h)
    m = white.best_move()
    b.push(m)
    node = game.add_variation(m)
    while not b.is_game_over():
        if b.turn == chess.BLACK:
            m = black.best_move()
            b.push(m)
            node = node.add_variation(m)
        else:
            m = white.best_move()
            b.push(m)
            node = node.add_variation(m)
        if b.can_claim_draw():
            b.is_game_over(claim_draw=True)
        print(b)
        print()

def run_human_AI_game(b, h, game, color):
    ai = AI.AI(b, color, h)
    while not b.is_game_over():
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
        if node:
            node = node.add_variation(m)
        else:
            node = game.add_variation(m)
        b.push(m)
        print(b)
        print("Current static score:", h.static_score(b.fen()))
        print()
        if b.can_claim_draw():
            b.is_game_over(claim_draw=True)

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
    if color:
        run_human_AI_game(b, h, game, color)
    else:
        run_AI_game(b, h, game)
    print(game)


if __name__ == "__main__":
    main()