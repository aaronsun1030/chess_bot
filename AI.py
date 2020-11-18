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
        self.delta = self.heuristic.delta
        self.futility = self.heuristic.futility
        self.d_limit = self.heuristic.d_limit
 
    def best_move(self):
        """Find and return the best move for the given position."""  
        self.last_found_move = None
        move = self.iterative_deepening(self.heuristic.think_time(self.board.board_fen(), 0, 0))
        return move
    
    def iterative_deepening(self, limit):
        """Run iterative deepening, stopping on the last depth once time runs out"""
        self.start_time = time.time()
        self.time_limit = limit
        d = 1
        move = list(self.board.legal_moves)[0]
        while time.time() - self.start_time < limit:
            self.current_depth = d
            if self.last_found_move:
                move = self.last_found_move
            if self.d_limit and d == self.d_limit + 1:
                break
            self.find_move(self.board, d, True,
                self.color, -1 * self.INFTY, self.INFTY, None)
            d += 1
        return move

    def find_move(self, board, depth, saveMove, turn, alpha, beta, moves):
        """Does alpha-beta pruning to find the best move for the given position."""
        limit = self.check_limits(board, depth, False)
        if limit:
            if isinstance(limit, int):
                return 0 if limit == 1 else limit * -turn, None
            else:
                return None, None
        # Quiescence search and futility pruning
        if depth == 0:
            return self.quiescence(board, self.current_depth * 2, False, 
                turn, -1 * self.INFTY, self.INFTY, None)
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
                    pat = self.heuristic.static_score(board.board_fen())
                    if (turn * (pat - turn * self.futility[depth]) >= 
                        turn * (beta if turn == 1 else alpha)):
                        return pat, None
        
        b_prev = None
        b_index = self.hasher(board) % self.TABLE_SIZE
        b_prev = self.t_table[b_index]
        if b_prev:
            if b_prev[0] == board.board_fen():
                if b_prev[3] >= depth:
                    if saveMove:
                        self.last_found_move = b_prev[4]
                    return b_prev[1], b_prev[4]
            else:
                b_prev = None

        best_value, refute = self.alpha_beta_pruning(board, depth,
            self.move_order(board, b_prev, moves, False), turn, alpha, beta, False)

        if saveMove:
            self.last_found_move = refute
        self.t_table[b_index] = (board.board_fen(), best_value, 
            "PV" if alpha < best_value and best_value < beta else ("CUT" if beta <= alpha else "ALL"), 
            depth, refute)

        return best_value, refute

    def quiescence(self, board, depth, saveMove, turn, alpha, beta, moves):
        """Quiescence search, which searches checks and captures to a given depth."""
        limit = self.check_limits(board, depth, True)
        if limit:
            if isinstance(limit, int):
                return limit * -turn, None
            else:
                return None, None
        if depth == 0:
            return self.heuristic.static_score(board.board_fen()), None
        
        pat = self.heuristic.static_score(board.board_fen())
        if not board.is_check():
            if turn == 1:
                alpha = max(pat, alpha)
                if pat >= beta:
                    return beta, None
            else:
                beta = min(pat, beta)
                if pat <= alpha:
                    return alpha, None

        # Delta pruning given here
        best_value, refute = self.alpha_beta_pruning(board, depth,
            self.move_order(board, None, moves, True), turn, alpha, beta,
            lambda m, a: turn * (pat + turn * 
                (self.pieces[board.piece_type_at(m.to_square) or 1] + self.delta)) < turn * a)

        if best_value == -turn * self.INFTY:
            return pat

        return best_value, refute

    def alpha_beta_pruning(self, board, depth, moves, turn, alpha, beta, Q):
        """Runs alpha-beta pruning, by going through each move and doing
        a recursive call on each move. There are two cases for quiescence and regular search."""
        best_value = -turn * self.INFTY
        current_value = 0
        refute = None
        killers = set()

        for move in moves:
            board.push(move)
            temp = None
            if Q:
                if not board.is_capture(move):
                    current_value, temp = self.quiescence(board, depth - 1, 
                        False, turn * -1, alpha, beta, killers)
                else:
                    if Q(move, alpha if turn == 1 else beta):
                        current_value = alpha if turn == 1 else beta
                    else:
                        current_value, temp = self.quiescence(board, depth - 1, 
                            False, turn * -1, alpha, beta, killers)
            else:
                current_value, temp = self.find_move(board, depth - 1, 
                    False, turn * -1, alpha, beta, killers)
            if temp:
                killers.add(temp)
            board.pop()
            if current_value is None:
                return None, None
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
            
    def check_limits(self, board, depth, Q):
        """Check whether to stop the search here for checkmate, draw, or timeout."""
        if time.time() - self.start_time > self.time_limit:
            return True
        if board.is_checkmate():
            return self.WINNING_VALUE - ((self.current_depth - depth) + (2 * self.current_depth if Q else 0))
        if board.can_claim_draw() or board.is_stalemate():
            return 1
        return False

    def move_order(self, board, b_prev, killers, Q):
        """Outputs the given moves for board, in the following order:
        1. Captures
        2. Checks
        The above two are given for quiescence Q, the below are not.
        3. Killers, or the best refutation for sister nodes
        4. All other legal moves in random order
        """
        Q = Q and not board.is_check()
        moves = set(board.legal_moves)
        captures = []
        checks = []
        for m in moves:
            remove = False
            if board.is_capture(m):
                captures.append(m)
                remove = True
            else:
                if board.gives_check(m):
                    checks.append(m)
                    remove = True
            if remove and killers:
                killers.discard(m)
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
        if killers:
            for k in killers:
                if k in moves:
                    yield k
                    if not Q:
                        moves.remove(k)
        if not Q:
            for m in moves:
                yield m
