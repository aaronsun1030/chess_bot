import random
import re

"""
This class is a chess heuristic whose main function
is static_score, which takes in a FEN and outputs a 
scoring of the board. The heuristic does not need to take into
account checkmates, as this is handled in AI. 
This file is meant to be changed for the purposes of the competition.
"""

class heuristic:

    def __init__(self):
        self.pieces = {'q': -9, 'r': -5, 'b': -3, 'n': -3, 'p': -1,
            'Q': 9, 'R': 5, 'B': 3, 'N': 3, 'P': 1}

    def static_score(self, fen):
        """Returns the heuristic score of the board. fen is given as a FEN of the board."""
        score = 0
        board = self.fen_to_array(fen)
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] in self.pieces:
                    score += self.pieces[board[i][j]]
        return score + random.random()

    def fen_to_array(self, fen):
        """Takes in a FEN and outputs the chessboard as a 2D array (8x8), which holds rows of squares, where each square is 
        either an empty string or a string representing a piece (upper case for white, lower case for black)."""
        def row_to_array(row):
            out = []
            for c in row:
                if c.isdigit():
                    for _ in range(int(c)):
                        out.append("")
                else:
                    out.append(c)
            return out
        match = re.match("(.*)/(.*)/(.*)/(.*)/(.*)/(.*)/(.*)/([^\\s]*)", fen)
        array = [row_to_array(match[i]) for i in range(1, 9)]
        return array  

    def think_time(self, fen, my_time, opp_time):
        return 20

