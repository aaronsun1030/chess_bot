import AI
import heuristic
import chess.pgn
import chess
import time

"""A testing file, which tries to solve a set of tactics at varying depths.
Starts for n-th tactic, where n is the value written in current.txt and saves
the results to results.txt. Does exactly tactics_per_run number of tactics per run."""

# TODO: Change this to your heuristic!
h = heuristic.heuristic()
# The number of tactics to solve.
tactics_per_run = 100
# The depth at which to give up (make smaller to make it not run forever)
max_depth = 5

pgn = open("testing/tactics.pgn")
results = open("testing/results.txt", 'a')
current = open("testing/current.txt", 'r')

white = AI.AI(None, 1, h)
black = AI.AI(None, -1, h)

tactic = chess.pgn.read_game(pgn)
first_try = True
fail = False
last_d = 0
num = int(current.read())
current.close()

for i in range(num):
    tactic = chess.pgn.read_game(pgn)

while tactic:
    if first_try:
        player = white if tactic.headers._tag_roster['White'] == 'solver' else black
        last_d = 1
    else:
        last_d += 1
    player.d_limit = last_d
    turn = 0
    fail = False
    player.board = tactic.board()
    start = time.time()
    for move in tactic.mainline_moves():
        if turn % 2 != 0:
            m = player.best_move()
            if m != move:
                if first_try:
                    results.write(str(tactic)[:-11] + '\n')
                results.write("Played move " + str(m) + " instead of " + str(move) + '\n')
                fail = True
                break
            player.d_limit -= 1
        turn += 1
        player.board.push(move)
    if fail:
        results.write('Failed at depth ' + str(last_d) + " in " + str(time.time() - start) + ' seconds. Trying again at a higher depth.\n')
        first_try = False
        if max_depth and last_d + 1 == max_depth:
            results.write('Giving up now...\n\n')
            results.close()
            results = open("testing/results.txt", 'a')
            first_try = True
    else:
        results.write("Success at depth " + str(last_d) + " in " + str(time.time() - start) + " seconds for the last iteration.\n\n")
        results.close()
        results = open("testing/results.txt", 'a')
        first_try = True
    if first_try:
        tactic = chess.pgn.read_game(pgn)
        num += 1
        current = open("testing/current.txt", 'w')
        current.write(str(num))
        current.close()
        if num % tactics_per_run == 0:
            break
        
pgn.close()
results.close()
