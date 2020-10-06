import sys
import time
import random
from chess.polyglot import POLYGLOT_RANDOM_ARRAY, ZobristHasher
"""
This file runs an AI that does alpha-beta pruning with the 
inputted heuristic. This is not intended to be changed for the 
purposes of the competition.
"""


class AI:
    
    def __init__(self, board, color, heuristic):
        """Create a new AI."""
        # 1 for white, -1 for black.
        self.color = color
        # Inputted heuristic with static_score and think_time
        self.heuristic = heuristic
        # Chessboard
        self.board = board

        # A value which is better than winning.
        self.INFTY = sys.maxsize - 1
        # A value to indicate a player will win in the coming moves.
        self.WINNING_VALUE = sys.maxsize - 100

        # The best move in the current position.
        self.last_found_move = None

        # Iterative deepening stuff
        self.current_depth = 0
        self.time_limit = 0
        self.start_time = 0

        # Transposition table stuff
        self.TABLE_SIZE = 2000
        self.t_table = [None] * self.TABLE_SIZE
        self.hasher = ZobristHasher(POLYGLOT_RANDOM_ARRAY)
        self.pieces = {1: 1, 2: 3, 3: 3, 4: 5, 5: 9, 6: 0}

        # Quiescence stuff
        self.delta = 2
        self.futility = [0, 3, 5, 9]
        self.d_limit = 10
 
    def best_move(self):
        """Find and return the best move for the given position."""  
        self.last_found_move = None
        move = self.iterative_deepening(self.heuristic.think_time(self.board.fen(), 0, 0))
        return move
    
    def iterative_deepening(self, limit):
        """Run iterative deepening, stopping on the last depth once time runs out"""
        self.start_time = time.time()
        self.time_limit = limit
        d = 1
        move = list(self.board.legal_moves)[0]
        while time.time() - self.start_time < limit:
            self.current_depth = d
            #print('delta:', self.delta_count, 'futility:', self.fut_count)
            self.delta_count = self.fut_count = 0
            #print(d, time.time() - self.start_time)
            if self.last_found_move:
                move = self.last_found_move
                #print('Best move:', move)
            if d == self.d_limit + 1:
                break
            self.find_move(self.board, d, True,
                self.color, -1 * self.INFTY, self.INFTY)
            d += 1
        return move

    def find_move(self, board, depth, saveMove, turn, alpha, beta):
        """Does alpha-beta pruning to find the best move for the given position."""
        limit = self.check_limits(board, depth, False)
        if limit:
            if isinstance(limit, int):
                return 0 if limit == 1 else limit * -turn
            else:
                return None

        if depth == 0:
            return self.quiescence(board, self.current_depth * 2, False, 
                turn, -1 * self.INFTY, self.INFTY)
        elif depth < self.current_depth and depth <= 3:
            if not board.is_check():
                try:
                    prev = board.pop()
                except IndexError:
                    prev = None
                if prev and board.is_capture(prev):
                    board.push(prev)
                else:
                    if prev:
                        board.push(prev)
                    pat = self.heuristic.static_score(board.fen())
                    if (turn * (pat - turn * self.futility[depth]) >= 
                        turn * (beta if turn == 1 else alpha)):
                        self.fut_count += 1
                        return pat
        
        b_prev = None
        b_index = self.hasher(board) % self.TABLE_SIZE
        b_prev = self.t_table[b_index]
        if b_prev:
            if b_prev[0] == board.fen():
                if b_prev[3] >= depth:
                    if saveMove:
                        self.last_found_move = b_prev[4]
                    return b_prev[1]  
            else:
                b_prev = None

        best_value, refute = self.alpha_beta_pruning(board, depth,
            self.move_order(board, b_prev, False), turn, alpha, beta, False)

        if saveMove:
            self.last_found_move = refute
        self.t_table[b_index] = (board.fen(), best_value, 
            "PV" if alpha < best_value and best_value < beta else ("CUT" if beta <= alpha else "ALL"), 
            depth, refute)

        return best_value

    def quiescence(self, board, depth, saveMove, turn, alpha, beta):
        limit = self.check_limits(board, depth, True)
        if limit:
            if isinstance(limit, int):
                return limit * -turn
            else:
                return None
        if depth == 0:
            return self.heuristic.static_score(board.fen())
        
        pat = self.heuristic.static_score(board.fen())
        if not board.is_check():
            if turn == 1:
                alpha = max(pat, alpha)
                if pat >= beta:
                    return beta
            else:
                beta = min(pat, beta)
                if pat <= alpha:
                    return alpha

        best_value, _ = self.alpha_beta_pruning(board, depth,
            self.move_order(board, None, True), turn, alpha, beta,
            lambda m, a: turn * (pat + turn * 
                (self.pieces[board.piece_type_at(m.to_square) or 1] + self.delta)) < turn * a)

        if best_value == -turn * self.INFTY:
            return pat

        return best_value
        

    def check_limits(self, board, depth, Q):
        if time.time() - self.start_time > self.time_limit:
            return True
        if board.is_checkmate():
            return self.WINNING_VALUE - ((self.current_depth - depth) + (2 * self.current_depth if Q else 0))
        if board.can_claim_draw() or board.is_stalemate():
            return 1
        return False

    def alpha_beta_pruning(self, board, depth, moves, turn, alpha, beta, Q):

        best_value = -turn * self.INFTY
        current_value = 0
        refute = None

        for move in moves:
            board.push(move)
            if Q:
                if not board.is_capture(move):
                    current_value = self.quiescence(board, depth - 1, 
                        False, turn * -1, alpha, beta)
                else:
                    if Q(move, alpha if turn == 1 else beta):
                        self.delta_count += 1
                        current_value = alpha if turn == 1 else beta
                    else:
                        current_value = self.quiescence(board, depth - 1, 
                            False, turn * -1, alpha, beta)
            else:
                current_value = self.find_move(board, depth - 1, 
                    False, turn * -1, alpha, beta)
            board.pop()
            if current_value is None:
                return None 
            if turn == 1:
                if current_value > best_value:
                    best_value = current_value
                    refute = move
                alpha = max(alpha, best_value)
            else:
                if current_value < best_value:
                    best_value = current_value
                    refute = move
                beta = min(beta, best_value) 
            if beta <= alpha:
                break
        
        return alpha if turn == 1 else beta, refute
            

    def move_order(self, board, b_prev, Q):
        Q = Q and not board.is_check()
        moves = set(board.legal_moves)
        captures = []
        checks = []
        for m in moves:
            if board.is_capture(m):
                captures.append(m)
            else:
                if board.gives_check(m):
                    checks.append(m)
        captures.sort(key=lambda m: 90 if board.is_en_passant(m) else 
            9 * self.pieces[board.piece_type_at(m.from_square)] - 
            self.pieces[board.piece_type_at(m.to_square)])
        
        if b_prev:
            if b_prev[4]:
                yield b_prev[4]
        for c in captures:
            yield c
            if not Q:
                moves.remove(c)
        for c in checks:
            yield c
            if not Q:
                moves.remove(c)
        if not Q:
            for m in moves:
                yield m

"""import heuristic
import chess
h = heuristic.heuristic()
b = chess.Board('rnb5/pp2nppk/2p4p/2bp3q/P6P/1P4P1/2PPNP2/R1BQKR2 w Q - 0 16')
a = AI(b, 1, h)
random.seed(2000000)
print(a.best_move())
print(a.delta_count, a.fut_count)"""