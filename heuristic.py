import random
import re

class heuristic:

    def __init__(self):
        self.pieces = {'q': -9, 'r': -5, 'b': -3, 'n': -3, 'p': -1,
            'Q': 9, 'R': 5, 'B': 3, 'N': 3, 'P': 1}

    def static_score(self, board):
        """Returns the heuristic score of the board. Board is given as a 2D array (8x8), which holds rows of squares,
        where each square as either an empty string or a string piece (upper case for white, lower case for black)."""
        score = 0
        board = self.fen_to_array(board.fen())
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] in self.pieces:
                    score += self.pieces[board[i][j]]
        return score + random.random()

    def fen_to_array(self, fen):
        def row_to_array(row):
            out = []
            for c in row:
                if c.isdigit():
                    for _ in range(int(c)):
                        out.append("")
                else:
                    out.append(c)
            return out
        match = re.match("(.*)/(.*)/(.*)/(.*)/(.*)/(.*)/(.*)/(.*)", fen)
        array = [row_to_array(match[i]) for i in range(1, 9)]
        return array  

        
