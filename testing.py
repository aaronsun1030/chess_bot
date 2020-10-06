import AI
import heuristic
import chess.pgn
import chess

pgn = open("testing/tactics.pgn")
failed = open("testing/failed.txt", 'w')
h = heuristic.heuristic()
white = AI.AI(None, 1, h)
black = AI.AI(None, -1, h)

tactic = chess.pgn.read_game(pgn)
fail = False
last_d = 0

while tactic:
    player = white if tactic.headers._tag_roster['White'] == 'solver' else black
    player.board = tactic.board()
    turn = 0
    if not fail:
        player.d_limit = min(int(len(list(tactic.mainline_moves())) / 3) + 1, 3)
        last_d = player.d_limit
    else:
        player.d_limit = last_d + 1
        last_d += 1
        fail = False
    for move in tactic.mainline_moves():
        if turn % 2 != 0:
            m = player.best_move()
            if m != move:
                if not fail:
                    failed.write(str(tactic)[:-11] + '\n')
                failed.write("Played move " + str(m) + " instead of " + str(move) + '\n')
                fail = True
                break
        turn += 1
        player.board.push(move)
    if not fail:
        tactic = chess.pgn.read_game(pgn)
    else:
        failed.write('Failed at depth ' + str(last_d) + '. Trying again at a higher depth.\n')

pgn.close()
failed.close()