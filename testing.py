import AI
import heuristic
import chess.pgn
import chess
import time

pgn = open("testing/tactics.pgn")
failed = open("testing/failed.txt", 'a')
current = open("testing/current.txt", 'r')
h = heuristic.heuristic()
white = AI.AI(None, 1, h)
black = AI.AI(None, -1, h)

tactic = chess.pgn.read_game(pgn)
first_try = True
fail = False
last_d = 0
num = int(current.read())
current.close()
current = open("testing/current.txt", 'w')
current.write(str(num + 10))
current.close()

for i in range(num):
    tactic = chess.pgn.read_game(pgn)

num = 0

while tactic:
    fail = False
    if first_try:
        player = white if tactic.headers._tag_roster['White'] == 'solver' else black
        player.d_limit = 1
        last_d = player.d_limit
        player.board = tactic.board()
        turn = 0
    else:
        player.d_limit = last_d + 1
        last_d += 1
    start = time.time()
    for move in tactic.mainline_moves():
        if turn % 2 != 0:
            m = player.best_move()
            if m != move:
                if first_try:
                    failed.write(str(tactic)[:-11] + '\n')
                failed.write("Played move " + str(m) + " instead of " + str(move) + '\n')
                fail = True
                break
        turn += 1
        player.board.push(move)
    if not fail:
        failed.write("Success at depth " + str(last_d) + " in " + str(time.time() - start) + " seconds for the last iteration.\n\n")
        tactic = chess.pgn.read_game(pgn)
        num += 1
        if num % 10 == 0:
            break
        first_try = True
    else:
        failed.write('Failed at depth ' + str(last_d) + " in " + str(time.time() - start) + ' seconds. Trying again at a higher depth.\n')
        first_try = False

pgn.close()
failed.close()